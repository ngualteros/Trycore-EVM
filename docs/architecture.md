# Arquitectura inicial

Monorepositorio con FastAPI/Python, React/Vite con JavaScript/JSX y PostgreSQL local.
SQLAlchemy utilizará su API síncrona y el driver Psycopg 3.

## Estado implementado

`app/main.py` compone FastAPI y registra el router de salud. Swagger UI vive en `/api-docs`.
`app/config.py` define la lectura de `DATABASE_URL` mediante Pydantic Settings desde el entorno
o `backend/.env`. La configuración no se instancia al importar la aplicación: la salud funciona
sin base de datos ni archivo `.env`.

`evm` contiene las fórmulas independientes y `models` contiene Project y Activity con
SQLAlchemy síncrono. `db.py` administra engine y sesiones de forma diferida. `services`
coordina CRUD y EVM; `schemas` valida entradas y salidas Pydantic. Los routers exponen
los doce endpoints de proyectos, actividades e indicadores descritos en [api.md](api.md).
El frontend muestra una pantalla inicial estática. Véase [persistencia](database.md).

## Responsabilidades para las siguientes etapas

Flujo acordado: **Router → Service → SQLAlchemy**.

- `routers/`: HTTP, validación y serialización mediante Pydantic.
- `services/`: casos de uso, reglas y límites de transacción.
- `models/`: entidades SQLAlchemy, relaciones y validación de asignaciones.
- `schemas/`: contratos Pydantic de entrada y salida.
- `evm/`: funciones puras sin importar FastAPI ni SQLAlchemy.
- `db.py`: engine síncrono y generador de sesiones, cerradas al finalizar; sin sesiones
  globales compartidas ni creación automática de tablas al arrancar.

Los handlers que acceden a persistencia síncrona utilizan `def`. No se añade Repository
ni infraestructura asíncrona. La salud no necesita un servicio vacío.

## Pruebas y evolución

El motor EVM tiene pruebas unitarias de fórmulas y casos límite. Las pruebas de persistencia
usan PostgreSQL 17 separado, con el marcador `integration`, esquemas exclusivos y rollback;
nunca usan la base de trabajo como alternativa. Sin TEST_DATABASE_URL se omiten explícitamente.

`init_db.sql` crea tablas y restricciones de forma repetible sin eliminar datos existentes;
no migra esquemas preexistentes. No se incorpora Alembic ni Docker. La integración frontend/API,
incluida la decisión de proxy o CORS, queda para la primera funcionalidad que la necesite.

Cada incremento debe ser revisable en una rama `feature/*` basada en `develop`. La estructura
permite incorporar persistencia, servicios, EVM y pantallas por separado. No se afirma
cobertura completa del desafío sin disponer de su enunciado.

## Herramientas y vulnerabilidades conocidas

El frontend conserva Oxlint para JavaScript/JSX; no utiliza ESLint. Las versiones de
dependencias se mantienen sin cambios en esta revisión.

La auditoría del 2026-11-17 reportó cinco avisos altos en `picomatch@4.0.7`,
`fdir@6.5.0`, `tinyglobby@0.2.17`, `vite@8.3.8` y `@vitejs/plugin-react@6.3.0`.
Todos derivan de [GHSA-fc5q-39xc-vjpf](https://github.com/advisories/GHSA-fc5q-39xc-vjpf):
patrones glob maliciosos pueden bloquear un proceso Node por consumo de CPU (ReDoS).
Afectan la cadena de herramientas de desarrollo; `npm audit --omit=dev` reportó cero
vulnerabilidades. No se identificó una entrada de usuario que alcance esos patrones en
la pantalla estática actual; esto no implica que las dependencias estén corregidas.

En la consulta realizada no había una versión corregida de picomatch. Se mantiene el
servidor de desarrollo en localhost y se deben evitar patrones de fuentes no confiables.
Queda pendiente revisar una corrección compatible cuando esté disponible y repetir las
verificaciones. No se aplicó `npm audit fix --force` ni la bajada mayor de Vite/plugin
propuesta por npm. Estos avisos siguen abiertos.
