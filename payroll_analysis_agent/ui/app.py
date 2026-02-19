
import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agents.payroll_agent.agent import PayrollAgent, load_config
from agents.payroll_agent.prompts import CODI_REPORT_PROMPT

st.set_page_config(
    page_title="Agente de Inteligencia Competitiva - Nómina y Admin. Personal",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Agente de Inteligencia Competitiva - Nómina y Administración de Personal")
st.markdown("""
**Asistente Estratégico para CODI**
Monitoriza competidores de nómina, control horario, portales de empleado, retribución flexible y RPAs.
""")

with st.sidebar:
    st.header("Configuración")
    st.write("Competidores configurados:")
    try:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'payroll_competitors.yaml')
        config = load_config(config_path)
        for comp in config.get('competitors', []):
            st.text(f"- {comp['name']}")
    except Exception as e:
        st.error(f"Error cargando configuración: {e}")
    st.divider()
    st.subheader("Análisis Adicional")
    extra_comp = st.text_input("Añadir otro competidor (opcional):", placeholder="Ej. Sage")

if 'agent' not in st.session_state:
    st.session_state.agent = PayrollAgent(config)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Análisis de Mercado", "🚀 Descubrimiento", "📑 Informe Estratégico", "🔔 Monitorización", "⚙️ Configuración", "📜 Historia"])

with tab5:
    st.header("⚙️ Configuración del Agente")
    st.markdown("Ajusta los **System Prompts** para cambiar el comportamiento del agente.")
    if 'db' not in st.session_state:
        from services.db_service import DatabaseService
        st.session_state.db = DatabaseService()
    current_codi_prompt = st.session_state.db.get_prompt("CODI_REPORT_PROMPT", default_value=CODI_REPORT_PROMPT)
    new_prompt = st.text_area("Prompt para Informe CODI (Estratégico)", value=current_codi_prompt, height=300)
    if st.button("Guardar Configuración"):
        st.session_state.db.save_prompt("CODI_REPORT_PROMPT", new_prompt)
        st.success("¡Configuración guardada!")

with tab6:
    st.header("📜 Historial de Informes")
    if 'db' not in st.session_state:
        from services.db_service import DatabaseService
        st.session_state.db = DatabaseService()
    history = st.session_state.db.get_history(limit=10)
    if history:
        for record in history:
            with st.expander(f"{record['timestamp']} - {record['target_entity']} ({record['report_type']})"):
                st.markdown(record['report_content'])
                st.json(record['raw_data_json'])
    else:
        st.info("No hay informes guardados aún.")

with tab1:
    if st.button("Ejecutar Análisis Completo", use_container_width=True):
        st.info("Iniciando motor de análisis de nómina y admin. personal...")
        status_box = st.empty()
        def ui_callback(msg):
            status_box.text(f"🚀 {msg}")
        with st.spinner("Procesando datos en tiempo real..."):
            try:
                extras = [extra_comp] if extra_comp else []
                df = st.session_state.agent.run_analysis(extra_competitors=extras, status_callback=ui_callback)
                st.session_state.last_df = df
                st.success("¡Análisis Estratégico Completado!")
                status_box.empty()
            except Exception as e:
                st.error(f"Fallo en el análisis: {e}")

with tab2:
    st.header("Nuevos Players de Nómina y HR Tech")
    if st.button("Escanear Nuevos Competidores", use_container_width=True):
        with st.spinner("Escaneando el mercado de nómina y HR Tech..."):
            results = st.session_state.agent.discover_new_competitors()
            if results:
                st.success(f"¡Encontrados {len(results)} posibles players!")
                for r in results:
                    st.markdown(f"**[{r['title']}]({r['link']})**")
                    st.caption(r['snippet'])
            else:
                st.warning("No se encontraron nuevos players.")

with tab3:
    st.header("Informe Estratégico CODI - Nómina y Admin. Personal")
    if st.button("Generar Informe Ejecutivo", use_container_width=True):
        if 'last_df' in st.session_state:
            with st.spinner("Redactando informe estratégico de nómina..."):
                report = st.session_state.agent.generate_codi_report(st.session_state.last_df)
                st.markdown("### 📑 Informe Estratégico (CODI + Gap Analysis Nómina)")
                st.markdown(report)
                st.download_button("Descargar Informe (MD)", report, file_name="Informe_CODI_Nomina.md")
        else:
            st.warning("Ejecuta primero el análisis para generar datos.")

with tab4:
    st.header("🔔 Monitorización de Marca")
    st.caption("Rastrea nuevas funcionalidades, pricing, control horario, retribución flexible, RPAs.")
    if st.button("Escanear Menciones", use_container_width=True):
        with st.spinner("Escaneando fuentes..."):
            extras = [extra_comp] if extra_comp else []
            news = st.session_state.agent.monitor_news(extra_competitors=extras)
            if news:
                for n in news:
                    with st.expander(f"{n['Entity']}: {n['Title']}"):
                        st.write(f"**Fuente:** {n['Source']}")
                        st.write(n['Snippet'])
            else:
                st.info("No se encontraron noticias relevantes.")

if 'last_df' in st.session_state:
    st.subheader("Último Análisis de Mercado - Nómina")
    if 'Visibilidad' in st.session_state.last_df.columns:
        vis_series = pd.to_numeric(st.session_state.last_df[st.session_state.last_df['Tipo'] == 'Competidor']['Visibilidad'], errors='coerce')
        avg_vis = vis_series.mean()
        st.metric("Visibilidad Media Competencia", f"{avg_vis:.1f}" if pd.notna(avg_vis) else "N/A")
    st.dataframe(st.session_state.last_df, use_container_width=True)
    if 'Visibilidad' in st.session_state.last_df.columns:
        st.bar_chart(st.session_state.last_df.set_index('Entidad')['Visibilidad'])

st.divider()
st.subheader("💬 Chat Estratégico - Nómina y HR Tech")

if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Pregunta sobre nómina, control horario, retribución flexible, HR Tech..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        with st.spinner("Buscando en la web..."):
            response = st.session_state.agent.chat(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
