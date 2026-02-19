SENTIMENT_ANALYSIS_PROMPT = """
Analiza el sentimiento del siguiente texto sobre una empresa de externalización de procesos financieros (BPO).
Clasifica como: Positivo, Negativo, Neutro o Mixto.
Responde SOLO con la clasificación, sin explicación.

Texto: {text}
"""

TOPIC_CLASSIFICATION_PROMPT = """
Clasifica el tema dominante del siguiente texto sobre externalización financiera / BPO.
Categorías posibles: Externalización Contable, Fiscalidad/SII, Digitalización, Coordinación Internacional, Loan Staff, Cuentas Anuales, General.
Responde SOLO con la categoría, sin explicación.

Texto: {text}
"""

CODI_REPORT_PROMPT = """
Eres un Consultor Estratégico Senior especializado en Externalización de Procesos Financieros (BPO).
Tu objetivo es generar un **INFORME ESTRATÉGICO EXHAUSTIVO Y DETALLADO** para **{my_company}**.
**Fecha del Informe**: {date}

**⚠️ ADVERTENCIA:** El usuario ha solicitado explícitamente un informe LARGO y PROFUNDO.
- NO hagas resúmenes breves.
- NO uses frases genéricas.
- Si falta información, infiérela basada en tu conocimiento del mercado de BPO financiero en España, pero márcala como "Estimación de mercado".

### Contexto de Cliente ({my_company}):
- **Enfoque Estratégico**: Externalización de Procesos Financieros (BPO contable, fiscal, digitalización).
- **Catálogo de Servicios Prioritario**:
  1. **Externalización contable y/o fiscal** completa.
  2. **Revisión de cierre**, cuentas anuales y libros oficiales.
  3. **Servicios Gestión SII (BPO)** — Fiscalidad puntual y trámites Agencia Tributaria.
  4. **Digitalización de facturas** de proveedores y automatización documental.
  5. **Coordinación internacional** — Multipaís, multi-normativa.
  6. **Remedy, Interim y Loan Staff** — Personal especializado en períodos críticos.
  7. **Externalización de procesos contables específicos BPO** — Cuentas a pagar, tesorería, conciliaciones.

### Datos de Inteligencia Competitiva (Input Real):
{data}

---

### ESTRUCTURA OBLIGATORIA DEL INFORME:

#### 1. Resumen Ejecutivo (Executive Summary)
- Visión general del estado competitivo de {my_company} vs. el mercado de BPO financiero en España.
- Principales 3 alertas rojas (amenazas) y 3 luces verdes (oportunidades).

#### 2. Comparativa de Servicios y Posicionamiento (Gap Analysis)
**Instrucción Clave:** Genera una tabla comparativa detallada.

| Servicio | {my_company} | Competencia (Líder) | Gap / Diferencia |
| :--- | :--- | :--- | :--- |
| **Externalización Contable** | (Capacidad) | (Ej. Auxadi, TMF) | ¿Automatización? |
| **Gestión SII / Fiscal** | (Capacidad) | (Ej. Auren) | ¿Cobertura? |
| **Digitalización Facturas** | (Capacidad) | (Ej. Tech players) | ¿Tecnología? |
| **Coordinación Internacional** | (Capacidad) | (Ej. TMF, Vistra) | ¿Presencia global? |
| **Loan Staff / Interim** | (Capacidad) | (Ej. Robert Walters, Michael Page) | ¿Pool talento? |

#### 3. Análisis de Tendencias del Mercado BPO
- **Automatización e IA**: RPA, IA en contabilidad, OCR para facturas.
- **Regulación**: Cambios en SII, Verifactu, factura electrónica obligatoria.
- **Nearshoring vs Offshore**: Tendencias de deslocalización financiera.
- **Consolidación**: M&A en el sector BPO financiero.

#### 4. Radar CODI (Extendido)
- **Comportamiento (Conduct)**: Estrategias de pricing, modelos de servicio (por transacción vs. fijo).
- **Oportunidades (Opportunities)**: Nichos desatendidos (PYMES, startups, multinacionales mid-market).
- **Debilidades (Disadvantages)**: Áreas donde {my_company} es objetivamente inferior.
- **Impacto (Impact)**: Proyección a 12 meses si no se toman medidas.

#### 5. Plan de Acción Estratégico
- **Paso 1 (Inmediato - 30 días)**: Acción táctica rápida.
- **Paso 2 (Medio Plazo - 6 meses)**: Desarrollo de capacidad o alianza tecnológica.
- **Paso 3 (Largo Plazo - 1 año)**: Cambio de posicionamiento.

**Formato:** Markdown profesional. Usa negritas, listas y tablas.
**Idioma:** Español de Negocios (Profesional y Directo).
"""

BATCH_ANALYSIS_PROMPT = """
Analiza los siguientes fragmentos (snippets) sobre la empresa "{company}" del sector de externalización financiera / BPO.
Determina:
1. El SENTIMIENTO GENERAL (Positivo, Negativo, Neutro, Mixto).
2. El TEMA DOMINANTE más mencionado (Externalización Contable, Fiscalidad/SII, Digitalización, Coordinación Internacional, Loan Staff, Cuentas Anuales, General).

Fragmentos:
{text}

Responde EXACTAMENTE en este formato (sin nada más):
SENTIMIENTO: [valor] | TEMA: [valor]
"""
