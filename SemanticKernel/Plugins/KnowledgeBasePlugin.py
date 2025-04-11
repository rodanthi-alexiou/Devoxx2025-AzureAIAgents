from semantic_kernel.functions import kernel_function
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import json

class KnowledgeBasePlugin:
    def __init__(self, endpoint: str, index_name: str, api_key: str):
        self.search_client = SearchClient(
            endpoint=endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(api_key),
        )

    @kernel_function(
        name="search_docs",
        description="Retrieve top 3 documents from the knowledge base that match a query. Includes filename and a 500-word preview of each result."
    )
    def search_docs(self, query: str) -> str:
        results = self.search_client.search(query, include_total_count=True)
        top_hits = []

        for result in results:
            raw_payload = result.get("payload", "{}")
            try:
                payload = json.loads(raw_payload)
                file = payload.get("file", "Unknown file")
                text = payload.get("text", "[No text]")
                words = text.split()
                truncated_text = " ".join(words[:500])
                top_hits.append(f"📄 {file}\n{truncated_text}")
            except Exception as e:
                top_hits.append(f"❌ Error parsing payload: {e}")
            
            if len(top_hits) >= 3:
                break

        return "\n\n---\n\n".join(top_hits)



    @kernel_function(
        name="ask_with_context",
        description="Answers a user question using top 5 relevant documents from Azure Search."
    )
    def ask_with_context(self, query: str) -> str:
        results = self.search_client.search(query, top=5)

        context_parts = []

        for r in results:
            raw_payload = r.get("payload", "{}")
            try:
                payload = json.loads(raw_payload)
                text = payload.get("text", "")
                file = payload.get("file", "Unknown file")
                if text:
                    context_parts.append(f"[📄 {file}]\n{text}")
            except json.JSONDecodeError:
                continue  # skip malformed payloads

        if not context_parts:
            return "No relevant documents found."

        context = "\n\n".join(context_parts)

        return (
            f"Based on the following documents:\n---\n{context}\n---\n"
            f"Answer the question: {query}"
        )
