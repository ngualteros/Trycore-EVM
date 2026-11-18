import { useState } from "react";
import Modal from "./Modal";

export default function ConfirmDelete({
  title,
  description,
  onConfirm,
  onClose,
}) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  async function confirm() {
    setBusy(true);
    try {
      await onConfirm();
    } catch (failure) {
      setError(failure.message);
      setBusy(false);
    }
  }
  return (
    <Modal title={title} onClose={onClose} busy={busy}>
      <p>{description}</p>
      {error && (
        <div className="notice error" role="alert">
          {error}
        </div>
      )}
      <div className="modal-actions">
        <button className="button secondary" onClick={onClose} disabled={busy}>
          Cancelar
        </button>
        <button className="button danger" onClick={confirm} disabled={busy}>
          {busy ? "Eliminando…" : "Confirmar eliminación"}
        </button>
      </div>
    </Modal>
  );
}
