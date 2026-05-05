from backend.agent.graph import app

result = app.invoke({"query": "create a s3 bucket"})
print(result["output"])