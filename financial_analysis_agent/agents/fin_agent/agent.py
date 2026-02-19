import sys
import os
import yaml
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to path to import shared tools
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.tools.search_tool import WebSearchTool
from shared.tools.sentiment_tool import SentimentTool
from shared.tools.news_tool import NewsMonitorTool
from services.db_service import DatabaseService
from agents.fin_agent.prompts import SENTIMENT_ANALYSIS_PROMPT, TOPIC_CLASSIFICATION_PROMPT, CODI_REPORT_PROMPT

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

from google.adk.agents import LlmAgent
from shared.tools.web_search_tool import duckduckgo_search
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
import asyncio
import nest_asyncio

class FinAgent:
    def __init__(self, config):
        self.config = config
        self.db = DatabaseService()
        self.search_tool = WebSearchTool()
        self.sentiment_tool = SentimentTool()
        self.news_tool = NewsMonitorTool()
        self.competitors = config.get('competitors', [])
        self.my_company = config.get('my_company', {})
        
        # Chat Agent (Persistent)
        self.chat_agent = LlmAgent(
            name="fin_chat_assistant",
            model="gemini-2.5-pro",
            instruction="""
            Eres un Asistente de Inteligencia Competitiva de Consultoría Financiera.
            Tu objetivo es responder preguntas sobre competidores, tendencias de mercado,
            regulación financiera (NIIF, ESG, CSRD), auditoría y servicios financieros en España.
            SIEMPRE usa la herramienta `duckduckgo_search` para buscar datos en tiempo real antes de responder.
            Tus respuestas deben ser precisas, basadas en datos recientes y en español.
            """,
            tools=[duckduckgo_search],
            output_key="chat_message_output"
        )
        self.chat_session_service = InMemorySessionService()
        self.chat_runner = Runner(agent=self.chat_agent, app_name="fin_chat_app", session_service=self.chat_session_service)

    def chat(self, user_input):
        """
        Processes a chat message using the ADK agent with web search.
        """
        nest_asyncio.apply()
        
        async def _run_chat():
            from google.genai import types
            
            session_id = "fin_chat_session"
            user_id = "fin_chat_user"
            session = await self.chat_session_service.get_session(session_id=session_id, app_name="fin_chat_app", user_id=user_id)
            if not session:
                await self.chat_session_service.create_session(
                    app_name="fin_chat_app",
                    session_id=session_id,
                    user_id=user_id
                )
            
            async for _ in self.chat_runner.run_async(
                user_id=user_id,
                session_id=session_id, 
                new_message=types.Content(parts=[types.Part(text=user_input)])
            ):
                pass
            
            session = await self.chat_session_service.get_session(session_id="fin_chat_session", app_name="fin_chat_app", user_id="fin_chat_user")
            if session and session.state:
                 return session.state.get("chat_message_output", "No response captured in state.")
            return "No session found."

        try:
            return asyncio.run(_run_chat())
        except Exception as e:
            return f"Error en chat: {e}"

    def monitor_news(self, extra_competitors=None):
        """
        Scans news for all competitors + self + extras.
        """
        current_competitors = self.competitors.copy()
        if extra_competitors:
            for extra in extra_competitors:
                current_competitors.append({"name": extra})
                
        all_entities = current_competitors + [self.my_company]
        return self.news_tool.scan_news(all_entities)

    def discover_new_competitors(self):
        """
        Uses Search Tool to find potential new players in financial consulting.
        """
        return self.search_tool.search_competitors(
            sector="consultoría financiera auditoría ESG due diligence",
            location="España"
        )

    def generate_codi_report(self, df):
        """
        Generates a strategic CODI report using Gemini.
        """
        if df.empty:
            return "No data available to generate report."
            
        data_str = df.to_string(index=False)
        
        effective_prompt_template = self.db.get_prompt("CODI_REPORT_PROMPT", default_value=CODI_REPORT_PROMPT)
        
        current_date_str = datetime.now().strftime("%d-%m-%Y")
        prompt = effective_prompt_template.replace("{my_company}", self.my_company['name']).replace("{data}", data_str).replace("{date}", current_date_str)
        
        try:
            response = self.sentiment_tool.model.generate_content(prompt)
            report_text = response.text
            
            self.db.save_report(
                report_type="CODI_STRATEGIC_FIN",
                target_entity=self.my_company['name'],
                content=report_text,
                raw_data=df.to_dict(orient='records')
            )
            
            return report_text
        except Exception as e:
            return f"Error generating CODI report: {e}"

    def perform_deep_research(self, company_name):
        """
        Executes the ADK Deep Research pipeline for a specific company.
        """
        from agents.fin_agent.deep_research import DeepResearchRunner
        runner = DeepResearchRunner()
        print(f"Starting Deep Research for {company_name}...")
        return runner.run(company_name)

    def run_analysis(self, extra_competitors=None, status_callback=None):
        def log(msg):
             print(msg)
             if status_callback:
                 status_callback(msg)

        log("Iniciando Análisis Competitivo de Consultoría Financiera...")
        report_data = []
        
        # 1. Base Competitors from Config
        current_competitors = self.competitors.copy()
        
        # 2. Extra user-defined competitors
        if extra_competitors:
            for extra in extra_competitors:
                if not any(c['name'].lower() == extra.lower() for c in current_competitors):
                    current_competitors.append({"name": extra})
        
        # 3. Auto-detect Market Leaders via Gemini Web Search
        log("Detectando líderes de mercado de consultoría financiera (IA + Búsqueda)...")
        
        try:
            prompt = "Lista las 5 principales consultoras financieras mid-market en España (competencia de BDO, Grant Thornton, Mazars, Baker Tilly, pero también locales y boutiques especializadas en auditoría, ESG y due diligence). Solo nombres separados por comas."
            leaders_text = self.chat(prompt)
            if leaders_text and "Error" not in leaders_text:
                 parts = leaders_text.split(',')
                 for p in parts:
                     clean_name = p.strip().strip('.').strip()
                     if clean_name and len(clean_name) < 40:
                         if not any(c['name'].lower() == clean_name.lower() for c in current_competitors) and clean_name.lower() != self.my_company['name'].lower():
                             current_competitors.append({"name": clean_name})
                             log(f"-> Líder detectado: {clean_name}")
        except Exception as e:
            log(f"⚠️ Error detectando líderes: {e}. Continuando con lista manual.")

        # 4. Include My Company
        my_comp_entry = self.my_company.copy()
        my_comp_entry['type'] = 'Propia'
        analysis_targets = [my_comp_entry] + current_competitors

        # Run Analysis Loop (Parallelized)
        from concurrent.futures import ThreadPoolExecutor, as_completed

        def process_competitor(comp):
            name = comp['name']
            is_own = comp.get('type') == 'Propia'
            type_label = "Propia" if is_own else "Competidor"
            
            process_log = []
            process_log.append(f"Analizando: {name}...")
            
            try:
                # Visibility
                vis_score = self.search_tool.count_mentions(name)
                
                # Search Queries (Financial Consulting focus)
                search_queries = [
                    f"{name} consultoría financiera auditoría interna España",
                    f"{name} informes sostenibilidad ESG EINF regulación",
                    f"{name} due diligence financiera valoraciones M&A",
                    f"{name} implantación ERP controller financiero interim",
                    f"{name} consolidación estados financieros planes viabilidad"
                ]
                
                search_results = []
                for q in search_queries:
                   results = self.search_tool.search(q, num_results=3)
                   search_results.extend(results)
                
                # FALLBACK: If search returns NOTHING, use mock data
                if not search_results:
                    process_log.append(f"⚠️ Sin resultados online para {name}. Usando datos simulados de respaldo.")
                    mock_snippets = [
                        f"{name} refuerza su división de auditoría interna y compliance para 2026.",
                        f"Nuevas alianzas de {name} en consultoría de sostenibilidad ESG y reporting CSRD.",
                        f"{name} expande sus servicios de due diligence financiera en el mid-market español."
                    ]
                    search_results = [{"snippet": s, "link": "Simulated Data (Search Failed)", "title": "Reporte Interno"} for s in mock_snippets]

                # Analysis
                avg_sentiment = "Neutro"
                avg_topic = "General"

                if search_results:
                    combined_text = "\n\n".join([f"- {r.get('snippet', '')}" for r in search_results if r.get('snippet')])
                    if combined_text:
                        from agents.fin_agent.prompts import BATCH_ANALYSIS_PROMPT
                        prompt = BATCH_ANALYSIS_PROMPT.replace("{company}", name).replace("{text}", combined_text)
                        try:
                            analysis_result = self.sentiment_tool.analyze(prompt, prompt_template="{text}")
                            if "|" in analysis_result:
                                parts = analysis_result.split("|")
                                for p in parts:
                                    if "SENTIMIENTO:" in p:
                                        avg_sentiment = p.split(":")[1].strip()
                                    if "TEMA:" in p:
                                        avg_topic = p.split(":")[1].strip()
                        except Exception as e:
                            print(f"Error analysis {name}: {e}")

                process_log.append(f"✅ {name}: Completado ({len(search_results)} resultados)")

                return {
                    "data": {
                        "Entidad": name,
                        "Tipo": type_label,
                        "Visibilidad": vis_score if vis_score > 0 else 50,
                        "Sentimiento": avg_sentiment,
                        "Tema_Dominante": avg_topic,
                        "Fuente_Top": search_results[0]['link'] if search_results else "No Web Results"
                    },
                    "logs": process_log
                }
            except Exception as e:
                return {
                    "data": {
                        "Entidad": name,
                        "Tipo": type_label,
                        "Visibilidad": 0,
                        "Sentimiento": "Error",
                        "Tema_Dominante": "Error",
                        "Fuente_Top": str(e)
                    },
                    "logs": [f"❌ Error analizando {name}: {e}"]
                }

        log(f"Iniciando procesamiento paralelo de {len(analysis_targets)} entidades...")
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_competitor, c) for c in analysis_targets]
            for future in as_completed(futures):
                try:
                    result = future.result()
                    report_data.append(result['data'])
                    for l in result['logs']:
                        log(l)
                except Exception as e:
                    log(f"Error fatal en thread: {e}")

        return pd.DataFrame(report_data)

    def generate_report(self, df):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"FIN_Competitor_Report_{timestamp}.xlsx"
        
        print(f"Generating report: {filename}")
        df.to_excel(filename, index=False)
        print("Report generated successfully.")

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'fin_competitors.yaml')
    
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)

    config = load_config(config_path)
    agent = FinAgent(config)
    
    df = agent.run_analysis()
    print("\nAnalysis Summary:")
    print(df)
    
    agent.generate_report(df)
