# AI PROCESS

## 1. Introducción
Este documento registra el uso de herramientas de Inteligencia Artificial durante el análisis, diseño, implementación, pruebas y validación de la aplicación Trycore EVM.

El objetivo es proporcionar trazabilidad del proceso de desarrollo, incluyendo las instrucciones originales suministradas a las herramientas, los resultados obtenidos, las decisiones técnicas, las verificaciones realizadas y las situaciones en las que fue necesario cuestionar o ajustar las propuestas de IA.

La aplicación implementa la gestión de proyectos y actividades mediante una arquitectura fullstack con React, FastAPI, SQLAlchemy y PostgreSQL, incorporando un motor independiente para calcular indicadores Earned Value Management (EVM).

La IA se utilizó como apoyo para el análisis y la implementación. Los resultados se contrastaron mediante revisión técnica, pruebas automatizadas, validaciones matemáticas y comprobaciones funcionales manuales.

## 2. Herramientas y metodología
### 2.1 Herramientas utilizadas
Las herramientas principales que se utilizaron para desarrollar el proyecto fueron:

- *ChatGPT:* Análisis funcional, fundamentos EVM, evaluación de decisiones técnicas, planificación y revisión del desarrollo.
- *Codex en Visual Studio Code:* Inspección del repositorio, generación y modificación de código, ejecución de pruebas y validación de componentes.
- *Visual Studio Code:* Edición, inspección de archivos y ejecución de comandos.
- *Git y GitHub:* Control de versiones, seguimiento de funcionalidades y Pull Requests mediante Gitflow.
- *pytest, pytest-cov, Vitest y Ruff:* Pruebas automatizadas, cobertura y análisis estático.
- *Swagger UI:* Validación manual de endpoints REST.

### Metodología
El desarrollo se organizó mediante ramas Gitflow, separando las funcionalidades en etapas incrementales:

1. Configuración inicial del proyecto.
2. Implementación del motor de cálculo EVM.
3. Modelado y persistencia PostgreSQL.
4. Implementación de la API REST.
5. Desarrollo del dashboard React.
6. Integración, validación y preparación de la entrega.

Cada etapa siguió un proceso de análisis de requisitos, instrucciones a la IA, revisión del código generado, ejecución de pruebas y validación antes de su integración.

Se priorizó la separación de responsabilidades, la reutilización del motor EVM, la precisión decimal y la reducción de complejidad arquitectónica innecesaria.

## 3. Historial cronológico

### Interacción 001 - Instrucciones iniciales del proyecto
Fecha: 2026-11-17 (fecha orientativa, verificar en historial)
Herramienta: ChatGPT

Prompt:
Trycore — AI/RPA Technical Challenge
Actúa como mi mentor técnico, arquitecto de software y colaborador de desarrollo para resolver la prueba técnica de Trycore, cuyo documento oficial adjunto será mi fuente de requisitos.

Objetivo
Construir y entregar una aplicación fullstack de gestión de proyectos y Earned Value Management (EVM), cumpliendo los requisitos funcionales, técnicos, de testing, Gitflow y documentación establecidos por Trycore (PDF adjunto).

Fecha límite: 19 de noviembre de 2026, antes de las 7:00 a. m. (Colombia).

Mi nivel de experiencia

Soy Ingeniero de Sistemas con más de seis años de experiencia en Application Support, automatización, RPA, Python, SQL, APIs y operaciones TI. Tengo un Máster en Inteligencia Artificial.

 Metodología

1. Divide el proyecto en fases pequeñas y verificables.
2. Explica los conceptos técnicos antes de implementarlos.
3. Propón alternativas y sus ventajas, riesgos y limitaciones.
4. No tomes decisiones arquitectónicas importantes por mí.
5. Trabaja con Python, FastAPI, PostgreSQL y React, salvo que decidamos justificadamente otra cosa.
6. Prioriza una aplicación funcional, mantenible, comprobable y sencilla.
7. No agregues funcionalidades fuera de los requisitos sin justificación.
8. Utiliza Codex para implementar tareas específicas cuando resulte conveniente.
9. Después de cada implementación, explica qué se creó, cómo funciona y cómo verificarlo.
10. No declares funcionalidades completas sin pruebas o evidencia.

 Requisitos de evaluación

Cumplir el documento original: EVM, CRUD de proyectos y actividades, frontend, persistencia, pruebas unitarias, cobertura mínima del 80% en lógica de negocio, tests de integración, código limpio, Gitflow y documentación.

 Trazabilidad obligatoria de IA

Debo mantener AI_PROCESS.md desde el inicio.

Registra los prompts enviados a ChatGPT y Codex de manera literal y cronológica. No los reconstruyas ni los parafrasees.

Ayúdame a identificar decisiones reales donde acepte o rechace recomendaciones de IA, validar los cálculos manualmente y documentar una decisión de arquitectura que yo haya tomado.

Nunca inventes evidencia, resultados de pruebas o intervenciones humanas.

 Forma de colaboración

Sé crítico, práctico, progresivo y pedagógico. Evita explicaciones innecesarias, pero no omitas conceptos que necesito comprender para defender técnicamente el proyecto.

Antes de continuar a una fase nueva, ayúdame a verificar que la anterior funciona.

 Entregables finales
- Repositorio GitHub con historial Gitflow.
- README.md e instrucciones de instalación.
- Script de inicialización de base de datos.
- AI_PROCESS.md completo.
- Aplicación funcional con pruebas.
- Video explicativo de máximo 10 minutos.

Mi prioridad es entregar una solución que pueda explicar y defender honestamente, demostrando criterio ingenieril y uso responsable de IA.

### 1.1
Analiza los requerimientos del desafío técnico de Trycore y propón una arquitectura fullstack utilizando Python, FastAPI, PostgreSQL y React.

Considera los siguientes criterios:

1. Separación de responsabilidades entre controladores, servicios, modelos y acceso a datos.
2. Arquitectura modular, escalable y mantenible, evitando complejidad innecesaria.
3. Implementación de operaciones CRUD para proyectos y actividades.
4. Cálculo de indicadores EVM mediante una capa de lógica de negocio independiente.
5. Pruebas unitarias e integración, con cobertura mínima del 80% de la lógica de negocio.
6. Documentación automática de API mediante OpenAPI/Swagger.
7. Organización del repositorio siguiendo Gitflow.

Antes de implementar, presenta:
- La estructura propuesta del proyecto.
- Las responsabilidades de cada componente.
- Las principales decisiones arquitectónicas y sus alternativas.
- Las dependencias necesarias.
- Un plan de implementación por fases, con criterios de aceptación.

No generes ni modifiques archivos todavía. Primero revisaré y validaré la propuesta arquitectónica.

### Interacción 002 - Consulta sobre CPI y SPI
Fecha: 2026-11-17 (fecha orientativa, verificar en historial)
Herramienta: ChatGPT

Prompt:

Quiero que me ayudes a entender con mayor claridad el CPI SPI, como se calculan, cuales son los casos, como deberia comportarse, que significa, que determina, etc.
Y como se calcula correctamente.


### Interacción 003 - Fundamentos y análisis EVM
Fecha: 2026-11-17 (fecha orientativa, verificar en historial)
Herramienta: ChatGPT

Prompt:

Voy a iniciar el desarrollo del desafío técnico de Trycore, utilizando el PDF adjunto como fuente principal de requisitos.

FASE 1 — Análisis del problema y fundamentos de Earned Value Management (EVM)

