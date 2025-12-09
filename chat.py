from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, schemas, database, auth, chatbot
import os
from fastapi.responses import JSONResponse

router = APIRouter(
    tags=["Chat"]
)

@router.post("/chat", response_model=schemas.ChatResponse)
def chat_with_bot(request: schemas.ChatRequest, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    try:
        response_text = chatbot.process_query(request.message, db, current_user.id)
        return {"response": response_text}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"response": f"I encountered an internal error: {str(e)}"}


@router.get("/prompts")
def get_prompts():
    # Return the contents of AI_PROMPTS.md from the project root
    try:
        # project root is two levels above this file
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        prompts_path = os.path.join(project_root, 'AI_PROMPTS.md')
        if not os.path.exists(prompts_path):
            return JSONResponse(status_code=404, content={"error": "Prompts file not found."})
        with open(prompts_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

