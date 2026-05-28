# This is a simple script to run that provides a basic health check endpoint for the backend docker container to ensure that the container is running and responsive with a status code of 200. It uses FastAPI to create a web server that listens on port 8080 and responds to GET requests at the /health endpoint with a JSON message indicating that the container is healthy but does not indicate the django server is running or healthy.
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)