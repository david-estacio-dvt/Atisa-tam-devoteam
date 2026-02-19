SENTIMENT_ANALYSIS_PROMPT = """
Analiza el sentimiento del siguiente texto sobre una empresa de consultoría financiera.
Clasifica como: Positivo, Negativo, Neutro o Mixto.
Responde SOLO con la clasificación, sin explicación.

Texto: {text}
"""

TOPIC_CLASSIFICATION_PROMPT = """
Clasifica el tema dominante del siguiente texto sobre consultoría financiera.
Categorías posibles: Auditoría, ESG/Sostenibilidad, Due Diligence, ERP, Regulatorio, Valoraciones, Riesgos, General.
Responde SOLO con la categoría, sin explicación.

Texto: {text}
"""

CODI_REPORT_PROMPT = """
Eres un Consultor Estratégico Senior de Servicios Financieros (Nivel MBB - McKinsey/Bain/BCG).
Tu objetivo es generar un **INFORME ESTRATÉGICO EXHAUSTIVO Y DETALLADO** para **{my_company}**.
**Fecha del Informe**: {date}

**⚠️ ADVERTENCIA:** El usuario ha solicitado explícitamente un informe LARGO y PROFUNDO.
- NO hagas resúmenes breves.
- NO uses frases genéricas.
- Si falta información, infiérela basada en tu conocimiento del mercado de consultoría financiera en España, pero márcala como "Estimación de mercado".

### Contexto de Cliente ({my_company}):
- **Enfoque Estratégico**: Consultoría Financiera Integral (Auditoría, ESG, Due Diligence, ERP).
- **Catálogo de Servicios Prioritario**:
  1. **Consolidación de estados financieros** y controller financiero.
  2. **Auditoría interna** y revisión contable y de riesgos.
  3. **Controller financiero e Interim Management**.
  4. **Soporte regulatorio** y consultas contables (NIIF, PGC).
  5. **Informes de Sostenibilidad (ESG/EINF)** y reporting no financiero.
  6. **Due Diligence Financiera** y operaciones corporativas.
  7. **Valoraciones económicas** y M&A advisory.
  8. **Mapa de riesgos**, análisis y rediseño de procesos financieros.
  9. **Planes de viabilidad** e informes económicos.
  10. **Implantaciones ERP** y conciliación de saldos contables.

### Datos de Inteligencia Competitiva (Input Real):
{data}

---

### ESTRUCTURA OBLIGATORIA DEL INFORME:

#### 1. Resumen Ejecutivo (Executive Summary)
- Visión general del estado competitivo de {my_company} vs. el mercado de consultoría financiera en España.
- Principales 3 alertas rojas (amenazas) y 3 luces verdes (oportunidades).

#### 2. Comparativa de Servicios y Posicionamiento (Gap Analysis)
**Instrucción Clave:** Genera una tabla comparativa detallada. Si no tienes el dato exacto, usa "N/D" o estima.

| Servicio | {my_company} | Competencia (Líder) | Gap / Diferencia |
| :--- | :--- | :--- | :--- |
| **Auditoría Interna** | (Capacidad) | (Ej. BDO, Grant Thornton) | ¿Cobertura? |
| **ESG / EINF** | (Capacidad) | (Ej. Mazars, KPMG) | ¿Nos falta expertise? |
| **Due Diligence** | (Capacidad) | (Ej. Big 4 adjacent) | ¿Competitividad en M&A? |
| **Implantación ERP** | (Capacidad) | (Ej. SAP Partners) | ¿Tecnología? |

#### 3. Análisis de Tendencias del Mercado
- ESG como motor de crecimiento: ¿Quién lidera la narrativa?
- Regulación (CSRD, taxonomía UE): ¿Quién se está posicionando mejor?
- Digitalización financiera: IA en auditoría, automatización contable.

#### 4. Radar CODI (Extendido)
- **Comportamiento (Conduct)**: Estrategias de pricing, M&A de firmas y expansión geográfica.
- **Oportunidades (Opportunities)**: Nichos desatendidos (mid-market, ESG para PYMES, etc.).
- **Debilidades (Disadvantages)**: Áreas donde {my_company} es objetivamente inferior (marca, equipo, tecnología).
- **Impacto (Impact)**: Proyección a 12 meses si no se toman medidas.

#### 5. Plan de Acción Estratégico
- **Paso 1 (Inmediato - 30 días)**: Acción táctica rápida.
- **Paso 2 (Medio Plazo - 6 meses)**: Desarrollo de capacidad o alianza.
- **Paso 3 (Largo Plazo - 1 año)**: Cambio de posicionamiento.

**Formato:** Markdown profesional. Usa negritas, listas y tablas.
**Idioma:** Español de Negocios (Profesional y Directo).
"""

BATCH_ANALYSIS_PROMPT = """
Analiza los siguientes fragmentos (snippets) sobre la empresa "{company}" del sector de consultoría financiera.
Determina:
1. El SENTIMIENTO GENERAL (Positivo, Negativo, Neutro, Mixto).
2. El TEMA DOMINANTE más mencionado (Auditoría, ESG, Due Diligence, ERP, Regulatorio, Valoraciones, Riesgos, General).

Fragmentos:
{text}

Responde EXACTAMENTE en este formato (sin nada más):
SENTIMIENTO: [valor] | TEMA: [valor]
"""
