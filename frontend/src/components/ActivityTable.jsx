import { formatDecimal, formatMoney } from "../utils/decimal";

export default function ActivityTable({ activities, onEdit, onDelete }) {
  return (
    <div
      className="table-scroll"
      role="region"
      aria-label="Tabla de actividades, desplazamiento horizontal disponible"
      tabIndex="0"
    >
      <table>
        <caption className="sr-only">
          Actividades e indicadores individuales calculados por la API
        </caption>
        <thead>
          <tr>
            {[
              "Actividad",
              "BAC",
              "Planificado",
              "Real",
              "AC",
              "PV",
              "EV",
              "CV",
              "SV",
              "CPI",
              "SPI",
              "Acciones",
            ].map((label) => (
              <th key={label} scope="col">
                {label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {activities.map((activity) => (
            <tr key={activity.id}>
              <th scope="row">{activity.name}</th>
              <td>{formatMoney(activity.bac)}</td>
              <td>{formatDecimal(activity.planned_progress_pct)} %</td>
              <td>{formatDecimal(activity.actual_progress_pct)} %</td>
              <td>{formatMoney(activity.actual_cost)}</td>
              {["pv", "ev", "cv", "sv", "cpi", "spi"].map((key) => (
                <td
                  key={key}
                  title={activity.evm[key] ?? "No calculable"}
                  className={
                    activity.evm[key]?.startsWith("-") ? "negative-value" : ""
                  }
                >
                  {key === "cpi" || key === "spi"
                    ? formatDecimal(activity.evm[key], 4)
                    : formatMoney(activity.evm[key])}
                </td>
              ))}
              <td>
                <div className="row-actions">
                  <button
                    onClick={() => onEdit(activity)}
                    aria-label={`Editar actividad ${activity.name}`}
                  >
                    Editar
                  </button>
                  <button
                    className="delete-link"
                    onClick={() => onDelete(activity)}
                    aria-label={`Eliminar actividad ${activity.name}`}
                  >
                    Eliminar
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
