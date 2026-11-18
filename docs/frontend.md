# Dashboard React

React + Vite con JavaScript/JSX. `src/services/api.js` centraliza las solicitudes a los
endpoints existentes; `useDashboard` coordina selección, carga, cancelación y actualización.
Los componentes separan formularios, confirmaciones, tarjetas EVM, tabla y gráfica SVG.
No se añade una librería de gráficas ni se calculan fórmulas EVM en JavaScript.

## Ejecución local en Windows

Configurar la base de **desarrollo**, sus tablas y `backend/.env` siguiendo
[database.md](database.md). No utilizar `trycore_evm_test` para el trabajo habitual.
Desde la raíz, en una terminal:

```powershell
Set-Location backend
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

En otra terminal, desde la raíz:

```powershell
Set-Location frontend
npm.cmd ci
npm.cmd run dev -- --port 5173 --strictPort
```

Abrir **http://127.0.0.1:5173/**. No es obligatorio crear un `.env` frontend con los valores
predeterminados. Si ya existe, comprobar que `VITE_API_BASE_URL` esté vacío para usar el proxy:

```dotenv
VITE_API_BASE_URL=
API_PROXY_TARGET=http://127.0.0.1:8000
```

El navegador solicita `/api/...` al mismo origen y Vite lo reenvía al backend. No se
necesitan cambios CORS en FastAPI. `VITE_API_BASE_URL`, cuando se usa, es un origen público
sin `/api` al final; nunca debe contener credenciales. Reiniciar Vite tras cambiar el entorno.

El proxy es de desarrollo. Para desplegar `dist/`, el servidor debe reenviar `/api` a FastAPI
en el mismo origen, o configurarse explícitamente otro origen y su CORS. `vite preview` no
es un servidor de producción. Las fuentes externas tienen alternativas tipográficas locales.

## Datos y precisión

- Los formularios envían los decimales como cadenas. Admiten punto o coma decimal, sin
  separadores de miles; rechazan negativos, más de dos decimales significativos, porcentajes
  superiores a 100 e importes superiores a 99999999999999.99.
- La API es la fuente de los indicadores individuales y consolidados. El frontend conserva
  las cadenas originales; el formateador usa operaciones de texto y BigInt para presentar
  COP con dos decimales e índices con cuatro. Este redondeo es solo visual.
- `null` se presenta como «No calculable», nunca como cero. La gráfica convierte a Number
  exclusivamente para dimensiones SVG; los rótulos usan las cadenas originales.
- Al seleccionar o actualizar un proyecto se consulta su lista de actividades, su EVM
  consolidado y un EVM por actividad. No hay polling. AbortController evita aplicar
  respuestas de una selección anterior. Para portafolios muy grandes, la API actual
  implica N solicitudes EVM individuales; una optimización futura requiere otro contrato.

## Comprobación del caso de referencia

En un proyecto nuevo de demostración, crear «Implementación de plataforma corporativa»
y añadir las siguientes actividades (escribir los importes sin puntos de miles):

| Actividad | BAC | Planificado | Real | AC |
| --- | ---: | ---: | ---: | ---: |
| Análisis | 10000000 | 80 | 100 | 9000000 |
| Desarrollo | 20000000 | 60 | 40 | 12000000 |
| Pruebas | 30000000 | 50 | 50 | 16000000 |

Comprobar BAC 60.000.000, PV 35.000.000, EV 33.000.000, AC 37.000.000, CV −4.000.000,
SV −2.000.000, CPI 0,8919, SPI 0,9429, EAC 67.272.727,27 y VAC −7.272.727,27.
Los últimos cuatro son presentaciones redondeadas de las cadenas de FastAPI. Ediciones
y eliminaciones deben actualizar tabla, tarjetas y gráfica. Las eliminaciones requieren
confirmación, incluyendo la advertencia de cascada al eliminar un proyecto.

## Pruebas

Desde `frontend/`:

```powershell
npm.cmd test
npm.cmd run lint
npm.cmd run build
```

Vitest, Testing Library y jsdom son dependencias de desarrollo para probar componentes,
formularios, estados, contratos HTTP y precisión. La prueba real está separada de la suite
simulada para impedir conexiones accidentales a una API de desarrollo.

Para ejecutar el caso de referencia mediante React y FastAPI **reales** en aislamiento:

1. Configurar `backend/.env.test` con TEST_DATABASE_URL hacia `trycore_evm_test`.
2. Desde la raíz, mantener abierta esta terminal:

```powershell
.\backend\.venv\Scripts\python.exe -u frontend/scripts/test_api_server.py
```

3. En otra terminal desde `frontend/`, ejecutar:

```powershell
$env:API_PROXY_TARGET='http://127.0.0.1:18001'
npm.cmd run dev -- --port 5174 --strictPort
```

4. Desde una tercera terminal en `frontend/`:

```powershell
npm.cmd exec -- vitest run --config vite.live.config.js
```

El helper verifica el nombre de la base, crea exclusivamente un esquema nuevo con UUID y
usa sesiones restringidas a él. La prueba llena los formularios y verifica el caso empresarial
sin respuestas simuladas. Iniciar un helper nuevo para cada ejecución: requiere un portafolio
vacío. Al terminar, pulsar **Enter** en la terminal del helper para detenerlo y eliminar solo
su esquema temporal; detener el Vite de pruebas con Ctrl+C. No cerrar a la fuerza el helper,
porque impediría su limpieza. No se usan datos de desarrollo ni se añaden endpoints al backend.

## Riesgos conocidos

La auditoría del 2026-11-18 reporta seis avisos altos derivados de picomatch
(GHSA-fc5q-39xc-vjpf): picomatch, fdir, tinyglobby, Vite, plugin React y Vitest. Afectan la
cadena de desarrollo/compilación/pruebas; `npm audit --omit=dev` reporta cero vulnerabilidades.
El riesgo es consumo excesivo de CPU al procesar patrones glob maliciosos. No se identifica
una ruta de entrada de esos patrones desde los formularios del dashboard. Los avisos siguen
abiertos: no se aplicaron cambios mayores automáticos ni `audit fix --force`. Mantener las
herramientas locales y no ejecutar configuraciones/patrones no confiables.