Antes de comenzar la implementación, necesito establecer una comprensión clara del problema de negocio, los indicadores requeridos y las reglas que deberá implementar la aplicación.

Desarrolla lo siguiente:

1. Análisis funcional: explica el problema empresarial que busca resolver Trycore, los usuarios de la aplicación y las funcionalidades obligatorias.
2. Fundamentos EVM: explica qué es Earned Value Management, cuál es su propósito y cómo se aplica al control de proyectos.
3. Indicadores: explica individualmente BAC, PV, EV, AC, CV, SV, CPI, SPI, EAC y VAC. Incluye fórmulas, interpretación de resultados y ejemplos numéricos.
4. Caso práctico: construye un ejemplo empresarial con un proyecto de tres actividades, cada una con presupuesto, avance planificado, avance real y costo ejecutado. Calcula los indicadores individuales y consolidados.
5. Validación matemática: explica cómo verificar manualmente los resultados, especialmente los indicadores consolidados del proyecto.
6. Casos borde: analiza escenarios como AC = 0, PV = 0, ausencia de actividades, avance real del 0%, presupuesto igual a cero y divisiones indefinidas. Propón alternativas razonables para manejarlos, sin tomar decisiones definitivas todavía.
7. Criterios de aceptación: identifica qué resultados y comportamientos debo verificar mediante pruebas automatizadas.

Lineamientos de trabajo:
- Utiliza como referencia prioritaria las fórmulas y requisitos del documento oficial.
- Distingue entre requisitos explícitos y decisiones de diseño propuestas.
- Explica el razonamiento detrás de los cálculos.
- No implementes código todavía.
- No avances a la arquitectura hasta que validemos esta primera fase.

El objetivo es comprender y validar el modelo EVM antes de convertirlo en lógica de negocio.

Recuerda que este prompt y los siguientes deben conservarse textualmente en el registro cronológico de uso de IA para AI_PROCESS.md.


### Interacción 004 - Validación matemática EVM
Fecha: 2026-11-17 (fecha orientativa, verificar en historial)
Herramienta: ChatGPT

Prompt adaptado:

FASE 1 — Validación final de EVM

Antes de avanzar a la arquitectura, quiero validar el modelo matemático que implementaré.

1. Construye un caso de prueba de tres actividades con distintos presupuestos, avances planificados, avances reales y costos ejecutados.
2. Presenta los indicadores individuales y consolidados, mostrando los cálculos intermedios.
3. Demuestra por qué el CPI y el SPI consolidados deben calcularse a partir de los valores agregados y no mediante el promedio simple de los índices individuales.
4. Analiza las divisiones por cero en CPI, SPI y EAC. Compara las alternativas de respuesta de la API (null, cero, error o estado no calculable), indicando sus implicaciones.
5. Propón casos de prueba unitarios con entradas y resultados numéricos esperados.
6. Identifica qué decisiones de diseño siguen pendientes de aprobación.

No implementes código ni avances todavía a la arquitectura.

El objetivo es obtener una referencia matemática verificable que pueda utilizar posteriormente para validar los cálculos del backend.

### Interacción 005 - Diseño de arquitectura
Fecha: 2026-11-17 
Herramienta: ChatGPT

Prompt adaptado:

FASE 2 — Diseño de arquitectura y planificación técnica

He completado la revisión conceptual de Earned Value Management (EVM). Continúa con el diseño técnico del desafío de Trycore, utilizando el PDF adjunto como referencia principal.

Antes de implementar código, desarrolla lo siguiente:

1. Arquitectura fullstack: explica cómo se relacionarán el frontend, backend, API REST, capa de negocio y base de datos. Incluye un diagrama de arquitectura.
2. Stack tecnológico: evalúa Python + FastAPI, React + Vite y PostgreSQL. Explica por qué serían adecuados y compara alternativas más sencillas cuando corresponda.
3. Arquitectura backend: propón una estructura modular con separación de responsabilidades entre routers, schemas, models, services y acceso a datos. Explica el propósito de cada componente.
4. Modelo de datos: diseña las entidades Project y Activity, sus atributos, tipos de datos, relaciones y restricciones. Identifica qué información debe almacenarse y qué indicadores deben calcularse dinámicamente.
5. Diseño de API REST: propone los endpoints necesarios para cumplir todas las operaciones CRUD y consultar indicadores EVM individuales y consolidados. Incluye métodos HTTP, rutas, ejemplos JSON y códigos de respuesta.
6. Motor de cálculo EVM: define dónde debe ubicarse la lógica de negocio, cómo reutilizarla y cómo garantizar que los indicadores consolidados se calculen correctamente. Identifica las decisiones pendientes sobre casos borde.
7. Frontend: identifica las páginas, componentes, formularios, tablas, indicadores y gráficas necesarios para cumplir el desafío sin agregar complejidad innecesaria.
8. Testing: propone la estrategia de pruebas unitarias e integración, considerando el requisito de cobertura mínima del 80% de la lógica de negocio.
9. Gitflow: explica cómo organizaremos el repositorio desde el inicio utilizando main, develop, feature/, release/ y Pull Requests.
10. Plan de implementación: establece el orden de desarrollo, dependencias entre componentes y criterios de aceptación para cada fase.

Condiciones:
- Prioriza simplicidad, mantenibilidad y cumplimiento de los requisitos.
- Diferencia requisitos obligatorios de decisiones arquitectónicas propuestas.
- Identifica alternativas y trade-offs relevantes.
- No implementes código ni crees archivos todavía.
- No tomes decisiones arquitectónicas definitivas sin presentar primero sus alternativas.

El objetivo es disponer de un diseño técnico claro, verificable y adecuado para comenzar la implementación con Codex y VS Code.

### Interacción 006 - Arquitectura definitiva y entorno
Fecha: 2026-11-17
Herramienta: ChatGPT

Prompt:

FASE 2.1 — Arquitectura definitiva y preparación del repositorio

Tras revisar la propuesta arquitectónica, continuaremos con una implementación sencilla, modular y orientada a cumplir los requisitos de Trycore.

Trabajaré con Python, FastAPI, React + Vite, PostgreSQL, SQLAlchemy síncrono y pytest.

Utilizaré una arquitectura de tres capas principales: Router → Service → SQLAlchemy, manteniendo el motor EVM independiente de la persistencia.

Para el motor EVM, utilizaré los indicadores consolidados calculados sobre los valores agregados, conservando precisión decimal. Los indicadores matemáticamente indefinidos se representarán mediante null y un estado explicativo.

Los indicadores EVM se calcularán dinámicamente, sin persistir los valores derivados.

Para esta primera versión utilizaré un script SQL de inicialización y evitaremos funcionalidades adicionales que no estén justificadas por los requisitos.

Necesito preparar el entorno de desarrollo y comenzar la implementación con Codex.

Desarrolla lo siguiente:

1. Propón la estructura definitiva de carpetas y archivos, explicando brevemente su responsabilidad.
2. Identifica las herramientas que debo tener instaladas en Windows para trabajar con Python, FastAPI, PostgreSQL, React, Git y Codex desde VS Code.
3. Explica cómo crear correctamente el repositorio GitHub y configurar las ramas main y develop.
4. Define las primeras ramas feature/ que utilizaré y el orden en que se integrarán mediante Pull Requests.
5. Identifica las dependencias mínimas del backend y frontend.
6. Define los criterios de aceptación de mi primera funcionalidad: el motor de cálculo EVM y sus pruebas unitarias.
7. Propón un procedimiento de trabajo con Codex donde cada cambio pueda revisarse, probarse y confirmarse antes de integrarlo.

