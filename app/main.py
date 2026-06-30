from fastapi import FastAPI

app = FastAPI()

@app.get("/home")
def read_home():
    return {"message": "Welcome to the Home Page!"}

@app.get("/health")
def read_health():
    return {"status": "healthy"}