from fastapi import FastAPI

app = FastAPI(
    title="Risk Engine",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "Risk Engine Running"
    }