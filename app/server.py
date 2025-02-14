from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

class Joke(BaseModel):
    explanation: str = Field(description="Explains why the joke is funny")
    joke: str = Field(description="The generated joke")

app = FastAPI()

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a professional stand-up comedian. Your job is to write a joke about a given topic.
     Always format your output as a json object, with the following fields:
     - explanation: explain why your joke is funny, and how it uses the specified topic
     - joke: the joke that you wrote"""),
    ("human", "Tell me a joke about {topic}."),
])

model = ChatVertexAI(
    model="gemini-1.5-pro-001",
    response_mime_type = "application/json",
    this_does_not_exist = "foo",
)

parser = JsonOutputParser(pydantic_object=Joke)

chain = prompt | model | parser

add_routes(
    app,
    chain,
    path="/joke",
    output_type=Joke,
)

prompt2 = ChatPromptTemplate.from_messages([
    ("system", "You are an 11-year old who writes jokes."),
    ("human", "Tell me a joke about {topic}."),
])

model2 = ChatVertexAI(
    model="gemini-1.5-pro-001",
).with_structured_output(Joke)
# ).with_structured_output(Joke, method="json_mode")

chain2 = prompt2 | model2

add_routes(
    app,
    chain2,
    path="/joke2",
    output_type=Joke,
)

prompt3a = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an 11-year old who writes jokes."),
        ("human", "Tell me a joke about {topic}."),
    ]
)

# Pydantic is supposed to be able to generate JSON Schema, but it does not work here, I suspect due to the wrong version being used
# https://docs.pydantic.dev/latest/concepts/json_schema/#generating-json-schema
# jokeSchema = Joke.model_json_schema()
# print(jokeSchema)

model3a = ChatVertexAI(
    model="gemini-1.5-pro-001",
    response_mime_type="application/json",
    response_schema={
        "type": "object",
        "properties": {
            "explanation": {
                "type": "string",
                "description": "Explains why the joke is funny",
            },
            "joke": {"type": "string", "description": "The generated joke"},
        },
        "required": ["explanation", "joke"],
    },
)

parser3a = JsonOutputParser()

prompt3b = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert at translating jokes into other languages."),
        ("human", "Translate the following joke into spanish: {joke}."),
    ]
)

model3b = ChatVertexAI(
    model="gemini-1.5-pro-001",
    response_mime_type="application/json",
    response_schema={
        "type": "object",
        "properties": {
            "translation": {
                "type": "string",
                "description": "The translated joke",
            },
        },
        "required": ["translation"],
    },
)

parser3b = JsonOutputParser()

chain3 = prompt3a | model3a | parser3a | prompt3b | model3b | parser3b

add_routes(
    app,
    chain3,
    path="/joke-spanish",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
