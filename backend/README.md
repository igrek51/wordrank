# Webdict backend in Python
Web application for vocabulary training with dynamically changing word ranks

## Running locally
```
make run
```

## Add words in a batch
```
curl -X POST -H "Content-Type: application/json" -d '{"words": ["word1", "word2"]}' http://localhost:5000/add
```