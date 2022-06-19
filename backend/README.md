# WordRank backend in Python
Web application for vocabulary training with dynamically changing word ranks

## Running locally
```
make run
```

## Add words in a batch
```bash
curl -X POST -H "Content-Type: application/json"  http://localhost:8000/wordrank/api/word \
    -d '{"word": "name", "definition": "def", "dictionaryCode": "en-pl", "userId": "1"}'
```

```python
import requests

words = [
    ("name2", "def"),
    ("name3", "def"),
]

for name, definition in words:
    r = requests.post('http://localhost:8000/wordrank/api/word', 
        json={'word': name, 'definition': definition, 'dictionaryCode': 'en-pl', 'userId': '1'})
    r.raise_for_status()
```
