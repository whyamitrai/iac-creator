from fastapi import FastAPI
import uvicorn
from backend.api.routes import router


app = FastAPI()

app.include_router(router)


@app.get("/")
def health():
    return {"status": "running"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    print("started")
