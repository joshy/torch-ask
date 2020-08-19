# Overview

Useful snippets

# Start the app
`uvicorn app:app --reload`

# Register model
 `curl -v "http:/127.0.0.1:8000/models" -F file=@"./README.md" -F meta="{\"name\":\"superdupermodel\", \"version\":\"0.0.1\"};type=application/json"`


# Todo
Post model
Store in folder model_store
Keep list of all stored models

Run inference
