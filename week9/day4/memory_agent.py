class MemoryAugmentedAgent:
    def __init__(self, agent, embedder, session_mem, vector_store, db):
        self.agent = agent
        self.embedder = embedder
        self.session_mem = session_mem
        self.vector_store = vector_store
        self.db = db

    def step(self, user_input):

        self.session_mem.add("user", user_input)

        query_emb = self.embedder(user_input)

        similar_context = self.vector_store.search(query_emb)

        memory_block = "\n".join(similar_context)
        short_context = self.session_mem.get_context()

        final_prompt = f"""
        Relevant past memories:
        {memory_block}

        Recent conversation:
        {short_context}

        User: {user_input}
        """

        reply = self.agent.generate_reply(messages=[{"role": "user", "content": final_prompt}])

        summary = self.summarize(user_input, reply)
        emb = self.embedder(summary)
        self.vector_store.add(emb, summary)
        self.save_to_sqlite(summary, emb)

        self.session_mem.add("assistant", reply)
        return reply

    def summarize(self, user, reply):
        prompt = f"Summarize key facts from this interaction:\nUser: {user}\nAgent: {reply}"
        return self.agent.generate_reply(messages=[{"role":"user","content":prompt}])
