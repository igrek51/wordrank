export class DictionaryStatisticsDTO {
  dictDisplayName: string;
  allCount: number;

  trained: ProgressBarData;
  trainingInProgress: ProgressBarData;
  touched: ProgressBarData;
  coolingDown: ProgressBarData;
}

export class ProgressBarData {
  count: number;
  percentage: string;
}
