import dlt
import json
from datetime import datetime

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
                # pdf_path = download_google_drive_pdf(link)
                # text = extract_text(pdf_path)
                # TODO define function for chunking
                chunks = chunk_for_weaviate(text)
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

# Chunk PDFs
import os
process_linkedin_links_with_dlt(linkedin_links, output_path="demo_chunks.json")
     