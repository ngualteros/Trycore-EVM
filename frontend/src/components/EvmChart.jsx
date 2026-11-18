import { formatMoney } from "../utils/decimal";

const series = [
  ["pv", "Valor planificado (PV)", "#526bce"],
  ["ev", "Valor ganado (EV)", "#118675"],
  ["ac", "Costo ejecutado (AC)", "#bd7524"],
];

export default function EvmChart({ activities }) {
  // Number conversion exists only for SVG geometry; financial values stay as API strings.
  const values = activities.flatMap((row) =>
    series.map(([key]) => Number(row.evm[key] ?? 0)),
  );
  const maximum = Math.max(0, ...values);
  const height = Math.max(130, activities.length * 112 + 20);
  return (
    <section className="panel chart-panel" aria-labelledby="chart-title">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Comparación por actividad</p>
          <h2 id="chart-title">Valor planificado, ganado y costo</h2>
        </div>
        <span className="unit-label">COP</span>
      </div>
      <div className="chart-legend">
        {series.map(([key, label, color]) => (
          <span key={key}>
            <i style={{ background: color }} />
            {label}
          </span>
        ))}
      </div>
      {activities.length === 0 ? (
        <p className="empty-inline">
          La gráfica aparecerá cuando agregues la primera actividad.
        </p>
      ) : (
        <div className="chart-scroll">
          <svg
            viewBox={`0 0 860 ${height}`}
            role="img"
            aria-label="Comparación de PV, EV y AC por actividad en pesos colombianos"
            style={{ minWidth: 680 }}
          >
            {[0, 1, 2, 3, 4].map((tick) => (
              <line
                key={tick}
                x1={205 + tick * 125}
                x2={205 + tick * 125}
                y1="0"
                y2={height}
                stroke="#e7ebf1"
              />
            ))}
            {activities.map((activity, index) => (
              <g
                key={activity.id}
                transform={`translate(0 ${index * 112 + 10})`}
              >
                <text x="0" y="43" className="chart-label">
                  <title>{activity.name}</title>
                  {activity.name.length > 24
                    ? activity.name.slice(0, 23) + "…"
                    : activity.name}
                </text>
                {series.map(([key, label, color], seriesIndex) => {
                  const numeric = Number(activity.evm[key] ?? 0);
                  const width = maximum ? (numeric / maximum) * 490 : 0;
                  return (
                    <g
                      key={key}
                      transform={`translate(205 ${seriesIndex * 27})`}
                    >
                      <rect width={width} height="18" rx="3" fill={color}>
                        <title>
                          {activity.name} · {label}:{" "}
                          {formatMoney(activity.evm[key])}
                        </title>
                      </rect>
                      <text x={width + 8} y="13" className="chart-value">
                        {formatMoney(activity.evm[key])}
                      </text>
                    </g>
                  );
                })}
              </g>
            ))}
          </svg>
        </div>
      )}
      <p className="chart-note">
        Comparación del estado actual, no una serie temporal. Importes
        calculados por FastAPI.
      </p>
    </section>
  );
}
