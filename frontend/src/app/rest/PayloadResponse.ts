export class PayloadResponse {
  httpStatus: number;
  message: string;
  payload;

  static isOk(response: PayloadResponse): boolean {
    return response.httpStatus == 200;
  }
}
