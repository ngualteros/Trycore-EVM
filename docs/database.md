# Persistencia PostgreSQL

## Esquema y ciclo de vida

`projects` tiene `id` INTEGER con identidad, `name` VARCHAR(150) obligatorio y no vacío
ni compuesto solo por espacios, y `description` TEXT opcional. `activities` tiene su propia
identidad, nombre con las mismas restricciones y `project_id` obligatorio con índice y
clave foránea hacia `projects`. No se exige unicidad de nombres.

Las cuatro medidas se almacenan como Decimal: BAC y costo real con NUMERIC(16,2), avances
con NUMERIC(5,2). No se almacenan indicadores EVM: se calcularán con el motor independiente.
No se modifican sus fórmulas ni su contrato.

`ON DELETE CASCADE` elimina actividades al borrar el proyecto directamente en SQL.
SQLAlchemy usa `cascade="all, delete-orphan"` y `passive_deletes=True`: mantiene el mismo
comportamiento con colecciones cargadas y delega en PostgreSQL cuando no están cargadas.
Retirar una actividad de la colección ORM también la elimina; no puede quedar huérfana.

`app/db.py` construye el engine y la fábrica de sesiones de forma diferida y reutilizable.
Importar FastAPI no lee credenciales obligatoriamente ni conecta a PostgreSQL. El generador
`get_session()` cierra la sesión incluso en caso de error, sin commit implícito. Los servicios
controlan las escrituras mediante commit y rollback explícitos ante errores SQLAlchemy.
Cambiar DATABASE_URL requiere reiniciar el proceso para renovar los recursos cacheados.

## Precisión y validación

- NUMERIC(16,2) admite 14 cifras enteras y 2 decimales. Rango monetario aceptado:
  **0.00 a 99999999999999.99**, inclusive.
- Los avances admiten **0.00 a 100.00**, inclusive.
- Los modelos requieren Decimal finitos; no convierten float. Crear valores desde cadenas,
  por ejemplo `Decimal("123.45")`.
- La asignación ORM rechaza negativos, excesos de rango y más de dos posiciones decimales
  significativas; `1.2300` es válido, `1.231` no. La validación no depende del contexto Decimal.
- Las restricciones SQL protegen valores almacenados, incluyendo NULL, NaN y rangos.
  PostgreSQL redondea entradas con escala excesiva antes de comprobar CHECK: SQL directo
  podría convertir `-0.001` a `0.00` o `100.001` a `100.00`. Las escrituras Core/SQL omiten
  los validadores ORM. Deben recibir valores previamente validados; la API aplica también
  la política de dos decimales antes de persistir mediante schemas Pydantic.
- No se deben redondear los indicadores EVM a dos decimales durante el cálculo. La escala
  de almacenamiento corresponde a las entradas, no a los resultados derivados.

## Instalación local segura en Windows

PostgreSQL 17.12 es la versión objetivo. En el entorno inspeccionado, los ejecutables están
en `D:\Programas\Postgres\bin`; adaptar la ruta si la instalación es diferente.
Crear las bases y usuarios solo si aún no existen, mediante pgAdmin o una sesión psql
administrativa. No cambiar la configuración global del servidor.

```powershell
& 'D:\Programas\Postgres\bin\psql.exe' -X -h localhost -U postgres -d postgres -W
```

En esa sesión, para una instalación nueva, crear usuarios separados y asignar contraseñas
con `\password`, que las solicita interactivamente y evita incluirlas en el historial SQL:

```sql
CREATE ROLE trycore_app LOGIN;
\password trycore_app
CREATE DATABASE trycore_evm OWNER trycore_app;
CREATE ROLE trycore_test LOGIN;
\password trycore_test
CREATE DATABASE trycore_evm_test OWNER trycore_test;
```

No repetir CREATE ROLE/CREATE DATABASE si ya existen. El rol de pruebas no necesita ser
superusuario ni tener permiso CREATEDB; debe poder crear esquemas en su base aislada.

Copiar `backend/.env.example` a `backend/.env` y sustituir localmente DATABASE_URL. Para
pruebas, copiar `backend/.env.test.example` a `backend/.env.test` y completar únicamente
TEST_DATABASE_URL. Ambos archivos locales están ignorados por Git. No compartir las claves
en el chat ni incluirlas en comandos o capturas; codificar los caracteres reservados en la URL.

Desde la raíz, inicializar las tablas de desarrollo de manera atómica:

```powershell
& 'D:\Programas\Postgres\bin\psql.exe' -X -h localhost -U trycore_app -d trycore_evm -W -1 -v ON_ERROR_STOP=1 -f database/init_db.sql
```

El script ahora crea tablas en la base seleccionada, **no crea la base**. Es SQL estándar
para PostgreSQL sin metacomandos psql. Usa el search_path de la conexión; emplear un esquema
de confianza. IF NOT EXISTS permite repetirlo sin borrar datos, pero no actualiza ni repara
tablas preexistentes con otro esquema. Un cambio futuro de esquema exige SQL explícito revisado.

## Pruebas y aislamiento

Desde `backend/`:

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m pytest tests/persistence -m integration --cov=app.models --cov=app.db
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
```

Las pruebas de integración leen TEST_DATABASE_URL del entorno o `.env.test`, nunca usan
DATABASE_URL como alternativa. La suite exige el nombre exacto `trycore_evm_test`, distinto
de la base de desarrollo cuando esta esté configurada. El helper genérico conserva además
la validación del sufijo `_test`. Nunca configurar esa base como entorno de desarrollo.

Cada prueba crea un esquema con UUID dentro de una transacción externa, configura un
search_path local y usa savepoints para que los commits ORM no confirmen esa transacción.
Al terminar se revierte la creación completa del esquema y sus datos; se comprueba que el
esquema desapareció. No se ejecutan DROP DATABASE, DROP TABLE ni TRUNCATE sobre datos existentes.
La inicialización se prueba tanto con el script SQL como con metadata de SQLAlchemy.
Se comparan columnas, tipos, nulabilidad, identidades, PK, FK, CHECK e índices mediante
introspección real, y se prueba que repetir el SQL conserva una fila existente.

Sin TEST_DATABASE_URL, las pruebas PostgreSQL se omiten expresamente. Con una URL configurada,
los fallos de conexión, versión o permisos fallan la suite; no se ocultan como omisiones.
La suite exige PostgreSQL 17. La cobertura de líneas sin integración no demuestra persistencia.
