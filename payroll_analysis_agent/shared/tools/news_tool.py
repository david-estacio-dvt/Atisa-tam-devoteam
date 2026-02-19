import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from shared.tools.search_tool import WebSearchTool

class NewsMonitorTool:
    def __init__(self):
        self.search_tool = WebSearchTool()

    def scan_news(self, competitors, days_back=7):
        """
        Scans for recent news about competitors in Payroll & HR Administration.
        Searches for: new features, pricing, regulatory, integrations.
        """
        news_results = []
        
        query_templates = [
            "{name} software nómina nueva funcionalidad lanzamiento España 2026",
            "{name} control horario fichaje app empleado portal",
            "{name} retribución flexible beneficios RPA automatización nómina",
        ]
        
        for comp in competitors:
            name = comp['name']
            for template in query_templates:
                query = template.format(name=name)
                print(f"[NewsMonitor] Scanning: {query[:60]}...")
                results = self.search_tool.search(query, num_results=3)
                for r in results:
                    if not any(n['Source'] == r['link'] for n in news_results):
                        news_results.append({
                            "Entity": name,
                            "Title": r.get('title', 'Sin título'),
                            "Source": r.get('link', ''),
                            "Snippet": r.get('snippet', ''),
                            "Date": "Reciente"
                        })
        return news_results
