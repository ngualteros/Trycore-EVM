# Registro de asistencia de IA

## 2026-11-17 — Configuración inicial

El usuario pidió inspeccionar el repositorio y presentar una propuesta sin cambios.
La inspección encontró `README.md`, un `.gitignore` de Python y las ramas `main`, `develop` y
`feature/project-setup` en el commit inicial. Se presentó un plan para revisión.

El usuario aprobó la arquitectura con ajustes explícitos: JavaScript/JSX, PostgreSQL local,
inicialización SQL sin Alembic, `requirements.txt`, pytest, pytest-cov y Ruff. Autorizó
el endpoint de salud, Swagger en `/api-docs`, una pantalla mínima y documentación de Windows.
Prohibió entidades, CRUD, fórmulas EVM, tablas, autenticación, Docker, commits y Pull Requests.

La IA creó el esqueleto del backend, pruebas de infraestructura, configuración de herramientas,
script de base vacía y documentación. Generó el frontend con la plantilla oficial
`create-vite@9.3.4` para React y sustituyó la demostración por una pantalla mínima.
La plantilla incluye Oxlint para JavaScript/JSX.

Las primeras consultas a npm y la instalación con pip fallaron por restricciones de red del
sandbox. Se solicitaron ejecuciones con permisos ampliados para descargar las dependencias.
No se cambió la configuración global de Git: la inspección usó `safe.directory` limitado al
comando debido a una diferencia de propietario del repositorio.

Los resultados de las verificaciones se registran después de ejecutarlas. Este archivo no
describe trabajo anterior a esta conversación ni supone aprobación humana de los cambios finales.

### Verificaciones ejecutadas

- `python -m pip check` dentro del entorno virtual: sin dependencias incompatibles.
- `python -m pytest`: 3 pruebas aprobadas; cobertura del 100% de las 18 sentencias actuales.
  Starlette emitió una advertencia de deprecación del uso de `httpx` en TestClient.
- `python -m ruff check .`: aprobado.
- `python -m ruff format --check .`: 11 archivos con formato correcto.
- `npm.cmd run lint`: aprobado con Oxlint.
- `npm.cmd run build`: aprobado con Vite 8.3.8.
- Se arrancaron temporalmente Uvicorn y Vite en los puertos 18000 y 15173 y se comprobaron
  respuestas HTTP 200, JSON de salud y contenido del frontend. Ambos procesos se detuvieron.
  No se realizó inspección visual en navegador.
- `npm.cmd audit --json`: 5 avisos de severidad alta en la cadena de herramientas de desarrollo
  (`picomatch`, `fdir`, `tinyglobby`, `vite` y `@vitejs/plugin-react`), originados en
  GHSA-fc5q-39xc-vjpf. El registro consultado ofrece `picomatch` 4.0.7 como última versión,
  incluida en el rango vulnerable. La corrección automática propone bajar versiones mayores
  de Vite/plugin; no se aplicó `audit fix --force`. Los avisos permanecen pendientes.
- No se encontró `psql` en PATH ni la carpeta habitual `C:\Program Files\PostgreSQL`.
  No se ejecutó `database/init_db.sql` ni se verificó una conexión PostgreSQL.
- Git mantiene la rama `feature/project-setup`. No se crearon commits ni Pull Requests.
