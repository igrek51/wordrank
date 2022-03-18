from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ProgressBarData(BaseModel):
    count: int
    percentage: str


class StatisticsModel(BaseModel):
    dictDisplayName: str
    allCount: int
    trained: ProgressBarData
    trainingInProgress: ProgressBarData
    touched: ProgressBarData
    coolingDown: ProgressBarData