Restricciones:
- No implementes todavía el backend ni el frontend.
- No generes código de negocio.
- Prioriza instrucciones concretas y reproducibles para Windows y VS Code.
- Explica cómo verificar que el entorno quedó correctamente configurado.
- Mantén actualizado el plan para documentar el proceso en AI_PROCESS.md.

Al finalizar, debo estar preparados para crear el repositorio y comenzar la primera implementación de manera controlada.

### Interacción 007 - Inspección y plan inicial
Fecha: 2026-11-17 
Herramienta: Codex

Prompt adaptado:

Estoy desarrollando una aplicación fullstack para gestión de proyectos y análisis Earned Value Management (EVM), siguiendo el desafío técnico de Trycore.

La arquitectura aprobada utiliza Python, FastAPI, React con Vite, PostgreSQL y SQLAlchemy síncrono. El backend seguirá una separación Router → Service → SQLAlchemy, con un motor EVM independiente.

Tarea: preparar la estructura inicial del repositorio.

1. Inspecciona los archivos existentes.
2. Propón una estructura mínima para backend, frontend, pruebas, configuración y documentación.
3. Identifica las dependencias necesarias.
4. Define las configuraciones básicas para pytest y Ruff.
5. Comprueba que la estructura sea compatible con Gitflow y con el posterior desarrollo incremental.

No implementes funcionalidades de negocio todavía.

Antes de modificar archivos, presenta el plan concreto y espera mi aprobación. No realices commits ni Pull Requests.

Prioriza simplicidad, mantenibilidad y configuración reproducible en Windows.

### Interacción 008 - Configuración inicial del repositorio
Fecha: 2026-11-17 
Herramienta: Codex

Prompt:

He revisado la propuesta de configuración inicial. Apruebo la arquitectura general del monorepositorio, con los siguientes ajustes para mantener coherencia con las decisiones técnicas previamente establecidas y reducir complejidad innecesaria.

Ajustes aprobados:

1. Utilizar React + Vite con JavaScript y JSX, en lugar de TypeScript.
2. Utilizar PostgreSQL instalado localmente en Windows, sin Docker Compose.
3. Utilizar un script database/init_db.sql para inicialización de la base de datos, sin incorporar Alembic.
4. Simplificar las dependencias de Python mediante requirements.txt y configuración de pytest y Ruff en pyproject.toml.
5. Mantener FastAPI, SQLAlchemy síncrono, Pydantic, pytest, pytest-cov y Ruff.
6. Conservar .editorconfig y .gitattributes para consistencia de formato.
7. Mantener las responsabilidades Router → Service → SQLAlchemy, con el motor EVM como módulo independiente.
8. Preparar README.md, AI_PROCESS.md y docs/architecture.md, sin generar documentación ficticia del desarrollo.

Tarea:

Implementa exclusivamente la configuración inicial correspondiente a feature/project-setup.

Incluye:
- Estructura mínima de carpetas de backend y frontend.
- Aplicación FastAPI básica con endpoint de comprobación de salud.
- Swagger UI configurado en /api-docs.
- Frontend React + Vite con una pantalla inicial mínima.
- Configuración de pytest, pytest-cov y Ruff.
- Archivos .env.example y .gitignore adecuados.
- Dependencias necesarias.
- Instrucciones reproducibles de ejecución local en Windows.

Restricciones:
- No implementes todavía entidades Project/Activity.
- No implementes operaciones CRUD ni fórmulas EVM.
- No crees todavía las tablas de base de datos.
- No agregues autenticación, Docker, Alembic ni funcionalidades adicionales.
- No realices commits ni Pull Requests.
- No inventes resultados de pruebas ni documentación del proceso de IA.
- Mantén todos los cambios en la rama feature/project-setup.

Al finalizar, ejecuta las verificaciones disponibles y presenta un resumen de archivos creados, comandos ejecutados, resultados y posibles errores para revisión antes de realizar el primer commit.

### Interacción 009 - Auditoría del project setup
Fecha: 2026-11-17
Herramienta: Codex

Prompt:

Realiza una auditoría final de la configuración inicial de feature/project-setup antes del primer commit.

1. Ejecuta pytest y Ruff e informa el número exacto de pruebas superadas y cualquier error o advertencia.
2. Revisa las cinco vulnerabilidades reportadas por npm audit. Identifica las dependencias afectadas, su impacto real y las posibles soluciones sin aplicar actualizaciones mayores automáticamente.
3. Verifica que el backend exponga correctamente Swagger UI en /api-docs y que el endpoint de salud responda HTTP 200.
4. Comprueba que el frontend compile y que ESLint finalice correctamente.
5. Revisa .gitignore para asegurar que excluya .venv, node_modules, .env, credenciales y archivos generados.
6. Revisa AI_PROCESS.md e identifica cualquier prompt, decisión o resultado que no esté respaldado por el historial real de trabajo. No inventes ni modifiques registros históricos.
7. Comprueba que los archivos creados correspondan exclusivamente a la configuración inicial, sin funcionalidades de negocio.

No realices commits, pushes ni Pull Requests.

Entrega un informe breve con los comandos ejecutados, resultados, errores y recomendaciones. Si detectas problemas, propone primero las correcciones sin aplicarlas automáticamente.

### Interacción 010 - Correcciones de la configuración
Fecha: 2026-11-18
Herramienta: Codex

Prompt:

He revisado los resultados de la auditoría de feature/project-setup.

Apruebo las siguientes correcciones puntuales antes del primer commit:

1. Corregir los caracteres dañados en frontend/src/App.jsx, asegurando codificación UTF-8 y textos correctamente escritos en español.
2. Ampliar .gitignore con reglas razonables para excluir archivos sensibles, credenciales, claves privadas y artefactos locales, sin excluir archivos necesarios del proyecto.
3. Mantener Oxlint como herramienta de linting del frontend. No instalar ESLint, ya que Oxlint cumple el propósito de análisis estático requerido para esta etapa.
4. Mantener las versiones actuales de dependencias. No ejecutar npm audit fix --force ni aplicar cambios mayores automáticos.
5. Registrar las vulnerabilidades conocidas y su alcance de manera concisa en la documentación técnica correspondiente, sin afirmar que están corregidas.

Después de aplicar estos cambios:
- Ejecuta nuevamente las pruebas de pytest.
- Ejecuta Ruff y Oxlint.
- Comprueba que React compile correctamente.
- Verifica git diff --check.
- Confirma que el repositorio sigue en feature/project-setup.
- Revisa que no se hayan incluido credenciales o archivos generados.

No implementes funcionalidades de negocio y no realices commits, pushes ni Pull Requests todavía.

Entrega un resumen de los cambios efectuados y los resultados verificables para aprobar la integración.

### Interacción 011 - Implementación del motor EVM
Fecha: 2026-11-18
Herramienta: Codex

Prompt:

FASE 3 — Implementación del motor Earned Value Management (EVM)

Estoy trabajando en la rama feature/evm-engine del desafío técnico de Trycore.

Implementa el motor de cálculo EVM utilizando Python, manteniéndolo completamente independiente de FastAPI, SQLAlchemy y PostgreSQL.

 Requisitos funcionales

