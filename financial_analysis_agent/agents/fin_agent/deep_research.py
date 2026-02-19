import os
import datetime
import asyncio
import collections.abc
from typing import Literal

from google.adk.agents import BaseAgent, LlmAgent, LoopAgent, SequentialAgent
from google.adk.events import Event, EventActions
# from google.adk.tools import google_search
from shared.tools.web_search_tool import duckduckgo_search
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types
from pydantic import BaseModel, Field

# Configuration wrapper
class DeepResearchConfig:
    worker_model = "gemini-2.5-pro"
    critic_model = "gemini-2.5-pro"
    max_search_iterations = 3

config = DeepResearchConfig()

# --- Structured Output Models ---
class SearchQuery(BaseModel):
    search_query: str = Field(description="Specific search query.")

class Feedback(BaseModel):
    grade: Literal["pass", "fail"] = Field(description="Pass or fail grade.")
    comment: str = Field(description="Feedback comment.")
    follow_up_queries: list[SearchQuery] | None = Field(default=None, description="Follow-up queries.")

# --- Agents ---

# 1. Plan Generator (Simplified for HR Context)
plan_generator = LlmAgent(
    model=config.worker_model,
    name="plan_generator",
    description="Genera un plan de investigación para una empresa específica.",
    instruction="""
    Eres un Planificador de Inteligencia Estratégica.
    Tu objetivo es crear un plan de investigación específico para una empresa competidora objetivo.
    
    El plan debe incluir estas fases:
    1. [INVESTIGACIÓN] Estrategia y Movimientos de Mercado (Adquisiciones, Alianzas, Expansión).
    2. [INVESTIGACIÓN] Producto y Tecnología (Nuevas funcionalidades, IA, Precios).
    3. [INVESTIGACIÓN] Reputación y Feedback (Buscar en: Reddit, Glassdoor, Twitter/X, Foros, LinkedIn).
    4. [ENTREGABLE] Informe de Inteligencia Estratégica.

    Salida: El plan debe ser una lista con viñetas.
    IMPORTANTE: RESPONDE SIEMPRE EN ESPAÑOL.
    """,
    tools=[duckduckgo_search] 
)

# 2. Researcher (Executes the plan)
section_researcher = LlmAgent(
    model=config.worker_model,
    name="section_researcher",
    description="Ejecuta el plan de investigación.",
    instruction="""
    Eres un Investigador de Mercado Senior.
    Ejecuta el plan de investigación proporcionado en 'research_plan'.
    
    Fase 1: [INVESTIGACIÓN]
    - Para cada objetivo, genera 3-4 búsquedas específicas en Google/DuckDuckGo.
    - Ejecútalas usando `duckduckgo_search`.
    - Resume los hallazgos en detalle.
    
    Fase 2: [ENTREGABLE]
    - Una vez terminada la investigación, compila un informe completo basado *solo* en los hallazgos.
    - Formato Markdown.
    - IMPORTANTE: EL INFORME DEBE ESTAR EN ESPAÑOL.
    """,
    tools=[duckduckgo_search],
    output_key="section_research_findings"
)

# 3. Evaluator (Checks quality)
research_evaluator = LlmAgent(
    model=config.critic_model,
    name="research_evaluator",
    description="Evalúa la calidad de la investigación.",
    instruction="""
    Evalúa los 'section_research_findings'.
    - Si es completo y cubre Estrategia, Producto y Reputación: Califica 'pass'.
    - Si es superficial o falta info clave: Califica 'fail' y proporciona consultas de seguimiento específicas.
    - IMPORTANTE: RAZONA EN ESPAÑOL.
    """,
    output_schema=Feedback,
    output_key="research_evaluation"
)

# 4. Escalation Checker (Stops loop)
class EscalationChecker(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name=name)

    async def _run_async_impl(self, ctx) -> collections.abc.AsyncGenerator[Event, None]:
        if (ev := ctx.session.state.get("research_evaluation")) and ev.get("grade") == "pass":
            yield Event(author=self.name, actions=EventActions(escalate=True))
        else:
            yield Event(author=self.name)


# 5. Enhanced Searcher (Fixes gaps)
enhanced_search_executor = LlmAgent(
    model=config.worker_model,
    name="enhanced_search_executor",
    instruction="""
    Eres un Investigador de Profundidad.
    Revisa 'research_evaluation'. Si falló (fail), ejecuta 'follow_up_queries' usando `duckduckgo_search`.
    Añade los nuevos hallazgos a 'section_research_findings'.
    IMPORTANTE: ESCRIBE TODO EN ESPAÑOL.
    """,
    tools=[duckduckgo_search],
    output_key="section_research_findings"
)

# Pipeline
research_pipeline = SequentialAgent(
    name="research_pipeline",
    sub_agents=[
        plan_generator,
        section_researcher,
        LoopAgent(
            name="refinement_loop",
            max_iterations=config.max_search_iterations,
            sub_agents=[
                research_evaluator,
                EscalationChecker(name="escalation_checker"),
                enhanced_search_executor
            ]
        )
    ]
)

# --- Runner Wrapper ---
class DeepResearchRunner:
    def __init__(self):
        self.session_service = InMemorySessionService()
        self.runner = Runner(agent=research_pipeline, app_name="deep_research_app", session_service=self.session_service)

    def run(self, company_name: str):
        """
        Runs the deep research capabilities synchronously.
        """
        # We need to run the async runner in a sync context for Streamlit/Flask
        try:
           return asyncio.run(self._run_async(company_name))
        except RuntimeError:
            # If already in an event loop (like Streamlit sometimes), use existing loop
             loop = asyncio.get_event_loop()
             return loop.run_until_complete(self._run_async(company_name))

    async def _run_async(self, company_name: str):
        # Seed the plan generator with the specific company
        # Seed the plan generator with the specific company
        instruction = f"Crea un plan de investigación profunda para la empresa: {company_name}"
        
        # In a real ADK app, we'd pass this as input event content
        # For simplicity here, we rely on the agent getting the user message
        
        result_state = {}
        
        
        # Execute the runner
        # Corrected signature based on inspection:
        # run_async(*, user_id, session_id, new_message, ...)
        from google.genai import types
        
        session_id = "deep_research_session"
        user_id = "deep_research_user"
        
        # Ensure session exists
        session = await self.session_service.get_session(session_id=session_id, app_name="deep_research_app", user_id=user_id)
        if not session:
            await self.session_service.create_session(
                app_name="deep_research_app",
                session_id=session_id,
                user_id=user_id
            )
        
        # Iterate over the async generator to execute the agent
        async for _ in self.runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=types.Content(parts=[types.Part(text=instruction)])
        ):
            pass # Consume events
        
        # Extract findings from state
        session = await self.session_service.get_session(session_id="deep_research_session", app_name="deep_research_app", user_id="deep_research_user")
        if session and session.state:
            return session.state.get("section_research_findings", "No findings generated.")
        return "No session found."
