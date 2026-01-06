import re

class SQLGenerator:
    def __init__(self, client, model_name):
        self.client = client
        self.model_name = model_name

    def generate_query(self, question, schema, error_context=None):
        error_info = ""
        if error_context:
            error_info = f"\nYour previous query failed with error: {error_context}. Fix the logic."

        SYSTEM_PROMPT = f"""
        You are a specialized SQLite Expert. Your sole job is to translate Natural Language into valid, executable SQL queries.

        ### DATABASE SCHEMA:
        {schema}

        ### CRITICAL RULES:
        1. OUTPUT FORMAT: Return ONLY raw SQL code. No markdown, no backticks.
        2. JOINS: When asked for "by [entity name]", always JOIN the relevant tables to provide the NAME of the entity, not just the ID.
        3. SQLITE DATE HANDLING: 
        - Use `strftime('%Y', sale_date) = '2023'` or `sale_date LIKE '2023%'` for year-based filtering.
        - Do not use functions like YEAR() which are not supported in SQLite.
        4. AGGREGATIONS: Use descriptive aliases for calculated columns (e.g., SUM(amount) AS total_sales).
        5. SAFETY: Use SELECT only and if the user asks to modify should simply respond "I do not have the authority to do that". Include LIMIT 100 if not specified.
        """

        USER_PROMPT = f"User Question: {question}{error_info}\nSQL:"

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT}
            ]
        )
        
        raw_sql = response.choices[0].message.content
        return self._clean_sql(raw_sql)

    def _clean_sql(self, text):
        text = re.sub(r"```sql|```", "", text)
        # only the first SELECT statement to be takken into consideration to avoid running multiple statements
        match = re.search(r"(SELECT.*?;?)", text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()
    
    def verify_logic(self, question, generated_sql, schema):
        """Checks if the generated SQL actually matches the user's intent."""
        
        verify_prompt = f"""
        Analyze the following SQL query and the user's question. 
        Does the SQL correctly answer the question based on the schema?

        User Question: {question}
        Generated SQL: {generated_sql}
        Schema: {schema}

        If the SQL is correct, respond with 'VALID'. 
        If it is wrong do not include 'VALID' (e.g., wrong column, missing filter, wrong join), explain WHY briefly.
        """

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": verify_prompt}]
        )
        
        content = response.choices[0].message.content
        return content.strip()

    def summarize_results(self, question, results):
        prompt = f"The user asked: '{question}'. The database returned these rows: {results}. Provide a concise, friendly summary of this answer."
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content