Cada actividad debe recibir:
- BAC: presupuesto total planificado.
- Planned Progress: porcentaje de avance planificado entre 0 y 100.
- Actual Progress: porcentaje de avance real entre 0 y 100.
- AC: costo real ejecutado.

Implementa los indicadores:
- PV = BAC × Planned Progress / 100
- EV = BAC × Actual Progress / 100
- CV = EV − AC
- SV = EV − PV
- CPI = EV / AC
- SPI = EV / PV
- EAC = BAC / CPI
- VAC = BAC − EAC

Incluye la interpretación de CPI y SPI: favorable, desfavorable o según lo previsto.

 Consolidación por proyecto

Implementa una función que reciba una colección de actividades y:

1. Calcule PV y EV por actividad.
2. Sume BAC, PV, EV y AC.
3. Calcule CV y SV consolidados.
4. Calcule CPI = EV total / AC total.
5. Calcule SPI = EV total / PV total.
6. Calcule EAC = BAC total / CPI total.
7. Calcule VAC = BAC total − EAC total.

No calcules CPI ni SPI consolidados mediante promedios de los índices individuales.

 Casos borde
- Cuando AC = 0, CPI debe ser None.
- Cuando PV = 0, SPI debe ser None.
- Cuando CPI = 0 o sea indefinido, EAC y VAC deben ser None.
- Cuando no existan actividades, los totales deben ser cero y los índices indefinidos.
- Permitir BAC = 0 y avances de 0%, siempre que las entradas no sean negativas.
- Rechazar porcentajes fuera del rango 0–100 y valores monetarios negativos.
- Diferenciar indicadores indefinidos de indicadores cuyo valor es cero.

 Requisitos técnicos
- Utiliza Decimal para cálculos monetarios y numéricos.
- Evita redondear valores intermedios.
- Separa las fórmulas del código de acceso a datos y de los endpoints.
- Diseña funciones pequeñas, reutilizables y con nombres descriptivos.
- Implementa pruebas unitarias con pytest para cálculos individuales, consolidados, interpretaciones y casos borde.
- Configura medición de cobertura para la lógica EVM.
- Mantén el código limpio y compatible con Ruff.

 Caso de validación obligatorio

Tres actividades, importes en millones:

| Actividad | BAC | Planificado | Real | AC |
|---|---:|---:|---:|---:|
| Análisis | 10 | 80% | 100% | 9 |
| Desarrollo | 20 | 60% | 40% | 12 |
| Pruebas | 30 | 50% | 50% | 16 |

Resultados consolidados esperados:
- BAC = 60
- PV = 35
- EV = 33
- AC = 37
- CV = -4
- SV = -2
- CPI = 33/37
- SPI = 33/35
- EAC = 740/11
- VAC = -80/11

Los tests deben validar estos resultados, las fórmulas individuales y los escenarios límite.

 Restricciones
- Modifica únicamente archivos relacionados con el motor EVM y sus pruebas.
- No implementes todavía CRUD, modelos de base de datos ni frontend.
- No realices commits, pushes ni Pull Requests.
- No modifiques el historial de prompts de AI_PROCESS.md.
- Ejecuta pytest, cobertura y Ruff.
- Informa cualquier diferencia matemática o ambigüedad encontrada antes de asumir comportamientos no definidos.

Al finalizar, entrega un resumen de archivos modificados, resultados de las pruebas, porcentaje de cobertura y posibles decisiones pendientes.

### Interacción 012 - Revisión técnica del motor EVM
Fecha: 2026-11-18
Herramienta: Codex

Prompt:

Realiza una revisión técnica final del motor EVM implementado en feature/evm-engine.

No modifiques archivos todavía.

1. Explica las funciones públicas implementadas en engine.py y las estructuras de datos de types.py.
2. Explica cómo se calculan los indicadores individuales y consolidados, identificando dónde se aplican las fórmulas.
3. Confirma con ejemplos cómo se gestionan AC = 0, PV = 0, CPI = 0 y proyectos sin actividades.
4. Verifica que los 74 tests comprueban resultados matemáticos y casos borde reales, y no únicamente tipos o existencia de respuestas.
5. Identifica posibles errores lógicos, duplicación de código o complejidad innecesaria.
6. Comprueba que None en Python puede representarse correctamente como null en una futura respuesta JSON.
7. Revisa cualquier implicación de la precisión decimal para la futura integración con FastAPI y PostgreSQL.

Entrega un informe conciso con hallazgos, riesgos y recomendaciones, distinguiendo problemas bloqueantes de mejoras opcionales.

No realices commits, pushes ni Pull Requests.

### Interacción 013 - Modelos y persistencia PostgreSQL
Fecha: 2026-11-18
Herramienta: Codex

Prompt:

FASE 4 — Implementación de persistencia y modelos PostgreSQL

Continúo el desarrollo del desafío técnico de Trycore en la rama feature/database-models.

El repositorio ya contiene la estructura FastAPI y un motor EVM independiente con pruebas unitarias. Implementa ahora la capa de persistencia utilizando PostgreSQL 17.12 instalado localmente en Windows y SQLAlchemy 2.x síncrono.

 1. Modelo de datos

Implementa dos entidades relacionadas:

Project
- id: identificador único, clave primaria.
- name: nombre obligatorio, no vacío, máximo 150 caracteres.
- description: texto opcional.

Activity
- id: identificador único, clave primaria.
- project_id: clave foránea obligatoria hacia Project.
- name: nombre obligatorio, no vacío, máximo 150 caracteres.
- bac: presupuesto total, NUMERIC(16,2), no negativo.
- planned_progress_pct: NUMERIC(5,2), entre 0 y 100.
- actual_progress_pct: NUMERIC(5,2), entre 0 y 100.
- actual_cost: NUMERIC(16,2), no negativo.

Un proyecto puede contener múltiples actividades. Cada actividad pertenece a un único proyecto.

Implementa eliminación en cascada de actividades cuando se elimine su proyecto, manteniendo coherencia entre SQLAlchemy y PostgreSQL.

 2. Conexión PostgreSQL
- Utiliza SQLAlchemy síncrono y psycopg.
- Configura el motor y las sesiones de base de datos.
- Obtén DATABASE_URL de variables de entorno.
- No incluyas credenciales reales en el código.
- Conserva un archivo .env.example con valores ficticios.
- Evita conexiones obligatorias durante la importación de FastAPI.
- No agregues Docker, Alembic ni una capa Repository adicional.

 3. Inicialización

Implementa database/init_db.sql con la creación de las tablas, claves, relaciones y restricciones.

El script debe ser reproducible e idempotente cuando sea razonable, sin eliminar datos existentes.

Asegura que los modelos SQLAlchemy y el esquema SQL sean equivalentes.

 4. Precisión y validación
- Utiliza Decimal y Numeric(..., asdecimal=True).
- Evita conversiones innecesarias a float.
- Los importes monetarios deben admitir dos decimales.
- Los porcentajes deben estar entre 0 y 100.
- Rechaza valores negativos o fuera del rango admitido.
- Documenta cómo se manejan los límites de NUMERIC(16,2).
- Mantén los indicadores EVM fuera de las tablas: deben calcularse dinámicamente mediante el motor existente.

No modifiques las fórmulas ni los contratos del motor EVM en esta fase.

 5. Pruebas

Implementa pruebas de persistencia en una base PostgreSQL de pruebas aislada que permitan verificar:

