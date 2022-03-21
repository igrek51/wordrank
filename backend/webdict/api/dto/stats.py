from pydantic import BaseModel


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
