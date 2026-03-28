from pydantic import BaseModel

class ResourceAction(BaseModel):
    cpu: int
    memory: int


class ResourceObservation(BaseModel):
    observation: str
    reward: float
    done: bool
    info: dict


class ResourceState(BaseModel):
    steps: int