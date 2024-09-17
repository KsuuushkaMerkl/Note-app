from pydantic import BaseModel, ConfigDict


class Schemas(BaseModel):
    model_config = ConfigDict()

