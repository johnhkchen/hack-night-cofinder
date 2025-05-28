import dlt
import json
import requests
from datetime import datetime

# Json of format
# {"name": "bob", "summary": "bob is a software engineer", "jobs": [{"title": "Software Engineer", "company": "TechCorp", "location": "Remote", "description": "Developing software solutions."}]}
def chunk_for_weaviate(json_data):
    """
    Simple function to chunk JSON data for Weaviate.
    Creates logical chunks from structured JSON data.
    
    Args:
        json_data (dict): JSON object to chunk
    
    Returns:
        list: List of chunks with text and metadata
    """
    chunks = []
    
    # Extract basic info
    name = json_data.get('name', 'Unknown')
    summary = json_data.get('summary', '')
    
    # Create main profile chunk
    profile_text = f"Name: {name}"
    if summary:
        profile_text += f"\nSummary: {summary}"
    
    chunks.append({
        "text": profile_text,
        "metadata": {
            "type": "profile",
            "name": name,
            "chunk_id": f"{name.lower().replace(' ', '_')}_profile"
        }
    })
    
    # Process jobs if they exist
    jobs = json_data.get('jobs', [])
    for i, job in enumerate(jobs):
        job_text = f"Person: {name}\n"
        job_text += f"Job Title: {job.get('title', 'N/A')}\n"
        job_text += f"Company: {job.get('company', 'N/A')}\n"
        job_text += f"Location: {job.get('location', 'N/A')}\n"
        job_text += f"Description: {job.get('description', 'N/A')}"
        
        chunks.append({
            "text": job_text,
            "metadata": {
                "type": "job",
                "name": name,
                "job_title": job.get('title', 'N/A'),
                "company": job.get('company', 'N/A'),
                "chunk_id": f"{name.lower().replace(' ', '_')}_job_{i}"
            }
        })
    
    return chunks

def download_mock_data_json(link):
    response = requests.get(link)
    if response.status_code == 200:
        try:
            return response.json()  # Parse JSON response
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def process_linkedin_links_with_dlt(linkedin_links, output_path="demo_chunks.json"):
    # Create a simple dlt pipeline for tracking
    pipeline = dlt.pipeline(
        pipeline_name="linkedin_job_posts",
        destination="duckdb"
    )

    @dlt.resource
    def track_processing():
        all_chunks = []
        for link in linkedin_links:
            print(f"Processing: {link}")
            try:

                resultJson = download_mock_data_json(link)                
                chunks = chunk_for_weaviate(resultJson)
                all_chunks.extend(chunks)

                # Yield tracking info
                yield {
                    "link": link,
                    "status": "success",
                    "chunks_created": len(chunks),
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                print(f"❌ Failed to process {link}: {e}")
                yield {
                    "link": link,
                    "status": "failed",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }

        # Save chunks as before
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Saved {len(all_chunks)} chunks to {output_path}")

    # Run pipeline
    info = pipeline.run(track_processing())

    # Just print the info object - it has what we need
    print(f"\n🔍 DLT Pipeline completed!")
    print(f"✅ Load info: {info}")

    return info
