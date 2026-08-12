from fastapi import FastAPI

app = FastAPI(title="RepoLens AI Service")


@app.get("/")
def root():
    return {"message": "RepoLens AI Service is running!"}