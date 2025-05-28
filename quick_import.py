import weaviate
from weaviate.classes.init import Auth
import requests, json, os

from dotenv import load_dotenv

load_dotenv()

# Environment variables for secure credential handling
weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]

# Connect to Weaviate
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_api_key),
)

data = [
    {
        "description": "PhD in Machine Learning from Stanford, 10+ years in AI startups. Led the deployment of multimodal LLMs for real-world enterprise use cases."
    },
    {
        "description": "Graphic designer specializing in poster layouts and typography. No experience in coding or AI but interested in 'cool tech stuff'."
    },
    {
        "description": "Full-stack developer with experience in Python, Node.js, and Rust. Built and scaled infrastructure for a YC-backed SaaS company."
    },
    {
        "description": "Recent college graduate with a business degree. Passionate about becoming a 'CEO of something big'. No technical background."
    },
    {
        "description": "ML engineer at a FAANG company. Built production-grade ML pipelines and contributed to open-source deep learning libraries."
    },
    {
        "description": "Influencer with 250k followers on TikTok. Looking to 'get into AI' but unsure where to start."
    },
    {
        "description": "CTO at an edtech company. Experience building adaptive learning platforms with real-time personalization using AI models."
    },
    {
        "description": "Barista with strong people skills. Believes AI is the future and wants to help with social media promotion for an AI startup."
    },
    {
        "description": "Former quant trader turned deep learning researcher. Interested in cofounding a startup around RLHF or AI safety tooling."
    },
    {
        "description": "iOS developer focused on fitness apps. No AI experience, but proficient in mobile UX and frontend optimization."
    },
]

# Assume the data is a list of dictionaries like: { "description": "..." }
profiles = client.collections.get("JobReqs")

with profiles.batch.fixed_size(batch_size=200) as batch:
    for entry in data:
        batch.add_object(
            {
                "description": entry["description"],
            }
        )
        if batch.number_errors > 10:
            print("Batch import stopped due to excessive errors.")
            break

failed_objects = profiles.batch.failed_objects
if failed_objects:
    print(f"Number of failed imports: {len(failed_objects)}")
    print(f"First failed object: {failed_objects[0]}")

client.close()
