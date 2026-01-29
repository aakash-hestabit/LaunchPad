import uuid
import json
from openai import OpenAI
from .session_memory import SessionMemory
from .vector_store import VectorStore
from .long_term_store import LongTermMemory
import os
import re

SIM_THRESHOLD = 0.80    
DUP_THRESHOLD = 0.93

def clean_llm_json(text: str):

    text = text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)

    return text.strip()


def safe_json_list(text: str):
    text = clean_llm_json(text)

    match = re.search(r"\[.*\]", text, re.S)
    if match:
        try:
            return json.loads(match.group())
        except:
            return []
    return []


def safe_json_obj(text: str):
    text = clean_llm_json(text)

    match = re.search(r"\{.*\}", text, re.S)
    if match:
        try:
            return json.loads(match.group())
        except:
            return {}
    return {}

class MemoryManager:
    def __init__(self):
        self.session = SessionMemory()
        self.vector = VectorStore()
        self.long_term = LongTermMemory()
        self.llm = OpenAI(api_key=os.environ["LLM_API_KEY"],
                          base_url="https://api.groq.com/openai/v1")

    def _generate_id(self):
        return int(uuid.uuid4().int % (2**63 - 1))

    def summarize(self, text: str):
        prompt = f"""
You are extracting LONG-TERM SEMANTIC MEMORY about the USER.

Only store facts that:
- Describe the user's preferences, goals, skills, projects, or constraints
- Would still be useful weeks later
- Help personalize future interactions

DO NOT store (STRICT):
- Temporary conversation flow
- Greetings or small talk
- What the assistant said unless it reveals something about the user
- Clarifications or meta dialogue


Return JSON list:
[
  {{"fact": "...", "category": "...", "importance": [0.0 - 1.0]}}
]

Conversation:
{text}
"""
        response = self.llm.responses.create(
            model="openai/gpt-oss-20b",
            input=prompt,
        )

        print(response.output_text)

        try:
            return safe_json_list(response.output_text)
        except:
            return []

    def store_interaction(self, user_msg, agent_msg):
        self.session.add("User", user_msg)
        self.session.add("Agent", agent_msg)

        facts = self.summarize("USER MESSAGE: "+user_msg + "\n" + "AGENT RESPONSE: "+ agent_msg)

        facts = [f for f in facts if f.get("importance", 0) >= 0.5]

        for fact in facts:
            self.reconcile_and_store(fact)
            # memory_id = self._generate_id()

            # self.vector.add_text(memory_id, fact["fact"])
            # self.long_term.store(
            #     memory_id,
            #     fact["fact"],
            #     fact.get("category", "general"),
            #     fact.get("importance", 0.5),
            # )

    def retrieve_context(self, query):
        short = self.session.get_context()
        results = self.vector.search(query, k=3)

        RECALL_THRESHOLD = 0.6  

        filtered_ids = [mem_id for mem_id, score in results if score >= RECALL_THRESHOLD]
        facts = self.long_term.get_by_ids(filtered_ids)

        return (f"""
            SESSION MEMORY:
            {short}

            RELEVANT FACTS:
            {facts}
            """)

    
    def reconcile_memory(self, old_fact: str, new_fact: str):
        prompt = f"""
You are managing an AI memory system.

Compare these two facts:

OLD: {old_fact}
NEW: {new_fact}

Choose exactly one label:
[DUPLICATE] - Same meaning
[CONTRADICTS] - Cannot both be true
[UPDATES] - B is a newer version of A
[MERGEABLE] - Different but can be combined
[UNRELATED] - Same topic but different facts

STRICT JSON OUTPUT:
Choose the relationship and output JSON:
{{
  "relation": one of ["DUPLICATE", "CONTRADICTS", "UPDATES", "MERGEABLE", "UNRELATED"],
  "final_fact": string | null
}}

Rules:
- If DUPLICATE - final_fact = null
- If CONTRADICTS or UPDATES - final_fact = NEW
- If MERGEABLE - final_fact = merged concise fact
- If UNRELATED - final_fact = null
"""
        res = self.llm.responses.create(
            model="openai/gpt-oss-20b",
            input=prompt,
        )

        print(f"\n reconclie result: \n {res.output_text} \n")

        return safe_json_obj(res.output_text)



    def reconcile_and_store(self, fact_obj):
        new_fact = fact_obj["fact"]
        candidates = self.vector.search(new_fact, k=3)

        if not candidates:
            self._store_new_fact(fact_obj)
            return

        for mem_id, score in candidates:

            if score < SIM_THRESHOLD:
                continue

            if score > DUP_THRESHOLD:
                return

            old_fact = self.long_term.get_by_ids([mem_id])[0]
            decision = self.reconcile_memory(old_fact, new_fact)

            rel = decision["relation"]
            final = decision["final_fact"]

            if rel == "DUPLICATE":
                return

            if rel in {"CONTRADICTS", "UPDATES", "MERGEABLE"}:
                self.vector.delete(mem_id)
                self.long_term.delete(mem_id)

                if final:
                    self._store_new_fact({**fact_obj, "fact": final})
                return

        self._store_new_fact(fact_obj)


    def _store_new_fact(self, fact_obj):
        if fact_obj.get("importance", 0) < 0.5:
            return

        memory_id = self._generate_id()
        self.vector.add_text(memory_id, fact_obj["fact"])
        self.long_term.store(
            memory_id,
            fact_obj["fact"],
            fact_obj.get("category", "general"),
            fact_obj.get("importance", 0.5),
        )