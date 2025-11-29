import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

def _build_chain(model_name: str):
    """Return the LangChain prompt|model chain. Raises informative errors if model fails."""
    model = OllamaLLM(model=model_name)
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain

def parse_with_ollama(dom_chunks, parse_description, model_name=None):
    """
    dom_chunks: list of string chunks
    parse_description: what to extract
    model_name: optional override (defaults to OLLAMA_MODEL)
    Returns: dict with { 'parsed_text': str, 'est_tokens': int }
    """
    model_name = model_name or OLLAMA_MODEL
    try:
        chain = _build_chain(model_name)
    except Exception as e:
        # If model not found or other Ollama client error, raise a clear message
        msg = (
            f"Failed to build Ollama chain with model '{model_name}': {e}\n\n"
            "Troubleshooting:\n"
            " - Verify the model is installed locally: run `ollama ls` in a terminal.\n"
            " - If the model name differs, set OLLAMA_MODEL in your .env (e.g. OLLAMA_MODEL=llama3.2).\n"
            " - If you're running a remote Ollama server, ensure connectivity and config."
        )
        raise RuntimeError(msg) from e

    parsed_results = []
    for i, chunk in enumerate(dom_chunks, start=1):
        try:
            response = chain.invoke(
                {"dom_content": chunk, "parse_description": parse_description}
            )
            parsed_text = str(response)
            parsed_results.append(parsed_text)
        except Exception as e:
            raise RuntimeError(
                f"Error parsing chunk {i}/{len(dom_chunks)} with model '{model_name}': {e}\n"
                "You can test the model locally with `ollama generate <model> \"hello\"` or `ollama ls`."
            ) from e

    full_text = "\n".join(parsed_results).strip()
    est_tokens = max(1, len(full_text) // 4)
    return {"parsed_text": full_text, "est_tokens": est_tokens}
