from fastapi import APIRouter

router = APIRouter()

@router.post("/schedule")
def set_schedule():
    pass

@router.delete("/schedule")
def delete_schedule():
    pass

@router.put("/schedule")
def update_schedule():
    pass