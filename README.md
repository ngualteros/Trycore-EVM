# Trycore EVM

Aplicación fullstack de gestión de proyectos con indicadores Earned Value Management.
Esta rama contiene solo la configuración inicial: API de salud, Swagger UI, pantalla React
y herramientas. No hay entidades, tablas, CRUD ni cálculos EVM.

## Requisitos locales

- Windows y PowerShell.
- Python 3.12 (entorno utilizado: 3.12.7).
- Node.js 22.12+ o posterior compatible con Vite (entorno utilizado: 26.13.1).
- npm (entorno utilizado: 11.20.0).
- PostgreSQL local, con el servicio iniciado, para preparar la base de datos.

La API de salud y el frontend arrancan sin PostgreSQL. Los comandos parten de la raíz
del repositorio salvo indicación contraria. Se usa `npm.cmd` y el ejecutable del entorno
virtual para evitar cambios en la política de ejecución de PowerShell.
Si `python` no apunta a Python 3.12, usar `py -3.12` para crear el entorno.

## Backend

```powershell
python -m venv backend/.venv
Set-Location backend
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- Salud: <http://127.0.0.1:8000/health>, devuelve `{"status":"ok"}`.
- Swagger UI: <http://127.0.0.1:8000/api-docs>.
- OpenAPI: <http://127.0.0.1:8000/openapi.json>.

`/health` comprueba que la aplicación responde; no verifica PostgreSQL. Swagger carga
recursos desde un CDN y necesita internet en el navegador. Editar `backend/.env` con las
credenciales locales antes de añadir persistencia. La configuración está preparada,
pero todavía no se crea un engine ni una sesión.

## PostgreSQL local

`database/init_db.sql` crea únicamente la base vacía `trycore_evm` si no existe.
Está escrito para **psql** porque utiliza `\gexec`; no ejecutarlo directamente en el
Query Tool de pgAdmin. No crea tablas ni modifica bases existentes.

Desde la raíz, con `psql` en PATH:

```powershell
psql -h localhost -p 5432 -U postgres -d postgres -W -v ON_ERROR_STOP=1 -f database/init_db.sql
```

Si `psql` no está en PATH, usar su ruta real, por ejemplo:

```powershell
& 'C:\Program Files\PostgreSQL\18\bin\psql.exe' -h localhost -p 5432 -U postgres -d postgres -W -v ON_ERROR_STOP=1 -f database/init_db.sql
```

Reemplazar `18` por la carpeta de la versión instalada. El usuario debe poder crear bases
de datos. `-W` solicita la contraseña sin guardarla en el comando. En `DATABASE_URL`, codificar
los caracteres reservados de la contraseña como componentes de URL. No versionar `.env`.

## Frontend

En otra terminal, desde la raíz:

```powershell
Set-Location frontend
npm.cmd ci
Copy-Item .env.example .env
npm.cmd run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

Abrir <http://127.0.0.1:5173>. La pantalla es estática; todavía no hace peticiones a la API.
`VITE_API_BASE_URL` queda reservado para esa integración. Las variables `VITE_*` son públicas:
no deben contener secretos. Detener cada servidor con `Ctrl+C`.

El frontend se generó con `npm.cmd create vite@9.3.4 frontend -- --template react --no-interactive`.
No repetir ese comando sobre el proyecto existente. Se conserva Oxlint, incluido por la plantilla,
para revisar JavaScript/JSX. No se usa TypeScript.

## Verificaciones

Desde `backend/`:

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
```

pytest incluye cobertura de `app/` con pytest-cov. Las pruebas iniciales comprueban salud,
OpenAPI y lectura de configuración, sin conectarse a una base de datos.

Desde `frontend/`:

```powershell
npm.cmd run lint
npm.cmd run build
npm.cmd audit
```

`requirements.txt` fija las versiones instaladas de Python, incluidas las transitivas, para
Windows/Python 3.12. `package-lock.json` fija las del frontend; usar `npm.cmd ci` para
reinstalarlas. Actualizar dependencias requiere repetir las verificaciones.

Observaciones de la verificación inicial: `npm audit` reporta cinco avisos altos de la
cadena de desarrollo de Vite, originados en `picomatch` (GHSA-fc5q-39xc-vjpf), sin una
versión 4.x corregida disponible en el registro consultado. No se aplicó una degradación
automática de Vite. pytest también muestra una advertencia de Starlette por `httpx` en
TestClient. Consultar `AI_PROCESS.md` para los resultados y límites de las verificaciones.

## Organización y Git

- `backend/app/`: API, configuración y paquetes reservados para las capas futuras.
- `backend/tests/`: pruebas de infraestructura inicial.
- `frontend/`: React + Vite con JavaScript/JSX.
- `database/`: inicialización manual de PostgreSQL, sin tablas.
- `docs/architecture.md`: responsabilidades y evolución prevista.
- `AI_PROCESS.md`: registro verificable de la asistencia de IA en esta etapa.

El trabajo permanece en `feature/project-setup`. Las futuras ramas `feature/*` se crearán
desde `develop` y se integrarán en ella tras revisión; `main` se reserva para entregas.
Esta preparación no crea commits ni Pull Requests. El enunciado completo del desafío no está
incluido; su cobertura deberá revisarse cuando esté disponible.
