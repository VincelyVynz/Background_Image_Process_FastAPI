from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get('/health')
def health():
    return {"Status": "OK"}