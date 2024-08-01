# langserve-test1

This project uses [Poetry](https://python-poetry.org/).

## gcp auth setup

```shell
gcloud auth application-default login
```

## Running locally

```shell
poetry install

poetry run langchain serve
```

http://localhost:8000/docs
http://localhost:8000/joke/playground/
http://localhost:8000/joke2/playground/
http://localhost:8000/joke-spanish/playground/

```shell
curl -s 'http://localhost:8000/joke/invoke' -H 'Content-Type: application/json' --data-raw '{"input":{"topic":"penguins"}}' | jq
```

## Setup LangSmith (Optional)
LangSmith will help us trace, monitor and debug LangChain applications. 
You can sign up for LangSmith [here](https://smith.langchain.com/). 
If you don't have access, you can skip this section


```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # if not specified, defaults to "default"
```

## Running in Docker

This project folder includes a Dockerfile that allows you to easily build and host your LangServe app.

### Building the Image

To build the image, you simply:

```shell
docker build . -t langserve-test1
```

If you tag your image with something other than `langserve-test1`,
note it for use in the next step.

### Running the Image Locally

```shell
docker run \
    -v "$HOME/.config/gcloud/application_default_credentials.json":/gcp/creds.json:ro \
    -e GOOGLE_APPLICATION_CREDENTIALS=/gcp/creds.json \
    -e GOOGLE_CLOUD_PROJECT=`gcloud config get project` \
    -p 8080:8080 \
    langserve-test1
```
