import os
import json
import traceback

class WebSearchTool:
    """
    Web search using Gemini's built-in Google Search grounding.
    No external API keys or CSE needed—uses the same Vertex AI / Gemini auth.
    """
    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is None:
            from google import genai
            use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "0") == "1"
            if use_vertex:
                self._client = genai.Client(
                    vertexai=True,
                    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
                    location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
                )
                print("[WebSearchTool] Initialized with Vertex AI.")
            else:
                self._client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
                print("[WebSearchTool] Initialized with Gemini API Key.")
        return self._client

    def search(self, query, num_results=5):
        """
        Uses Gemini with Google Search grounding to search the web.
        Returns a list of dicts with keys: title, link, snippet.
        """
        from google.genai import types

        client = self._get_client()

        prompt = (
            f"Busca en la web información actual sobre: {query}\n\n"
            f"Devuelve los {num_results} resultados más relevantes. "
            f"Para cada resultado incluye: título, URL y un resumen breve del contenido encontrado. "
            f"Responde SOLO con un array JSON válido con las claves: \"title\", \"link\", \"snippet\". "
            f"Sin texto adicional, sin bloques de código markdown."
        )

        try:
            print(f"[WebSearchTool] Gemini Grounded Search: {query[:70]}...")
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                    temperature=0.1,
                )
            )

            results = []

            # Method 1: Extract from grounding_metadata (most reliable)
            if response.candidates and response.candidates[0].grounding_metadata:
                gm = response.candidates[0].grounding_metadata
                if hasattr(gm, 'grounding_chunks') and gm.grounding_chunks:
                    for chunk in gm.grounding_chunks[:num_results]:
                        if hasattr(chunk, 'web') and chunk.web:
                            results.append({
                                "title": getattr(chunk.web, 'title', '') or "",
                                "link": getattr(chunk.web, 'uri', '') or "",
                                "snippet": ""
                            })

            # Enrich snippets from the text response if we got grounding chunks
            if results and response.text:
                # Use the full text as context for all results
                full_text = response.text[:1000]
                # Distribute text across results as snippets
                for i, r in enumerate(results):
                    if not r["snippet"]:
                        r["snippet"] = full_text[i*200:(i+1)*200] if len(full_text) > i*200 else full_text[:200]

            # Method 2: If no grounding chunks, try to parse the text response
            if not results and response.text:
                text = response.text.strip()
                # Remove markdown code fences if present
                if text.startswith("```"):
                    lines = text.split("\n")
                    text = "\n".join(lines[1:])
                    if text.endswith("```"):
                        text = text[:-3]
                    text = text.strip()

                try:
                    parsed = json.loads(text)
                    if isinstance(parsed, list):
                        for item in parsed[:num_results]:
                            results.append({
                                "title": item.get("title", ""),
                                "link": item.get("link", item.get("url", "")),
                                "snippet": item.get("snippet", item.get("summary", ""))
                            })
                except json.JSONDecodeError:
                    # Use the raw text as a single result
                    results.append({
                        "title": "Resultado de búsqueda Gemini",
                        "link": "gemini-grounded-search",
                        "snippet": response.text[:500]
                    })

            print(f"[WebSearchTool] Found {len(results)} results for: {query[:40]}")
            return results

        except Exception as e:
            print(f"[WebSearchTool] Search error: {type(e).__name__}: {e}")
            traceback.print_exc()
            return []

    def search_competitors(self, sector="consultoría RRHH gestión talento", location="España", year="2026"):
        """
        Searches for potential new competitors or market players.
        """
        query = f"principales empresas y startups de {sector} en {location} {year} ranking comparativa"
        print(f"[WebSearchTool] Discovering players: {query}")
        return self.search(query, num_results=10)

    def count_mentions(self, company_name):
        """
        Returns an approximate visibility score using grounded search.
        """
        query = f'"{company_name}" consultoría RRHH España noticias recientes'
        results = self.search(query, num_results=10)
        return len(results) * 100
