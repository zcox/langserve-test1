# langserve-test1

## gcp auth setup

```shell
gcloud auth application-default login
```

## Running locally

```shell
source .venv/bin/activate

pip install -r requirements.txt

langchain serve
```

http://localhost:8000/docs
http://localhost:8000/joke/playground/
http://localhost:8000/joke2/playground/
http://localhost:8000/joke-spanish/playground/


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
docker build . -t my-langserve-app
```

If you tag your image with something other than `my-langserve-app`,
note it for use in the next step.

### Running the Image Locally

To run the image, you'll need to include any environment variables
necessary for your application.

In the below example, we inject the `OPENAI_API_KEY` environment
variable with the value set in my local environment
(`$OPENAI_API_KEY`)

We also expose port 8080 with the `-p 8080:8080` option.

```shell
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8080:8080 my-langserve-app
```

## Calling the Service

```shell
curl -s 'http://localhost:8000/joke/invoke' -H 'Content-Type: application/json' --data-raw '{"input":{"topic":"penguins"}}' | jq
```
