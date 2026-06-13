# doc_ai.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST  = os.getenv("OLLAMA_HOST",  "http://10.22.39.192:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5vl:latest")


def call_llm(prompt: str, max_tokens: int = 3000) -> str:
    resp = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json={
            "model":   OLLAMA_MODEL,
            "prompt":  prompt,
            "stream":  False,
            "options": {"temperature": 0.2, "num_predict": max_tokens}
        },
        timeout=300
    )
    resp.raise_for_status()
    return resp.json()["response"].strip()


def get_rag_context(query: str) -> str:
    """Get relevant context from TechCorp knowledge base."""
    try:
        import sys
        rag_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "rag_system"
        )
        sys.path.insert(0, rag_path)
        from rag import get_collection, embed_texts

        qvec       = embed_texts([query])[0]
        collection = get_collection()
        if collection.count() == 0:
            return ""

        results = collection.query(
            query_embeddings=[qvec],
            n_results=2,
            include=["documents"]
        )
        return "\n\n".join(results["documents"][0])
    except Exception:
        return ""


def generate_document(
    doc_type:       str,
    prompt_template: str,
    field_values:   dict,
    use_rag:        bool = True
) -> dict:
    """
    Generate a complete document using Qwen.
    Returns { content, word_count, rag_used }
    """
    # Fill template with field values
    try:
        filled_prompt = prompt_template.format(**field_values)
    except KeyError as e:
        filled_prompt = prompt_template
        print(f"Template key error: {e}")

    # Add RAG context if available
    rag_context = ""
    if use_rag:
        search_query = f"{doc_type} {field_values.get('company_name', '')} {field_values.get('project_name', '')}"
        rag_context  = get_rag_context(search_query)

    if rag_context:
        filled_prompt += f"\n\nADDITIONAL COMPANY CONTEXT (use where relevant):\n{rag_context}"

    content    = call_llm(filled_prompt, max_tokens=3000)
    word_count = len(content.split())

    return {
        "content":    content,
        "word_count": word_count,
        "rag_used":   bool(rag_context),
        "doc_type":   doc_type
    }


def improve_section(section_text: str, instruction: str) -> str:
    """Improve a specific section of a document."""
    prompt = (
        f"Improve this section of a business document.\n\n"
        f"INSTRUCTION: {instruction}\n\n"
        f"CURRENT TEXT:\n{section_text}\n\n"
        f"Provide the improved version only. No explanations."
    )
    return call_llm(prompt, max_tokens=1024)


def translate_document(content: str, target_language: str) -> str:
    """Translate a document to another language."""
    prompt = (
        f"Translate this business document to {target_language}.\n"
        f"Maintain all formatting, headings, and structure.\n"
        f"Keep any proper nouns, company names, and technical terms as-is.\n\n"
        f"DOCUMENT:\n{content[:3000]}\n\n"
        f"TRANSLATION:"
    )
    return call_llm(prompt, max_tokens=3000)