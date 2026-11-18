# API REST

La API usa Router → Service → SQLAlchemy y conserva el motor EVM independiente. Los servicios
llaman directamente a `calculate_activity` y `calculate_project`, adaptando los campos del modelo
sin replicar fórmulas. Las operaciones de escritura confirman su transacción o hacen rollback
ante errores SQLAlchemy. Cada petición recibe una sesión que se cierra al terminar.

## Endpoints

| Método | Ruta | Respuesta correcta |
| --- | --- | --- |
| POST | `/api/projects` | 201, proyecto |
| GET | `/api/projects` | 200, lista de proyectos |
| GET | `/api/projects/{project_id}` | 200, proyecto |
| PUT | `/api/projects/{project_id}` | 200, proyecto actualizado |
| DELETE | `/api/projects/{project_id}` | 204, sin cuerpo; cascada de actividades |
| POST | `/api/projects/{project_id}/activities` | 201, actividad |
| GET | `/api/projects/{project_id}/activities` | 200, lista de actividades |
| GET | `/api/projects/{project_id}/activities/{activity_id}` | 200, actividad |
| PUT | `/api/projects/{project_id}/activities/{activity_id}` | 200, actividad actualizada |
| DELETE | `/api/projects/{project_id}/activities/{activity_id}` | 204, sin cuerpo |
| GET | `/api/projects/{project_id}/evm` | 200, indicadores consolidados |
| GET | `/api/projects/{project_id}/activities/{activity_id}/evm` | 200, indicadores individuales |

Las listas se ordenan por ID y no tienen paginación en esta fase. Las rutas de actividades
verifican la pertenencia al proyecto. Un proyecto inexistente no devuelve una lista vacía:
devuelve 404. Solo un proyecto existente sin actividades devuelve `[]`.

## Contratos JSON

Crear o reemplazar un proyecto:

```json
{"name": "Proyecto Trycore", "description": "Descripción opcional"}
```

Crear o reemplazar una actividad:

```json
{
  "name": "Análisis",
  "bac": "10.00",
  "planned_progress_pct": "80.00",
  "actual_progress_pct": "100.00",
  "actual_cost": "9.00"
}
```

- Los importes y porcentajes de entrada son **cadenas decimales**, no números JSON. Esto evita
  conversiones a float antes de validar. Las respuestas también los serializan como cadenas;
  no se garantiza una cantidad fija de ceros finales. IDs son enteros.
- Nombres obligatorios, no vacíos ni solo espacios, hasta 150 caracteres. Se conservan los
  espacios exteriores de nombres válidos. `description` puede omitirse o ser `null`.
- Se reutilizan los validadores de persistencia. Importes entre 0 y 99999999999999.99;
  avances entre 0 y 100; máximo dos posiciones decimales significativas. No se redondean
  silenciosamente entradas inválidas. Se rechazan NaN, Infinity y campos desconocidos.
- `PUT` reemplaza los campos editables completos: requiere `name` y, para actividades,
  las cuatro medidas. Omitir `description` la restablece a `null`. No se permite cambiar IDs
  o mover actividades a otro proyecto mediante el cuerpo.
- EVM devuelve `bac`, `pv`, `ev`, `ac`, `cv`, `sv`, `cpi`, `spi`, `eac`, `vac`,
  `cpi_interpretation` y `spi_interpretation`. Los valores indefinidos se incluyen como
  `null`; un índice cero se representa como cadena decimal cero. Se conservan las
  interpretaciones `favorable`, `desfavorable` y `según lo previsto` del motor.
- Un proyecto vacío tiene totales cero e índices, estimaciones e interpretaciones `null`.
  Los cálculos respetan el contexto Decimal del motor y no se redondean a centavos.

## Errores y OpenAPI

404 indica recurso inexistente o actividad ajena al proyecto. 422 indica request inválido
o restricciones de almacenamiento. La validación Pydantic devuelve `detail` como lista de
errores; un rechazo de almacenamiento devuelve un mensaje genérico en `detail`. Los errores
de disponibilidad SQLAlchemy devuelven 503. No se incluyen SQL, parámetros ni credenciales.
No se ha agregado autenticación: esta API está prevista para desarrollo local.

Swagger está en `/api-docs`, con etiquetas `projects`, `activities` y `evm`;
OpenAPI está en `/openapi.json`. Los esquemas documentan cuerpos, respuestas, parámetros y
códigos HTTP. Swagger necesita conexión al CDN para cargar sus recursos visuales.

## Ejecución en Windows

Crear/inicializar una base de **desarrollo** y configurar `backend/.env` con DATABASE_URL
siguiendo [database.md](database.md). No sustituirla por `trycore_evm_test` para trabajo normal.
No se crean bases ni tablas automáticamente al arrancar. Si ya existe `.env`, editarlo sin
sobrescribirlo con el ejemplo. Las credenciales se configuran localmente, nunca en el repositorio.

Desde `backend/`:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Desde otra terminal, contra la base de desarrollo ya configurada:

```powershell
$projectBody = @{ name = 'Proyecto local'; description = 'Ejemplo' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8000/api/projects' -ContentType 'application/json' -Body $projectBody
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/projects'
```

Sin configuración de base se puede consultar salud y Swagger, pero los endpoints de datos
requieren una DATABASE_URL válida y el esquema inicializado.

## Verificación automatizada

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m pytest tests/api --cov=app
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
```

Las pruebas HTTP usan TestClient, PostgreSQL real y exclusivamente `trycore_evm_test` a partir
de TEST_DATABASE_URL en `.env.test` (o el entorno). Cada request recibe una sesión; sus commits
quedan contenidos en la transacción externa de un esquema único por prueba. Al finalizar se
revierte todo y se comprueba la limpieza. No se conectan a la base de desarrollo.

Se comprueban CRUD, pertenencia, cascada, consultas directas a datos persistidos, rechazos,
resultados EVM del caso obligatorio, cadenas decimales, null y contenido de OpenAPI. La
inspección visual interactiva de Swagger y el uso manual contra desarrollo son comprobaciones
distintas de estas pruebas automáticas.
