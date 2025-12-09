from fastapi import FastAPI
from database import engine
import models
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, grades, chat, subjects

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Performance Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(grades.router)
app.include_router(chat.router)
app.include_router(subjects.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Performance Chatbot API"}
if __name__ == "__main__":
    import uvicorn, threading, time, webbrowser
    def open_browser():
        # Wait a short moment for the server to start
        time.sleep(1)
        webbrowser.open("http://localhost:8000")
    threading.Thread(target=open_browser).start()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
