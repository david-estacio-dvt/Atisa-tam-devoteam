# Prompts for HR Competitive Analysis Agent

SENTIMENT_ANALYSIS_PROMPT = """
Analiza el sentimiento del siguiente texto relacionado con una empresa o servicio del sector RRHH.
Clasifícalo ESTRICTAMENTE como una de estas tres categorías: "Positivo", "Negativo", "Neutral".

Contexto:
- "Positivo": Elogia servicios, buen ambiente laboral, nóminas eficientes o innovación.
- "Negativo": Quejas sobre retrasos, mala gestión, soporte deficiente o costes ocultos.
- "Neutral": Noticias factuales, ofertas de trabajo sin valoración cualitativa o actualizaciones generales del mercado.

Texto: "{text}"

Sentimiento:
"""

TOPIC_CLASSIFICATION_PROMPT = """
Clasifica el siguiente fragmento de texto en uno de los temas relevantes de RRHH:
- "Externalización de Nómina"
- "Consultoría RRHH"
- "Gestión del Talento"
- "Legal/Cumplimiento"
- "General/Otros"

Texto: "{text}"

Tema:
"""

CODI_REPORT_PROMPT = """
Eres un Consultor Estratégico Senior de RRHH (Nivel MBB - McKinsey/Bain/BCG).
Tu objetivo es generar un **INFORME ESTRATÉGICO EXHAUSTIVO Y DETALLADO** para **{my_company}**.
**Fecha del Informe**: {date}

**⚠️ ADVERTENCIA:** El usuario ha solicitado explícitamente un informe LARGO y PROFUNDO.
- NO hagas resúmenes breves.
- NO uses frases genéricas.
- Si falta información, infiérela basada en tu conocimiento del mercado de RRHH en España, pero márcala como "Estimación de mercado".

### Contexto de Cliente ({my_company}):
- **Enfoque Estratégico**: Consultoría de Talento y Transformación Organizacional (NO gestión de nómina pura).
- **Catálogo de Servicios Prioritario**:
  1. **Bienestar Corporativo** (Wellbeing).
  2. **Reingeniería de Procesos** y Eficiencia Organizacional.
  3. **Compensación y Beneficios** (Estudios retributivos, Valoración de puestos).
  4. **Experiencia del Empleado** (EVP, Clima, Comunicación interna).
  5. **Gestión del Talento** (Planes de carrera, Evaluación desempeño, Competencias).
  6. **Liderazgo y Diversidad** (Convivencia intergeneracional, Estilos de liderazgo).

### Datos de Inteligencia Competitiva (Input Real):
{data}

---

### ESTRUCTURA OBLIGATORIA DEL INFORME:

#### 1. Resumen Ejecutivo (Executive Summary)
- Visión general del estado competitivo de {my_company} vs. el mercado en 2026.
- Principales 3 alertas rojas (amenazas) y 3 luces verdes (oportunidades).

#### 2. Comparativa de Producto y Precios (Gap Analysis)
**Instrucción Clave:** Genera una tabla comparativa detallada. Si no tienes el dato exacto, usa "N/D" o estima según estándar del sector.

| Característica | {my_company} | Competencia (Líder Detectado) | Gap / Diferencia |
| :--- | :--- | :--- | :--- |
| **Modelo de Precios** | (Tu conocimiento) | (Ej. 3-5€/empleado/mes) | (Análisis de competitividad) |
| **Plataforma IA** | (Tu conocimiento) | (Ej. Automatización, Chatbot) | ¿Nos falta tecnología? |
| **Módulos Talento**  | (Tu conocimiento) | (Ej. Performance, ATS) | ¿Cobertura completa? |
| **Servicio Cliente** | Personalizado | (Ej. Ticket/Bot) | ¿Nuestra ventaja? |

#### 3. Análisis de Tendencias: Cultura y Talento
- Analiza qué competidores están liderando la narrativa de "Bienestar", "Flexibilidad" y "Retribución".
- ¿Quién está ganando la batalla por la reputación de marca empleadora?

#### 4. Radar CODI (Extendido)
- **Comportamiento (Conduct)**: Estrategias de marketing y ventas agresivas detectadas en los rivales.
- **Oportunidades (Opportunities)**: Nichos de mercado o dolores del cliente que nadie está resolviendo bien.
- **Debilidades (Disadvantages)**: Áreas donde {my_company} es objetivamente inferior (tecnología, marca, precio).
- **Impacto (Impact)**: Proyección a 12 meses si no se toman medidas.

#### 5. Plan de Acción Estratégico
- **Paso 1 (Inmediato - 30 días)**: Acción táctica rápida.
- **Paso 2 (Medio Plazo - 6 meses)**: Desarrollo de producto o alianza.
- **Paso 3 (Largo Plazo - 1 año)**: Cambio de posicionamiento.

**Formato:** Markdown profesional. Usa negritas, listas y tablas.
**Idioma:** Español de Negocios (Profesional y Directo).
"""

BATCH_ANALYSIS_PROMPT = """
Analiza los siguientes fragmentos de noticias y opiniones sobre la empresa {company}:

{text}

Basado en TODO el texto anterior, determina:
1. El Sentimiento General (Positivo, Negativo, Neutro).
2. El Tema Dominante (ej. Innovación, Precios, Servicio, Despidos, Legal).

Responde ESTRICTAMENTE en este formato:
SENTIMIENTO: [Resultado] | TEMA: [Resultado]
"""
