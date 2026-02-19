SENTIMENT_ANALYSIS_PROMPT = """
Analiza el sentimiento del siguiente texto sobre una empresa de externalización de nómina y administración de personal.
Clasifica como: Positivo, Negativo, Neutro o Mixto.
Responde SOLO con la clasificación, sin explicación.

Texto: {text}
"""

TOPIC_CLASSIFICATION_PROMPT = """
Clasifica el tema dominante del siguiente texto sobre nómina y administración de personal.
Categorías posibles: Nómina, Portal/App, Administración Personal, Laboral, Fichaje/Control Horario, Turnos, Retribución Flexible, RPA, General.
Responde SOLO con la categoría, sin explicación.

Texto: {text}
"""

CODI_REPORT_PROMPT = """
Eres un Consultor Estratégico Senior especializado en Externalización de Nómina y Administración de Personal.
Tu objetivo es generar un **INFORME ESTRATÉGICO EXHAUSTIVO Y DETALLADO** para **{my_company}**.
**Fecha del Informe**: {date}

**⚠️ ADVERTENCIA:** El usuario ha solicitado explícitamente un informe LARGO y PROFUNDO.
- NO hagas resúmenes breves.
- NO uses frases genéricas.
- Si falta información, infiérela basada en tu conocimiento del mercado de nómina y HR tech en España, pero márcala como "Estimación de mercado".

### Contexto de Cliente ({my_company}):
- **Enfoque Estratégico**: Externalización de Nómina y Administración de Personal.
- **Catálogo de Servicios Prioritario**:
  1. **Gestión integral de nómina** (core business) — Cálculo, generación y presentación.
  2. **Portal comunicación / App** — Portal del empleado y aplicación móvil.
  3. **Administración de personal** — Altas, bajas, contratos, documentación.
  4. **Asesoramiento laboral** — Consultoría normativa, convenios colectivos.
  5. **Control de tiempos y fichaje** — Registro horario, cumplimiento legal.
  6. **Planificación de turnos** — Cuadrantes, rotaciones, coberturas.
  7. **Retribución flexible** — Planes de beneficios personalizables.
  8. **RPAs** — Automatización de procesos repetitivos en nómina y RRHH.

### Datos de Inteligencia Competitiva (Input Real):
{data}

---

### ESTRUCTURA OBLIGATORIA DEL INFORME:

#### 1. Resumen Ejecutivo (Executive Summary)
- Visión general del estado competitivo de {my_company} vs. el mercado de nómina/payroll en España.
- Principales 3 alertas rojas (amenazas) y 3 luces verdes (oportunidades).

#### 2. Comparativa de Servicios y Posicionamiento (Gap Analysis)

| Servicio | {my_company} | Competencia (Líder) | Gap / Diferencia |
| :--- | :--- | :--- | :--- |
| **Nómina Core** | (Capacidad) | (Ej. Personio, PayFit) | ¿Automatización? |
| **Portal/App Empleado** | (Capacidad) | (Ej. Factorial, Kenjo) | ¿UX/Funcionalidades? |
| **Control Horario** | (Capacidad) | (Ej. Sesame, Woffu) | ¿Integración? |
| **Planificación Turnos** | (Capacidad) | (Ej. Shiftbase) | ¿IA predictiva? |
| **Retribución Flexible** | (Capacidad) | (Ej. Cobee, Flexoh) | ¿Variedad beneficios? |
| **RPA** | (Capacidad) | (Ej. UiPath, Automation Anywhere) | ¿Madurez? |

#### 3. Análisis de Tendencias del Mercado
- **HR Tech y SaaS**: Consolidación, verticales, pricing freemium vs. enterprise.
- **Regulación**: Registro horario obligatorio, teletrabajo, transparencia salarial.
- **IA en Nómina**: Automatización, detección de errores, chatbots para empleados.
- **Employee Experience**: Apps, self-service, engagement.

#### 4. Radar CODI (Extendido)
- **Comportamiento (Conduct)**: Estrategias de pricing, freemium, expansión.
- **Oportunidades (Opportunities)**: PYMES sin externalizar, internacionalización.
- **Debilidades (Disadvantages)**: Áreas donde {my_company} es inferior (app, UX, IA).
- **Impacto (Impact)**: Proyección a 12 meses.

#### 5. Plan de Acción Estratégico
- **Paso 1 (Inmediato - 30 días)**: Acción táctica rápida.
- **Paso 2 (Medio Plazo - 6 meses)**: Desarrollo tecnológico o alianza.
- **Paso 3 (Largo Plazo - 1 año)**: Cambio de posicionamiento.

**Formato:** Markdown profesional. Usa negritas, listas y tablas.
**Idioma:** Español de Negocios (Profesional y Directo).
"""

BATCH_ANALYSIS_PROMPT = """
Analiza los siguientes fragmentos (snippets) sobre la empresa "{company}" del sector de nómina y administración de personal.
Determina:
1. El SENTIMIENTO GENERAL (Positivo, Negativo, Neutro, Mixto).
2. El TEMA DOMINANTE más mencionado (Nómina, Portal/App, Administración Personal, Laboral, Fichaje/Control Horario, Turnos, Retribución Flexible, RPA, General).

Fragmentos:
{text}

Responde EXACTAMENTE en este formato (sin nada más):
SENTIMIENTO: [valor] | TEMA: [valor]
"""
