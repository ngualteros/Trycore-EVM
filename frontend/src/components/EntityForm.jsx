import { useState } from "react";
import Modal from "./Modal";
import {
  normalizeDecimal,
  validateActivity,
  validateProject,
} from "../utils/decimal";

const numericFields = [
  ["bac", "Presupuesto total (BAC)", "COP"],
  ["planned_progress_pct", "Avance planificado", "%"],
  ["actual_progress_pct", "Avance real", "%"],
  ["actual_cost", "Costo ejecutado (AC)", "COP"],
];

export default function EntityForm({ kind, initial, onSave, onClose }) {
  const isActivity = kind === "activity";
  const [values, setValues] = useState(() => ({
    name: initial?.name ?? "",
    description: initial?.description ?? "",
    ...Object.fromEntries(
      numericFields.map(([key]) => [key, initial?.[key] ?? ""]),
    ),
  }));
  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const title = `${initial ? "Editar" : isActivity ? "Nueva" : "Nuevo"} ${isActivity ? "actividad" : "proyecto"}`;
  function change(event) {
    const { name, value } = event.target;
    setValues((current) => ({ ...current, [name]: value }));
    setErrors((current) => ({ ...current, [name]: undefined }));
  }
  async function submit(event) {
    event.preventDefault();
    if (busy) return;
    const validation = isActivity
      ? validateActivity(values)
      : validateProject(values);
    setErrors(validation);
    setMessage("");
    if (Object.keys(validation).length) return;
    const body = isActivity
      ? {
          name: values.name,
          ...Object.fromEntries(
            numericFields.map(([key]) => [key, normalizeDecimal(values[key])]),
          ),
        }
      : { name: values.name, description: values.description || null };
    setBusy(true);
    try {
      await onSave(body);
    } catch (error) {
      setMessage(error.message);
      setErrors(error.fields || {});
      setBusy(false);
    }
  }
  function field(name, label, suffix) {
    return (
      <div className="form-field" key={name}>
        <label htmlFor={`field-${name}`}>
          {label}
          {suffix && <span> {suffix}</span>}
        </label>
        <input
          id={`field-${name}`}
          name={name}
          value={values[name]}
          onChange={change}
          inputMode={suffix ? "decimal" : "text"}
          maxLength={suffix ? 40 : 150}
          required
          aria-invalid={!!errors[name]}
          aria-describedby={errors[name] ? `error-${name}` : undefined}
        />
        {errors[name] && (
          <p className="field-error" id={`error-${name}`}>
            {errors[name]}
          </p>
        )}
      </div>
    );
  }
  return (
    <Modal title={title} onClose={onClose} busy={busy}>
      <form onSubmit={submit} noValidate>
        {message && (
          <div className="notice error" role="alert">
            {message}
          </div>
        )}
        {field("name", "Nombre")}
        {isActivity ? (
          <>
            <p className="form-hint">
              Sin separadores de miles. Máximo dos decimales; puedes usar punto
              o coma decimal.
            </p>
            <div className="form-grid">
              {numericFields.map(([key, label, suffix]) =>
                field(key, label, suffix),
              )}
            </div>
          </>
        ) : (
          <div className="form-field">
            <label htmlFor="field-description">
              Descripción <span>opcional</span>
            </label>
            <textarea
              id="field-description"
              name="description"
              value={values.description}
              onChange={change}
              rows="3"
            />
          </div>
        )}
        <div className="modal-actions">
          <button
            type="button"
            className="button secondary"
            onClick={onClose}
            disabled={busy}
          >
            Cancelar
          </button>
          <button className="button primary" disabled={busy}>
            {busy ? "Guardando…" : "Guardar"}
          </button>
        </div>
      </form>
    </Modal>
  );
}