1. Creación y consulta de proyectos.
2. Creación y consulta de actividades relacionadas.
3. Persistencia exacta de valores Decimal.
4. Restricciones de porcentajes e importes.
5. Integridad referencial.
6. Eliminación en cascada.
7. Aislamiento y limpieza de datos de prueba.

No utilices la base de producción o desarrollo para ejecutar pruebas destructivas.

 6. Validación

Ejecuta las verificaciones disponibles:
- pytest.
- pytest-cov.
- Ruff check y format check.
- git diff --check.
- Comprobación de conexión real con PostgreSQL.
- Verificación de que el script SQL y los modelos son coherentes.

Distingue claramente pruebas ejecutadas de comprobaciones pendientes.

 Restricciones
- Trabaja exclusivamente en feature/database-models.
- No implementes todavía endpoints CRUD.
- No modifiques el frontend.
- No agregues autenticación ni funcionalidades fuera del alcance.
- No realices commits, pushes ni Pull Requests.
- No reconstruyas ni modifiques prompts históricos de AI_PROCESS.md.
- No alteres configuraciones globales ni elimines datos existentes.

Al finalizar, entrega un resumen de archivos creados o modificados, pruebas ejecutadas, resultados y decisiones pendientes.

Si necesitas credenciales o parámetros del entorno local, explica cómo configurarlos de forma segura sin solicitar contraseñas en el chat.

### Interacción 014 - Implementación de la API REST
Fecha: 2026-11-18
Herramienta: Codex

Prompt:

FASE 5 — Implementación de API REST y CRUD con FastAPI

Continúo el desafío técnico de Trycore en la rama feature/rest-api.

Las fases anteriores ya implementaron y validaron:
- Estructura fullstack con FastAPI y React/Vite.
- Motor EVM independiente con Decimal, cálculos individuales y consolidados, y pruebas unitarias.
- Modelos Project y Activity mediante SQLAlchemy 2.x.
- Persistencia PostgreSQL con pruebas reales de integridad, precisión, relaciones y cascada.
- Una suite que reportó 186 pruebas aprobadas antes de esta fase.

 Objetivo

Implementa una API REST completa para gestionar proyectos y actividades, integrando la persistencia PostgreSQL con el motor EVM existente.

Antes de modificar código, inspecciona los modelos, funciones y contratos actuales para reutilizarlos sin duplicar lógica ni introducir incompatibilidades.

 1. Endpoints de proyectos

Implementa:
- POST /api/projects — Crear proyecto.
- GET /api/projects — Listar proyectos.
- GET /api/projects/{project_id} — Consultar proyecto.
- PUT /api/projects/{project_id} — Actualizar proyecto.
- DELETE /api/projects/{project_id} — Eliminar proyecto y sus actividades asociadas.

 2. Endpoints de actividades

Implementa:
- POST /api/projects/{project_id}/activities — Crear actividad en un proyecto.
- GET /api/projects/{project_id}/activities — Listar actividades del proyecto.
- GET /api/projects/{project_id}/activities/{activity_id} — Consultar actividad.
- PUT /api/projects/{project_id}/activities/{activity_id} — Actualizar actividad.
- DELETE /api/projects/{project_id}/activities/{activity_id} — Eliminar actividad.

Las consultas y modificaciones de actividades deben comprobar que pertenecen al proyecto indicado. Una actividad de otro proyecto no debe poder modificarse mediante un ID de proyecto incorrecto.

 3. Endpoints EVM

Implementa:
- GET /api/projects/{project_id}/evm — Indicadores consolidados del proyecto.
- GET /api/projects/{project_id}/activities/{activity_id}/evm — Indicadores de una actividad.

Los resultados deben incluir BAC, PV, EV, AC, CV, SV, CPI, SPI, EAC, VAC y las interpretaciones correspondientes.

Utiliza directamente las funciones públicas existentes calculate_activity y calculate_project.

No reimplementes las fórmulas en routers, servicios ni modelos SQLAlchemy.

Los proyectos sin actividades deben conservar el comportamiento ya definido en el motor EVM.

 4. Arquitectura

Respeta la arquitectura modular existente:
- routers/: endpoints HTTP.
- schemas/: modelos Pydantic de entrada y salida.
- services/: operaciones de negocio y coordinación con SQLAlchemy y EVM.
- models/: entidades existentes de PostgreSQL.
- db.py: sesiones de base de datos.
- evm/: motor matemático independiente.

No introduzcas una capa Repository adicional, microservicios, Docker o Alembic.

 5. Validaciones y contratos
- Utiliza Pydantic para validar requests y responses.
- Reutiliza las restricciones de nombres, presupuestos, porcentajes y costos establecidas en feature/database-models.
- No permitas valores negativos ni porcentajes superiores a 100.
- Conserva la precisión decimal durante todo el procesamiento.
- Evita conversiones intermedias a float.
- Define una representación JSON consistente: valores Decimal como cadenas y los indicadores matemáticamente indefinidos como null.
- Mantén los códigos HTTP apropiados: 201 para creación, 200 para consultas/actualizaciones, 204 para eliminación, 404 para recursos inexistentes y 422 para datos inválidos.
- No expongas detalles internos de errores SQL ni credenciales.
- Respeta las restricciones NUMERIC(16,2) y NUMERIC(5,2) existentes.
- Conserva las interpretaciones actualmente definidas por el motor EVM.

 6. Documentación Swagger/OpenAPI

Mantén la documentación interactiva disponible en /api-docs.

Organiza los endpoints con etiquetas claras para proyectos, actividades e indicadores EVM.

Documenta correctamente los esquemas, parámetros, tipos de respuesta y códigos HTTP.

 7. Pruebas automatizadas

Implementa pruebas de integración HTTP para cada endpoint utilizando FastAPI TestClient y una base PostgreSQL aislada.

Utiliza exclusivamente trycore_evm_test, configurada mediante backend/.env.test.

Verifica como mínimo:
- CRUD completo de proyectos.
- CRUD completo de actividades.
- Relaciones entre proyectos y actividades.
- Eliminación en cascada.
- Respuestas 404 y 422.
- Persistencia real después de crear y actualizar registros.
- Indicadores EVM individuales.
- Indicadores EVM consolidados.
- Caso matemático obligatorio de tres actividades.
- Decimales serializados correctamente.
- Indicadores indefinidos representados como null.
- Aislamiento y limpieza de datos entre pruebas.

No ejecutes pruebas destructivas en la base de desarrollo.

 8. Configuración y ejecución

Documenta cómo configurar y ejecutar el backend localmente.

Si falta crear o inicializar la base de desarrollo, explica los pasos necesarios sin asumir que puede reutilizarse la base de pruebas.

La API debe poder arrancar y recibir solicitudes mediante Uvicorn.

No implementes funcionalidades del frontend en esta fase.

 9. Validación final

Ejecuta:
- Suite completa de pytest.
- Cobertura de pruebas.
- ruff check .
- ruff format --check .
- git diff --check.

Comprueba además que los endpoints aparezcan correctamente en /api-docs.

Distingue cualquier comprobación realizada automáticamente de las que requieran validación manual.

 Restricciones
- Trabaja exclusivamente en feature/rest-api.
- Mantén el código limpio, modular y con nombres técnicos en inglés.
- No alteres el motor EVM salvo que detectes un error bloqueante real, que deberás explicar previamente.
- No agregues autenticación ni nuevas tecnologías innecesarias.
- No modifiques el frontend.
- No inventes métricas ni resultados de pruebas.
- No modifiques ni reconstruyas el historial de AI_PROCESS.md.
- No realices commits, pushes ni Pull Requests.

