import { formatDecimal, formatMoney } from "../utils/decimal";

const definitions = [
  ["bac", "Presupuesto total", "Base aprobada"],
  ["pv", "Valor planificado", "Trabajo previsto"],
  ["ev", "Valor ganado", "Trabajo realizado"],
  ["ac", "Costo ejecutado", "Inversión real"],
  ["cv", "Variación de costo", "EV − AC"],
  ["sv", "Variación de plazo", "EV − PV"],
  ["cpi", "Eficiencia de costo", "Índice CPI"],
  ["spi", "Eficiencia de plazo", "Índice SPI"],
  ["eac", "Costo estimado final", "Proyección al cierre"],
  ["vac", "Variación al cierre", "BAC − EAC"],
];

export function IndicatorStatus({ value }) {
  const labels = {
    favorable: "Favorable",
    desfavorable: "Desfavorable",
    "según lo previsto": "Según lo previsto",
  };
  const tone =
    value === "favorable"
      ? "positive"
      : value === "desfavorable"
        ? "negative"
        : "neutral";
  return (
    <span className={`badge ${tone}`}>
      <span aria-hidden="true">●</span> {labels[value] || "No calculable"}
    </span>
  );
}

export default function Metrics({ metrics }) {
  return (
    <section aria-label="Indicadores consolidados" className="metrics-grid">
      {definitions.map(([key, label, hint]) => {
        const isIndex = key === "cpi" || key === "spi";
        const value = metrics[key];
        return (
          <article className={`metric-card metric-${key}`} key={key}>
            <div className="metric-top">
              <h3>{label}</h3>
              <span>{key.toUpperCase()}</span>
            </div>
            <p
              className={`metric-value ${value?.startsWith("-") ? "negative-value" : ""}`}
              title={value == null ? "No calculable" : `Valor API: ${value}`}
            >
              {isIndex ? formatDecimal(value, 4) : formatMoney(value)}
            </p>
            {isIndex ? (
              <IndicatorStatus value={metrics[`${key}_interpretation`]} />
            ) : (
              <p className="metric-hint">{hint}</p>
            )}
          </article>
        );
      })}
    </section>
  );
}
