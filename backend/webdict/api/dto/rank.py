from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class RankModel(BaseModel):
    rankId: str
    dictionaryId: str
    reversedDictionary: bool
    wordName: str
    definition: str
    rankValue: float
    triesCount: int
    lastUse: Optional[str] = None

    counter_rank: Optional['RankModel'] = None
    last_use_datetime: Optional[datetime] = None
