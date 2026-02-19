import sys
import os
from datetime import datetime, timedelta

# Add project root
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from shared.tools.search_tool import WebSearchTool

class NewsMonitorTool:
    def __init__(self):
        self.search_tool = WebSearchTool()

    def scan_news(self, competitors, days_back=7):
        """
        Scans for recent news about competitors.
        """
        news_results = []
        
        for comp in competitors:
            name = comp['name']
            # User request: "el analisis de mercado y la monitorizacion la hoiciese por la web tambien (redes sociales, foros....)"
            # Targeting forums and news specificially.
            query = f"{name} noticias RRHH talento lanzamiento liderazgo 2026"
            
            print(f"[NewsMonitor] Scanning for: {query}")
            # We use the updated WebSearchTool which now uses DuckDuckGo
            results = self.search_tool.search(query, num_results=5)
            
            for r in results:
                news_results.append({
                    "Entity": name,
                    "Title": r['title'],
                    "Source": r['link'],
                    "Snippet": r['snippet'],
                    # DDG often puts relative time in snippet or body, but we can't easily parse it without more logic.
                    "Date": "Recent" 
                })
                
        return news_results
