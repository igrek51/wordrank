from fastapi import FastAPI


def setup_rank_endpoints(app: FastAPI):
    @app.get("/rank/top/{top:int}/{lang}")
    async def rank_top(top: int, lang: str):
        return {
            "rankId": 858,
            "dictionaryId": 1,
            "reversedDictionary": False,
            "wordName": "remit",
            "definition": "przekazać",
            "rankValue": "3",
            "triesCount": 10,
            "lastUse": "2022-03-15 11:28:32",
        }
