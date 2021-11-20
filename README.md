### text sumarization with huggingface pegasus libraries

example based on <https://huggingface.co/transformers/model_doc/pegasus.html>

```
docker build -t <app name> ,

docker run -d -p 8080:0880  <app name>

curl -H 'Content-type: application/json' -d '{"text_payload":"<insert text here>"}' localhost:8080/summarize
```
