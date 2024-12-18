from dotenv import load_dotenv
load_dotenv()

from azure.cosmos import CosmosClient
from sys import argv
import os
import pathlib
from api.contoso_chat.product import user
from azure.identity import DefaultAzureCredential
import prompty
import prompty.azure
from prompty.tracer import trace, Tracer, console_tracer, PromptyTracer


# add console and json tracer:
# this only has to be done once
# at application startup
Tracer.add("console", console_tracer)
json_tracer = PromptyTracer()
Tracer.add("PromptyTracer", json_tracer.tracer)


@trace
def get_user(userId: str) -> str:
    try:
        url = os.environ["COSMOS_ENDPOINT"]
        client = CosmosClient(url=url, credential=DefaultAzureCredential())
        db = client.get_database_client("limbo-dating-database")
        container = db.get_container_client("users")
        response = container.read_item(item=str(userId), partition_key=str(userId))
        # response["orders"] = response["orders"][:2]
        return response
    except Exception as e:
        print(f"Error retrieving user: {e}")
        return None


@trace
def get_response(userId, question, chat_history):
    print("getting user...")
    user = get_user(userId)
    print("user complete")
    context = user.find_users(question)
    print("users complete")
    print("getting result...")

    model_config = {
        "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
        "api_version": os.environ["AZURE_OPENAI_API_VERSION"],
    }

    result = prompty.execute(
        "chat.prompty",
        inputs={"question": question, "user": user, "documentation": context},
        configuration=model_config,
    )
    return {"question": question, "answer": result, "context": context}

if __name__ == "__main__":
    from tracing import init_tracing

    tracer = init_tracing(local_tracing=False)
    get_response(4, "What hiking jackets would you recommend?", [])
    #get_response(argv[1], argv[2], argv[3])