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
        Scans for recent news about competitors in BPO / Financial Process Outsourcing.
        Searches for: new services, technology, regulatory changes, M&A, loan staff.
        """
        news_results = []
        
        query_templates = [
            "{name} externalización contable fiscal BPO nuevo servicio 2026",
            "{name} digitalización facturas automatización RPA contabilidad España",
            "{name} SII Verifactu factura electrónica regulación fiscal",
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
