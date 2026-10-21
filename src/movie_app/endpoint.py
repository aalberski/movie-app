import json
from http import HTTPStatus

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class EventSchema(BaseModel):
    """Event Schema"""

    event_id: str
    event_type: str
    event_data: dict

@router.post("/", dependencies=[])
def handle_event(
    data: EventSchema,
):
    print(data)

    # This is where you implement the AI logic to handle the event