Al finalizar entrega un informe conciso con archivos creados o modificados, endpoints implementados, resultados de pruebas, cobertura y cualquier problema pendiente.

El resultado esperado es una API REST funcional, persistente y documentada que pueda ser consumida posteriormente por React.

### Interacción 015 - Configuración de PostgreSQL de desarrollo
Fecha: 2026-11-18 
Herramienta: Codex

Prompt:

Ya creé correctamente las bases PostgreSQL trycore_evm y trycore_evm_test.

También configuré backend/.env con DATABASE_URL apuntando exclusivamente a trycore_evm, y backend/.env.test con TEST_DATABASE_URL apuntando exclusivamente a trycore_evm_test.

Guíame para inicializar las tablas de la base de desarrollo mediante database/init_db.sql, comprobar la conexión y ejecutar FastAPI para validar manualmente los endpoints en Swagger UI.

No modifiques código, no ejecutes operaciones destructivas, no expongas credenciales y no hagas commits ni Pull Requests.

### Interacción 016 - Implementación del dashboard React
Fecha: 2026-11-18
Herramienta: Codex

Prompt:

FASE 6 — Implementación del Frontend Dashboard con React

Continúo el desafío técnico de Trycore en la rama feature/frontend-dashboard.

El proyecto ya dispone de:
- Backend FastAPI funcional con 12 endpoints de negocio.
- Modelos SQLAlchemy y persistencia PostgreSQL.
- Motor EVM independiente que calcula indicadores individuales y consolidados.
- Contratos de entrada y salida mediante Pydantic.
- API documentada en Swagger /api-docs.
- Pruebas automatizadas y validación manual del caso empresarial de tres actividades.

 OBJETIVO

Implementar un frontend empresarial profesional, funcional y responsive utilizando React, Vite y JavaScript/JSX, consumiendo exclusivamente los endpoints existentes del backend.

Antes de modificar código, inspecciona frontend/, docs/api.md y los schemas FastAPI para identificar las rutas y estructuras JSON reales. No inventes endpoints ni campos.

 1. Gestión de proyectos

Implementa una interfaz que permita:
- Consultar y seleccionar proyectos existentes.
- Crear proyectos.
- Editar proyectos.
- Eliminar proyectos, solicitando confirmación.
- Mostrar estados vacíos, carga y errores.

Al seleccionar un proyecto deben actualizarse sus actividades e indicadores.

 2. Gestión de actividades

Implementa CRUD completo de actividades asociadas al proyecto seleccionado.

Campos del formulario:
- Nombre.
- BAC.
- Porcentaje de avance planificado.
- Porcentaje de avance real.
- Costo ejecutado (AC).

Requisitos:
- Validar campos obligatorios.
- Impedir importes negativos y porcentajes fuera de 0–100.
- Respetar los límites de precisión y escala definidos en el backend.
- Presentar errores de validación de forma comprensible.
- Confirmar eliminaciones.
- Actualizar automáticamente tabla, indicadores y gráfica después de crear, editar o eliminar actividades.

 3. Dashboard EVM consolidado

Construye tarjetas de indicadores para:
- BAC, PV, EV y AC.
- CV y SV.
- CPI y SPI.
- EAC y VAC.

Muestra las interpretaciones de CPI y SPI con estados visuales:
- Favorable.
- Desfavorable.
- Según lo previsto.
- No calculable.

Los indicadores indefinidos recibidos como null no deben mostrarse como cero.

Utiliza un formato legible para los valores monetarios, preferiblemente COP, sin alterar la precisión de origen.

 4. Tabla de actividades

La tabla debe mostrar:
- Nombre de actividad.
- BAC.
- Avance planificado.
- Avance real.
- AC.
- PV.
- EV.
- CV.
- SV.
- CPI.
- SPI.
- Acciones de edición y eliminación.

Si es necesario, permite desplazamiento horizontal para conservar legibilidad en pantallas pequeñas.

Consulta los indicadores individuales desde los endpoints EVM existentes.

 5. Gráfica EVM

Implementa una gráfica comparativa de:
- Planned Value (PV).
- Earned Value (EV).
- Actual Cost (AC).

Representa los valores por actividad, con etiquetas, leyenda y diferenciación visual clara.

Utiliza una librería de gráficas adecuada para React solo si mejora la claridad y se integra sin complejidad excesiva.

Los valores graficados deben provenir de las respuestas de la API. La conversión numérica necesaria para visualización debe mantenerse aislada de cualquier lógica financiera; no vuelvas a calcular las fórmulas EVM en el frontend.

 6. Integración API
- Reutiliza exactamente los endpoints del backend.
- Centraliza las solicitudes HTTP en un módulo de servicios del frontend.
- Configura la URL base mediante variables de entorno Vite o mediante proxy de desarrollo.
- Maneja errores HTTP, problemas de conexión y respuestas 422.
- Evita solicitudes redundantes o ciclos de actualización.
- No incluyas credenciales en el frontend.
- Conserva los decimales como cadenas hasta el momento de formatearlos o graficarlos.
- Asegura que React pueda comunicarse con FastAPI localmente, utilizando proxy de Vite o configuración CORS mínima y específica si corresponde.

 7. Diseño y experiencia de usuario

Utiliza un diseño:
- Profesional y empresarial.
- Limpio, moderno y consistente.
- Responsive.
- Con buena jerarquía visual.
- Con textos de interfaz en español.
- Con estados de carga, vacíos, éxito y error.
- Accesible mediante etiquetas de formulario, controles adecuados y contraste legible.

Prioriza claridad y funcionalidad sobre animaciones o detalles visuales innecesarios.

No agregues autenticación, perfiles, exportaciones, notificaciones externas ni funcionalidades fuera del alcance.

 8. Pruebas y calidad

Implementa pruebas razonables del frontend para:
- Renderizado de componentes principales.
- Estados vacíos y errores de API.
- Validación de formularios.
- Actualización de indicadores tras cambios en actividades.
- Manejo de valores null.
- Uso correcto de las respuestas de la API.

Utiliza herramientas de testing compatibles con React y Vite, procurando no introducir dependencias innecesarias.

Ejecuta:
- Lint frontend con Oxlint.
- Build de producción Vite.
- Pruebas frontend implementadas.
- Suite backend existente para detectar regresiones.
- git diff --check.

Si las pruebas backend necesitan PostgreSQL, utiliza exclusivamente trycore_evm_test.

 9. Validación funcional

Verifica que el frontend permita completar el siguiente caso:

Proyecto: Implementación de plataforma corporativa.

Actividades:
1. Análisis — BAC 10.000.000, planificado 80%, real 100%, AC 9.000.000.
2. Desarrollo — BAC 20.000.000, planificado 60%, real 40%, AC 12.000.000.
3. Pruebas — BAC 30.000.000, planificado 50%, real 50%, AC 16.000.000.

Resultados esperados:
- BAC 60.000.000.
- PV 35.000.000.
- EV 33.000.000.
- AC 37.000.000.
- CV −4.000.000.
- SV −2.000.000.
- CPI 33/37.
- SPI 33/35.
- EAC 740/11 millones.
- VAC −80/11 millones.

Utiliza los indicadores calculados por FastAPI; no dupliques el cálculo EVM en React.

 10. Documentación

Actualiza README y documentación técnica con:
- Instalación de dependencias frontend.
- Configuración y ejecución del frontend y backend.
- Comunicación React–FastAPI.
- Instrucciones para comprobar el caso de referencia.

 RESTRICCIONES
