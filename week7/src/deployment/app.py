import uuid
import json
import io
import os
from typing import Optional
from PIL import Image
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel

from src.memory.memory_store import RedisChatMemory
from src.evaluation.rag_eval import RAGEvaluator
from src.retriever.hybrid_image_search import image_hybrid_search, hybrid_search, main
from src.pipelines.sql_pipeline import main as sql_main

load_dotenv()

def export_to_json(endpoint, session_id, query, context, response, eval_results, filename="CHAT-LOGS.json"):
    """Appends logs to a JSON file without overwriting previous entries."""
    log_entry = {
        "endpoint": endpoint,
        "session_id": session_id,
        "query": query,
        "context": str(context), 
        "response": response,
        "evaluation": eval_results
    }
    
    logs = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                logs = json.load(f)
                if not isinstance(logs, list):
                    logs = [logs]
        except (json.JSONDecodeError, IOError):
            logs = []
            
    logs.append(log_entry)
    
    with open(filename, 'w') as f:
        json.dump(logs, f, indent=4)


app = FastAPI(title="RAG System")
memory = RedisChatMemory()
evaluator = RAGEvaluator(llm_client=None) 

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

class SQLRequest(BaseModel):
    query: str
    session_id: Optional[str] = None


async def execute_rag_flow(query: str, context: any, session_id: str):
    history = memory.get_history(session_id)
    max_retries = 2
    attempts = 0
    final_answer = None
    eval_results = {}

    while attempts <= max_retries:
        raw_answer = await main(query, context, history)
        eval_results = evaluator.evaluate_response(query, context, raw_answer, history)
        
        if not eval_results.get('hallucination_detected', False):
            final_answer = raw_answer
            break 
        
        attempts += 1
        if attempts > max_retries:
            final_answer = f"Note: I'm unsure about this. {raw_answer}"
        else:
            final_answer = raw_answer

    memory.save_message(session_id, "user", query)
    memory.save_message(session_id, "assistant", final_answer)
    memory.export_to_json(session_id)
    export_to_json("/ask", session_id, query, context, final_answer, eval_results)

    return {
        "session_id": session_id,
        "answer": final_answer,
        "evaluation": eval_results,
        "retries": attempts
    }


@app.post("/ask")
async def ask_question(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())
    context = await hybrid_search(request.query)
    return await execute_rag_flow(request.query, context, session_id)

@app.post("/ask-image")
async def ask_image(
    query: str = Form(...), 
    session_id: Optional[str] = Form(None), 
    file: UploadFile = File(...)
):
    current_session_id = session_id or str(uuid.uuid4())
    
    try:
        image_data = await file.read()
        image_object = Image.open(io.BytesIO(image_data))
        if image_object.mode != 'RGB':
            image_object = image_object.convert('RGB')
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file or format")
    
    context = await image_hybrid_search(image_object)
    return await execute_rag_flow(query, context, current_session_id)

@app.post("/ask-sql")
async def ask_sql(request: SQLRequest):
    session_id = request.session_id or str(uuid.uuid4())
    try:
        history = memory.get_history(session_id)
        max_retries = 2
        attempts = 0
        final_answer = None
        schema = None

        while attempts <= max_retries:
            schema, query_results = sql_main(request.query, history)
            if(query_results['status']=='failed'):
                return {
                    "session_id": session_id,
                    "answer": query_results,
                    "evaluation": "No evaluation as the query generation failed",
                    "retries": attempts
                }

            eval_results = evaluator.evaluate_response(request.query, schema, query_results, history)
            
            if not eval_results.get('hallucination_detected', False):
                final_answer = query_results
                break 
            
            attempts += 1
            if attempts > max_retries:
                final_answer = f"Note: I'm unsure about this. {query_results}"
            else:
                final_answer = query_results

        memory.save_message(session_id, "user", request.query)
        memory.save_message(session_id, "assistant", str(final_answer))
        memory.export_to_json(session_id)
        export_to_json("/ask-sql", session_id, request.query, schema, final_answer, eval_results)

        return {
            "session_id": session_id,
            "answer": final_answer,
            "evaluation": eval_results,
            "retries": attempts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SQL Pipeline Error: {str(e)}")