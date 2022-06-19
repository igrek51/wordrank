from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from dataclasses import dataclass


class ExternalRank(BaseModel):
    rankId: str
    dictionaryId: str
    reversedDictionary: bool
    wordName: str
    definition: str
    rankValue: float
    triesCount: int
    lastUse: Optional[str] = None


@dataclass
class InternalRank:
    rankId: str
    rankValue: float
    triesCount: int
    user_word_id: str
    lastUse: Optional[str] = None
    counter_rank: Optional['InternalRank'] = None
    last_use_datetime: Optional[datetime] = None
