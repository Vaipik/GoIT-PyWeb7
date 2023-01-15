from fastapi import APIRouter


router = APIRouter(
    prefix="/currencies",
    tags=["currencies"]
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/")
async def get_currency():
    return fake_items_db
