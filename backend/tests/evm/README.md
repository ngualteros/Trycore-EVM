# Pruebas del motor EVM

Desde `backend/`, ejecutar la suite específica con cobertura de líneas y ramas:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/evm --cov-reset --cov=app.evm --cov-config=tests/evm/.coveragerc --cov-report=term-missing
```

La configuración exige 100% de cobertura del motor, sin cambiar la configuración
de las pruebas del resto del backend. Los importes deben expresarse en la misma
unidad; los datos del caso obligatorio están en millones.

La API acepta `ActivityInput` con cuatro valores `Decimal`. Rechaza otros tipos,
valores no finitos, importes negativos y porcentajes fuera de 0–100. Los índices
indefinidos y sus interpretaciones son `None`; un índice cero es desfavorable.

No se redondean ni cuantizan valores explícitamente. Se respeta el contexto
`Decimal` del llamador; las divisiones periódicas tienen su precisión finita.
Las pruebas usan contextos locales y tolerancias decimales estrictas para esas
divisiones, sin convertir los resultados a `float`.
