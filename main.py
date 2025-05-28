from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import weaviate
from weaviate.classes.init import Auth
from weaviate.agents.query import QueryAgent
from weaviate.agents.utils import print_query_agent_response
from dotenv import load_dotenv
load_dotenv()

# Best practice: store your credentials in environment variables
weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]

def push_to_weaviate(job):
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=Auth.api_key(weaviate_api_key),
    )

    print(client.is_ready())  # Should print: `True`

    client.close()  # Free up resources
    return {"status": "dummy"}

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/weaviate/")
async def query_weaviate():
    return {"message": "Hello Weaviate"}


# Define request model
class QueryInput(BaseModel):
    prompt: str

@app.post("/weaviate/")
async def query_weaviate(input: QueryInput):
    try:
        headers = {
            "OPENAI-API-KEY": os.environ["OPENAI_API_KEY"],
        }

        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=os.environ["WEAVIATE_URL"],
            auth_credentials=Auth.api_key(os.environ["WEAVIATE_API_KEY"]),
            headers=headers,
        )

        qa = QueryAgent(
            client=client,
            collections=["JobReqs"],
        )

        response = qa.run(input.prompt)

        # Display using class method; you can also use .__str__() or parse response object manually
        output = response.display()
        client.close()
        return {"response": output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/weaviate/")
async def add_to_vector_db():
    return push_to_weaviate("a sample job description")

fake_items_db = [
    {
        "job_desc": '''
            About Weaviate
Weaviate is an AI startup with open source and creativity at its core. Our AI-native vector database uses machine learning to create meaningful insights from unstructured data in a completely new way. Named one of Forbes’ Top 50 AI startups, and with over a million monthly downloads, Weaviate is quickly growing in popularity with developers and enterprises alike.

Our team members work remotely across the globe with the flexibility to work from anywhere and at any time. Our people experience this as a massive benefit! Operating with a strong sense of ownership and collaboration, our teams prioritize results while empowering each individual to do their best work.

About this role
As a member of Weaviate’s Customer Solution Engineering Team, you will provide hands-on technical guidance and ensure our enterprise customers can effectively utilize our vector database to its fullest potential. You will work closely with customers to troubleshoot issues, guide them through complex setups, and ensure their success with our products. You will use your learnings and experience to instill repeatable processes and playbooks into our CSE, Product, and Engineering organizations to ensure Weaviate can scale effectively as our customer base grows.

This is what you’ll be doing
Provide expert technical guidance and support for Weaviate's products. Assist customers with deployment, configuration, troubleshooting and usage best practices.
Collaborate with our engineering teams to diagnose and resolve software issues, ensuring high availability and performance for all users.
Contribute to product development by reporting back customer feedback and participating in planning sessions to discuss improvements or new features.
Offer guidance and support to customers during product updates, migrations, and deployments.
Lead data migrations for customers moving from a proof of concept, or open-source deployment to our enterprise offerings.
Contribute to the evolution of our CSE team by designing and implementing the activities, playbooks and structures required to support our growing customer base.
What we are looking for
10+ years of experience in a technical role like a Technical Account Manager, Solution Engineer, Solution Architect, or a similar role within the tech industry, preferably with a focus on software or database technologies.
Experience with python and/or Go as well as SME in AI use cases and technology (generative search, RAG implementation, vector DBs).
Strong problem-solving skills and the ability to diagnose and resolve complex technical issues.
Familiarity with cloud services (AWS, GCP, Azure) and infrastructure as code tools like Terraform and Kubernetes.
Experience with monitoring tools like Grafana and Prometheus is advantageous.
Exceptional communication skills, capable of explaining complex technical concepts in clear, customer-friendly language.
A proactive, customer-first mindset, with a dedication to resolving customer issues and enhancing their experience with our products.
Ability to work independently, managing your workload and priorities in a remote work environment.
Alignment with Weaviate's company values, demonstrating a commitment to innovation, quality, and teamwork.
What we offer
100% remote with lots of flexibility, read more here.
Competitive compensation, including paid time off.
Budget available to spend on going to conferences, co-working space, home office equipment, etc.
Work with very experienced and fun team members.
An atmosphere that encourages learning and personal growth, and that gives you lots of freedom, flexibility, and responsibilities.
Are you interested?
Have a look at this page to learn what you can expect from our interview process. Be aware that conducting a background check is part of our onboarding.

If you are interested in Weaviate and this role, you can apply via the ‘apply now!’ button below. All of our communication will be done in response to your application. If you have any questions feel free to reach out to our recruiter via the application. In this way, we ensure that our people can focus on doing their best work.

Department
Solution Engineering (Platform Operations)
Remote status
Fully Remote
Employment type
Full-time
        '''
    },
    {"job_desc": "Bar"},
    {"job_desc": "Baz"},
]
@app.get("/jobs/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

