from pydantic import BaseModel


class Trigger(BaseModel):
    element_id: str
    trigger: str
