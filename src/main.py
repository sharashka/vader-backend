from fastapi import FastAPI

app = FastAPI()


@app.get("/api/v1/status")
def status():
    return {"status": "ok"}
