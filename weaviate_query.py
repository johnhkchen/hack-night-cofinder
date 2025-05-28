import os
import weaviate
from weaviate.classes.init import Auth
from weaviate.agents.query import QueryAgent

from dotenv import load_dotenv

load_dotenv()

headers = {
    # Provide your required API key(s), e.g. Cohere, OpenAI, etc. for the configured vectorizer(s)
    "OPENAI-API-KEY": os.environ["OPENAI_API_KEY"],
}

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=os.environ["WEAVIATE_URL"],
    auth_credentials=Auth.api_key(os.environ["WEAVIATE_API_KEY"]),
    headers=headers,
)

# Instantiate a new agent object
qa = QueryAgent(
    client=client, collections=["JobReqs"]
)

# Perform a query
from weaviate.agents.utils import print_query_agent_response

response = qa.run(
    "Recommend cofounders for my AI startup?"
)

# Print the response
print_query_agent_response(response)    # Use the helper function
response.display()                      # Use the class method

client.close()
