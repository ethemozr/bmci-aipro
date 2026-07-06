from pydantic import BaseModel

class PortfolioCreate(BaseModel):
    symbol: str
    lot: float
    cost: float

class AlarmCreate(BaseModel):
    symbol: str
    condition_text: str
