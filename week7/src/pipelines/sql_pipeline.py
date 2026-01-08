import sqlite3
import sqlglot
import yaml
import os
from openai import OpenAI
from src.utils.schema_loader import SchemaLoader
from src.generator.sql_generator import SQLGenerator
from dotenv import load_dotenv
load_dotenv()
class SQLPipeline:
    def __init__(self, db_path, generator):
        self.db_path = db_path
        self.generator = generator
        self.schema_loader = SchemaLoader(db_path)

    def validate_sql(self, sql):
        forbidden = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER"]
        if any(word in sql.upper() for word in forbidden):
            raise PermissionError("Non-SELECT query detected.")
        
        sqlglot.transpile(sql, read="sqlite")
        return True

    def execute_safely(self, sql):
        conn = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            conn.close()

    def run(self, user_question, history):
        schema = self.schema_loader.get_schema_string()
        
        retries = 1
        last_error = None
        sql = self.generator.generate_query(user_question, schema, history)

        validation_retries = 2

        while(validation_retries>0):
            try:
                validation_retries -= 1
                verification = self.generator.verify_logic(user_question, sql, schema, history)

                if "VALID" not in verification.upper():
                    if validation_retries<=0:
                        print(verification)
                        raise Exception("The LLM was not able to generate Valid query.")
                    last_error = f"Logic verification failed: {verification}"
                    sql = self.generator.generate_query(user_question, schema, error_context=last_error, history = history)
                else:
                    break
            except Exception as e:
                return schema, {"status": "failed", "error": str(e), "sql": sql}


        while retries >= 0:
            try:
                self.validate_sql(sql)
                results = self.execute_safely(sql)
                
                summary = self.generator.summarize_results(user_question, results, history)
                
                return schema, {
                    "status": "success",
                    "sql": sql,
                    "results": results,
                    "answer": summary
                }
            
            except Exception as e:
                if retries == 0:
                    return schema, {"status": "failed", "error": str(e), "sql": sql}
                
                last_error = str(e)
                sql = self.generator.generate_query(user_question, schema, error_context=last_error, history=history)
                retries -= 1


def main(user_question:str, history):
    with open('src/config/model.yaml', 'r') as file:
        config_data = yaml.safe_load(file)
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key= os.environ['API_KEY']
    )
    model=config_data["model_name"]
    db_path = 'music_data.db'
    generator = SQLGenerator(client, model)
    schema, query_result = SQLPipeline(db_path, generator).run(user_question, history)

    return schema, query_result
    # if(query_result['status']=='failed'):
    #     print("Try again!!")
    #     print()
    #     print(query_result['error'])
    # else:
    #     print(f"question: {user_question}")
    #     print()
    #     print(f"sql generated: {query_result['sql']}")
    #     print()
    #     print(f"results: {query_result['results']}")
    #     print()
    #     print(f"summary: {query_result['answer']}")
