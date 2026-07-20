## Part 1
"*Some messages match more than one rule (e.g. "Can you send me the scholarship
document?"). Pick how to resolve conflicts and explain your choice in 1 sentence.*"

If message contains more than one category, then it will display a category whose keyword appears first in the message. 

## Part 2

API_KEY should be placed in .env to avoid unintentional push into GitHub, where it can be stolen.

SQL injection vulnerability in `query` in `search_documents(question)` [source](https://learn.microsoft.com/en-us/sql/relational-databases/security/sql-injection?view=sql-server-ver17#:~:text=However%2C%20assume%20that%20the%20user%20enters%20the%20following%20text)
#### Solution
Passing down a question as a parameter is better than it being inserted directly in SQL query. 
```python
query = "SELECT id, title, content FROM documents WHERE content LIKE ?"
cursor.execute(query, (f"%{question}%",))
```
`ask_llm(question, docs)` method is called twice, which happen to contain API call. To avoid possible rate limit I would call it once.
#### Solution
```python
answer = ask_llm(q, docs)
print(answer)
save_answer(q, answer)
```
SQL injection vulnerability in `save_answer(question, answer)`. Same as in `search_documents(question)`.
#### Solution
Pass down as a paramter.
```python
conn.execute(
    "INSERT INTO answers (question, answer) VALUES (?, ?)",
    (question, answer)
)
```
No error handling for bad API calls in `ask_llm(question, docs)` method. I think it's a good practice to use at least connection, timeout and HTTP error handling. [source](https://medium.com/@PythonWithPurpose/python-api-error-handling-handle-errors-like-a-pro-a0da2899bf71)
#### Solution

```python
try:
  response = requests.post(
    "https://api.example.com/v1/generate",
    json={"model": "some-model", "prompt": prompt},
    headers={"Authorization": f"Bearer {API_KEY}"},
    timeout=5
  )
  response.raise_for_status()
  return response.json()["response"]

except request.exceptions.RequestException as error:
  print(f"API request failed: {error}")
  return 13 # I usually return 13 because then I know there is something wrong. Preference
```

## Part 3
#### Q1
I think in LIKE `'%...%'` the vulnerability was always there as user could change SQL query directly, so speed comes second. To fight with performance issue I would use pgvector [source](https://pganalyze.com/blog/postgresql-vs-sql-server-btree-index-deduplication#:~:text=PostgreSQL,-doesn%E2%80%99t)
#### Q2
The more documents you have the bigger prompt will be. It is bad because you can exceed LLM's context limit. Basic RAG splits documents into chunks, creates embeddings for those chunks, retrieves the top-k most relevant chunks for the question, and sends only those chunks to the LLM. So it will lower cost of prompt. [source](https://www.ibm.com/think/topics/retrieval-augmented-generation#:~:text=What%20are%20the%20benefits%20of%20RAG%3F)
#### Q3
1) API request can time out;
2) API request can return HTTP error;
3) API request can return invalid response.
In production I would use Try-Except to safely handle the errors.
#### Q4
<img width="689" height="356" alt="image" src="https://github.com/user-attachments/assets/ecf08dbb-9f8d-40d5-a4c3-5feb49734a0e" />

Multiple messages will belong to one conversation.

Time took: ~1h 30min and I think 20 mins to setup Git repo and write in a readable way readme file.

