import os
import json
from google import genai
from google.genai import types

def duckduckgo_search(query: str) -> str:
    """
    Realiza una búsqueda web utilizando Gemini con Google Search Grounding.
    Utiliza esta herramienta cuando necesites encontrar información general, noticias o datos sobre empresas.
    
    Args:
        query: La consulta de búsqueda.
    
    Returns:
        Un string JSON con una lista de resultados, donde cada resultado tiene 'title', 'href' y 'body'.
    """
    try:
        use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "0") == "1"
        if use_vertex:
            client = genai.Client(
                vertexai=True,
                project=os.getenv("GOOGLE_CLOUD_PROJECT"),
                location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
            )
        else:
            client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Busca en la web: {query}. Resume los resultados encontrados en español.",
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                temperature=0.2,
            )
        )

        # Build results from grounding metadata
        results = []
        if response.candidates and response.candidates[0].grounding_metadata:
            gm = response.candidates[0].grounding_metadata
            if hasattr(gm, 'grounding_chunks') and gm.grounding_chunks:
                for chunk in gm.grounding_chunks[:5]:
                    if hasattr(chunk, 'web') and chunk.web:
                        results.append({
                            "title": getattr(chunk.web, 'title', '') or "Resultado",
                            "href": getattr(chunk.web, 'uri', '') or "",
                            "body": ""
                        })

        # If we got results, use the response text to enrich
        if results and response.text:
            # Put the full response as body of the first result
            results[0]["body"] = response.text[:500]
        elif response.text:
            # No grounding chunks, but we have text
            results.append({
                "title": "Resultado de búsqueda",
                "href": "",
                "body": response.text[:500]
            })

        return json.dumps(results, ensure_ascii=False)
    except Exception as e:
        return json.dumps([{"error": str(e)}])
