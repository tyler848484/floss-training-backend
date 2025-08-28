from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
import os
from dotenv import load_dotenv
from app.db import get_db
from sqlalchemy.orm import Session
import app.crud as crud
from app.schemas import ParentCreate
from app.jwt import get_current_parent
from app.jwt import create_access_token
from urllib.parse import urlencode
from fastapi.responses import JSONResponse

load_dotenv()

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@router.get("/login")
async def login(request: Request):
    redirect_uri = GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    google_sub = user_info["sub"]
    email = user_info["email"]
    first_name = user_info.get("given_name")
    last_name = user_info.get("family_name")

    parent = crud.get_parent_by_google_sub(db, google_sub)
    if not parent:
        parent = crud.get_parent_by_email(db, email)
        if parent:
            parent = crud.update_parent_google_sub(db, parent.id, google_sub)
        else:    
            parent_data = ParentCreate(
                first_name=first_name,
                last_name=last_name,
                email=email,
                google_sub=google_sub
            )
            parent = crud.create_parent(db, parent_data)

    access_token = create_access_token(data={"sub": str(parent.id), "id": str(parent.id)})

    response = RedirectResponse(url="https://floss-private-soccer-coaching-ui.vercel.app/auth-success")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
        domain="floss-private-soccer-coaching-ui.vercel.app",
        path="/",
        max_age=60*60*24*7
    )
    return response

@router.post("/logout")
def logout():
    response = JSONResponse({"message": "Logged out"})
    response.delete_cookie(
        key="access_token",
        path="/",
        domain="floss-private-soccer-coaching-ui.vercel.app",
        secure=True,
        httponly=True,
        samesite="none"
    )
    return response