- Trabaja exclusivamente en feature/frontend-dashboard.
- No modifiques el motor EVM ni los modelos PostgreSQL salvo error bloqueante que debas explicar previamente.
- No agregues nuevas funciones de negocio al backend.
- No migres a TypeScript.
- Mantén código limpio, modular y fácil de explicar.
- No modifiques ni reconstruyas AI_PROCESS.md.
- No realices commits, pushes ni Pull Requests.
- No expongas credenciales ni modifiques bases de datos con información existente sin autorización.

 RESULTADO ESPERADO

Al finalizar, informa:
1. Archivos creados y modificados.
2. Componentes React implementados.
3. Librerías nuevas y justificación.
4. Endpoints integrados.
5. Pruebas realizadas y resultados.
6. Instrucciones exactas para ejecutar y abrir la aplicación.
7. Problemas pendientes y validaciones manuales necesarias.

### Interacción 017 - Validación final del dashboard
Fecha: 2026-11-18
Herramienta: Codex

Prompt:

Validación final de feature/frontend-dashboard

La aplicación React ya fue revisada manualmente en Chrome utilizando la base de desarrollo.

Se confirmó que:
- El dashboard carga correctamente.
- Se visualizan el proyecto y las tres actividades de referencia.
- Los indicadores EVM coinciden con Swagger.
- La gráfica PV, EV y AC representa correctamente las actividades.
- La creación, edición y eliminación de una actividad funcionan.
- Los indicadores, la tabla y la gráfica se actualizan después de las operaciones.

Realiza ahora el cierre técnico de feature/frontend-dashboard.

1. Ejecuta la suite completa de pruebas frontend con Vitest.
2. Ejecuta Oxlint y el build de producción de Vite.
3. Ejecuta las pruebas backend, utilizando exclusivamente la base PostgreSQL de pruebas aislada.
4. Verifica git diff --check.
5. Revisa los seis avisos de seguridad de dependencias e identifica si afectan producción o desarrollo. No apliques actualizaciones mayores automáticas.
6. Revisa los archivos creados o modificados y detecta problemas bloqueantes, código innecesario o cambios fuera del alcance.
7. Confirma que no existan credenciales ni archivos .env sensibles preparados para Git.
8. Verifica que el motor EVM no fue duplicado en JavaScript.

No reimplementes funcionalidades existentes ni realices cambios estéticos innecesarios.

Corrige únicamente errores bloqueantes o problemas de calidad claramente justificados.

No modifiques AI_PROCESS.md.
No realices commits, pushes ni Pull Requests.

Entrega un informe final con resultados, riesgos pendientes y una conclusión explícita sobre si la rama está lista para integrarse a develop.

## 4. Desacuerdos con IA (dos casos)

### Desacuerdo 1 — Rechazo del uso de Docker y Alembic

**Contexto:**
Durante la planificación de la arquitectura, la IA planteó el uso de Docker para contenerizar la aplicación y Alembic para gestionar las migraciones de la base de datos. Sin embargo, consideré que estas herramientas añadían complejidad innecesaria para el alcance y los requisitos del desafío técnico.

**Decisión que tomé:**
Decidí no usar Docker ni Alembic. Opté por utilizar PostgreSQL instalado localmente, un script SQL (init_db.sql) para inicializar las tablas y ejecutar el backend y el frontend directamente desde sus respectivos entornos de desarrollo.

**Justificación técnica:**
Mi decisión se basó en priorizar una solución sencilla, funcional y mantenible, teniendo en cuenta el tiempo disponible para completar el desafío. Aunque Docker y Alembic son herramientas útiles en proyectos de mayor escala, no eran indispensables para implementar en este caso.

**Resultado:**
La aplicación se implementó utilizando React, FastAPI y PostgreSQL local, con un script SQL reproducible para la inicialización de la base de datos. Se completaron las funcionalidades requeridas y las pruebas automatizadas sin necesidad de incorporar Docker ni Alembic.

### Desacuerdo 2 Rechazo de una corrección automática de dependencias

**Contexto:**
Durante la configuración del frontend, la herramienta npm audit identificó cinco avisos de seguridad en dependencias en herramientas de desarrollo.
La corrección automática propuesta implicaba modificar versiones mayores de algunas dependencias, lo que podía introducir incompatibilidades o afectar la estabilidad del proyecto.

**Decisión que tomé:**
Decidí no aplicar npm audit fix --force automáticamente. En su lugar, solicité revisar las dependencias afectadas, analizar su impacto y documentar las vulnerabilidades conocidas.

**Justificación técnica:**
Consideré que una actualización mayor automática podía introducir riesgos de compatibilidad sin garantizar una solución adecuada. Preferí mantener las versiones utilizadas, verificar el funcionamiento de la aplicación y registrar los riesgos pendientes para una corrección posterior controlada.

**Resultado:**
Se conservaron las dependencias, se completaron las verificaciones funcionales y los avisos quedaron documentados. No se presentaron las vulnerabilidades como corregidas.

## 5. Decisión arquitectónica independiente

**Contexto:**

Después de analizar los requisitos del desafío técnico y estudiar los fundamentos de Earned Value Management (EVM), evalué las alternativas arquitectónicas para desarrollar la aplicación.

Durante esta etapa se consideró una arquitectura basada en microservicios, que consiste en dividir una aplicación en servicios independientes que se comunican entre sí. Aunque este enfoque ofrece ventajas de escalabilidad y despliegue independiente, también requiere una mayor complejidad de configuración, comunicación y mantenimiento.

**Decisión que tomé:**
Después de evaluar el alcance, las funcionalidades requeridas y el tiempo disponible, decidí implementar una arquitectura monolítica modular, manteniendo el frontend, el backend y la Base de datos en PostgreSQL.

**Justificación técnica:**

Consideré que una arquitectura de microservicios sería excesiva para una aplicación de este tamaño, ya que incorporaría complejidad de infraestructura y comunicación sin aportar beneficios significativos para los requisitos del desafío.

La arquitectura monolítica modular me permitió mantener el código organizado, facilitar las pruebas y simplificar la integración entre los componentes, sin sacrificar la posibilidad de ampliar el sistema posteriormente.

**Resultado:**

La aplicación se desarrolló con un backend modular en FastAPI, un frontend independiente en React y una base de datos PostgreSQL. El motor EVM quedó desacoplado de la API, permitiendo probar los cálculos de manera independiente.

Esta decisión permitió completar e integrar las funcionalidades principales, manteniendo una arquitectura sencilla, organizada y adecuada para el alcance del proyecto.

## 6. Aprendizaje y validación EVM

**Proceso de aprendizaje:**
Antes de comenzar con la implementación, consideré importante comprender correctamente el concepto de Earned Value Management (EVM), ya que no había trabajado directamente con esta metodología.

Inicialmente, investigué en internet para conocer sus fundamentos, en qué área de la gestión de proyectos se utiliza, cuál es su propósito y por qué es importante para el seguimiento de presupuestos, costos y cronogramas. Complementé esta investigación con los requisitos y las fórmulas incluidas en el PDF proporcionado por Trycore.

Una vez tuve una comprensión general del tema, utilicé ChatGPT como herramienta de aprendizaje. Le solicité que me explicara EVM desde los conceptos más básicos, utilizando un lenguaje sencillo y ejemplos prácticos, como si estuviera estudiando la metodología por primera vez.

Profundicé especialmente en los indicadores BAC, PV, EV, AC, CV, SV, CPI, SPI, EAC y VAC, buscando comprender no solamente sus fórmulas, sino también qué representa cada uno, cómo se relacionan y cómo interpretar sus resultados dentro de un proyecto real.

Adicionalmente, consulté videos educativos en YouTube donde se explicaban los conceptos y se desarrollaban ejercicios prácticos. Esto me permitió complementar las explicaciones de ChatGPT con otras fuentes y entender mejor cómo se aplica EVM en situaciones empresariales.

**Validación de mi comprensión:**
Para comprobar lo aprendido, solicité a ChatGPT ejemplos numéricos con diferentes actividades, presupuestos, porcentajes de avance y costos ejecutados. Revisé cómo se obtenían los indicadores individuales y cómo debían consolidarse los resultados a nivel de proyecto.

Uno de los puntos más importantes fue comprender que los indicadores CPI y SPI consolidados deben calcularse utilizando los valores totales del proyecto, en lugar de promediar los índices individuales de las actividades.

**Aplicación de lo aprendido:**
Con estos fundamentos, pude definir las reglas que debía implementar el motor EVM y los resultados esperados para las pruebas unitarias.

## 7. Verificaciones y resultados

Durante el desarrollo realicé diferentes verificaciones para comprobar que la aplicación cumpliera los requisitos funcionales y técnicos del desafío. Mi objetivo fue no depender únicamente de los resultados generados por la IA, sino contrastarlos mediante pruebas automatizadas y comprobaciones manuales.

**7.1. Motor de cálculo EVM**

Para validar la lógica de negocio, utilicé pytest y pytest-cov, ejecutados mediante Codex. El motor EVM alcanzó los siguientes resultados:

- 74 pruebas específicas aprobadas.
- 100% de cobertura de líneas y ramas reportada para el motor EVM.
- Validación de cálculos individuales y consolidados.
- Pruebas de entradas inválidas, porcentajes fuera de rango y valores monetarios negativos.
- Comprobación de casos especiales como divisiones por cero e indicadores indefinidos.

**7.2. Base de datos PostgreSQL**

Para validar la persistencia, configuré PostgreSQL localmente y creé dos bases independientes:

- trycore_evm: base de datos de desarrollo.

- trycore_evm_test: base utilizada para pruebas automatizadas.

Mediante Codex ejecuté pruebas de integración sobre una base aislada, verificando:

- Creación y consulta de proyectos y actividades.
- Relaciones entre tablas.
- Integridad referencial.
- Eliminación en cascada.
- Precisión de valores Decimal.
- Restricciones de presupuestos y porcentajes.
- Equivalencia entre los modelos SQLAlchemy y el esquema SQL.

Las 68 pruebas específicas de persistencia finalizaron correctamente.

**7.3. API REST con FastAPI**

La implementación de la API incorporó 12 endpoints para gestionar proyectos, actividades y consultar indicadores EVM.

Codex ejecutó pruebas automatizadas de integración HTTP, incluyendo operaciones CRUD, validaciones, errores y consultas de indicadores.

Al finalizar esta fase, la suite del backend reportó:

- 297 pruebas aprobadas.
- Ninguna prueba omitida.
- 100% de cobertura de líneas reportada.
- Verificaciones Ruff y Ruff Format satisfactorias.

**7.4. Frontend React**

Para validar la interfaz ejecuté FastAPI mediante Uvicorn y el frontend mediante Vite. Codex realizó las siguientes verificaciones:

- 27 pruebas frontend aprobadas con Vitest.
- Una prueba adicional de integración React–FastAPI utilizando PostgreSQL aislado.
- Oxlint sin errores ni advertencias.
- Compilación de producción de Vite correcta.
- Suite backend de 297 pruebas aprobadas.
 
Posteriormente, abrí la aplicación en Chrome y comprobé manualmente:

- Visualización de proyectos existentes.
- Presentación de indicadores EVM consolidados.
- Tabla de actividades.
- Gráfica comparativa de PV, EV y AC.
- Creación, edición y eliminación de actividades.
- Actualización automática de indicadores, tabla y gráfica después de modificar los datos.

Las operaciones realizadas funcionaron correctamente y los resultados coincidieron con los obtenidos anteriormente en Swagger.

**7.5. Control de versiones**

Organicé el desarrollo mediante Gitflow, utilizando las ramas main, develop y feature para separar las funcionalidades.

Realicé commits y Pull Requests para incorporar progresivamente la configuración inicial, el motor EVM, la persistencia y la API REST.

Antes de integrar cada funcionalidad, revisé los resultados de las pruebas y las verificaciones de calidad reportadas por Codex.

La validación final de la rama frontend también confirmó que no se estaban incluyendo credenciales locales ni archivos sensibles en los cambios preparados para Git.

## 8. Limitaciones conocidas y Reflexión

Durante el desarrollo identifiqué algunas limitaciones y posibles mejoras que considero importantes para una evolución futura de la aplicación.

**8.1. Ejecución local**

La aplicación fue desarrollada y validada en un entorno local utilizando FastAPI, React y PostgreSQL.

No implementé una infraestructura de despliegue en la nube ni contenerización con Docker, ya que el objetivo principal era entregar una solución funcional y verificable dentro del alcance del desafío.

Para utilizarla en producción sería necesario definir una estrategia de despliegue, configuración de entornos y administración de infraestructura.

**8.2. Seguridad y autenticación**

La aplicación no incluye autenticación ni gestión de roles y permisos.

Esta funcionalidad no fue incorporada porque no formaba parte del alcance establecido para el desafío. Sin embargo, sería necesaria antes de exponer la aplicación a usuarios externos en un entorno productivo.

**8.6. Precisión y límites numéricos**

Para conservar precisión monetaria, el motor EVM utiliza Decimal y PostgreSQL almacena los importes mediante campos NUMERIC.

La base de datos establece límites de precisión y escala que deben respetarse al registrar presupuestos, costos y porcentajes.

### Reflexión final

El desarrollo de este desafío fue una oportunidad para aplicar y fortalecer mis conocimientos en ingeniería de software, programación, automatización y desarrollo de aplicaciones fullstack.

Uno de los principales retos fue comprender Earned Value Management (EVM), una metodología con la que no había trabajado directamente. Para ello, investigué sus fundamentos y utilicé ChatGPT como apoyo para comprender los indicadores, sus fórmulas y su aplicación en escenarios empresariales.

Durante el proyecto utilicé ChatGPT para analizar requisitos, evaluar alternativas y tomar decisiones técnicas, mientras que Codex me apoyó en la implementación, revisión del código y ejecución de pruebas automatizadas.

Considero que uno de los aprendizajes más importantes fue la necesidad de mantener un criterio propio frente a las recomendaciones de IA, evaluando aspectos como la complejidad arquitectónica, las tecnologías utilizadas y la mantenibilidad de la solución.

También reforcé mis conocimientos en FastAPI, React, PostgreSQL, testing y Gitflow, especialmente durante la integración de los componentes y las validaciones funcionales realizadas manualmente.

Mi principal conclusión es que la Inteligencia Artificial puede acelerar significativamente el desarrollo de software, pero no reemplaza el análisis, el criterio técnico ni la validación humana. El verdadero valor está en saber utilizarla como herramienta de apoyo para construir soluciones funcionales, comprender las decisiones tomadas y garantizar la calidad de los resultados.