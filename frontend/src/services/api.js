const baseUrl = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "");
const fieldNames = {
  name: "Nombre",
  description: "Descripción",
  bac: "BAC",
  planned_progress_pct: "Avance planificado",
  actual_progress_pct: "Avance real",
  actual_cost: "Costo ejecutado",
};

export class ApiError extends Error {
  constructor(message, status, fields = {}) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.fields = fields;
  }
}

async function request(path, { body, signal, method = "GET" } = {}) {
  let response;
  try {
    response = await fetch(`${baseUrl}/api${path}`, {
      method,
      signal,
      headers: body ? { "Content-Type": "application/json" } : undefined,
      body: body ? JSON.stringify(body) : undefined,
    });
  } catch (error) {
    if (error.name === "AbortError") throw error;
    throw new ApiError(
      "No se pudo conectar con la API. Comprueba que el backend esté en ejecución.",
      0,
    );
  }
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    const fields = {};
    if (Array.isArray(payload.detail)) {
      for (const issue of payload.detail) {
        const field = issue.loc?.at(-1);
        if (fieldNames[field])
          fields[field] =
            `${fieldNames[field]}: revisa el valor, su rango y los decimales permitidos.`;
      }
    }
    const messages = {
      404: "El recurso ya no existe o no pertenece al proyecto. Actualiza la vista.",
      422: "No se pudo guardar. Revisa los campos y las restricciones indicadas.",
      503: "La base de datos no está disponible. Inténtalo de nuevo más tarde.",
    };
    throw new ApiError(
      messages[response.status] ||
        "La solicitud no pudo completarse. Inténtalo de nuevo.",
      response.status,
      fields,
    );
  }
  if (response.status === 204) return null;
  return response.json();
}

const projectPath = (id) => `/projects/${encodeURIComponent(id)}`;
const activityPath = (projectId, id) =>
  `${projectPath(projectId)}/activities${id == null ? "" : `/${encodeURIComponent(id)}`}`;

export const api = {
  listProjects: (signal) => request("/projects", { signal }),
  createProject: (body) => request("/projects", { method: "POST", body }),
  updateProject: (id, body) =>
    request(projectPath(id), { method: "PUT", body }),
  deleteProject: (id) => request(projectPath(id), { method: "DELETE" }),
  listActivities: (id, signal) => request(activityPath(id), { signal }),
  createActivity: (projectId, body) =>
    request(activityPath(projectId), { method: "POST", body }),
  updateActivity: (projectId, id, body) =>
    request(activityPath(projectId, id), { method: "PUT", body }),
  deleteActivity: (projectId, id) =>
    request(activityPath(projectId, id), { method: "DELETE" }),
  projectEvm: (id, signal) => request(`${projectPath(id)}/evm`, { signal }),
  activityEvm: (projectId, id, signal) =>
    request(`${activityPath(projectId, id)}/evm`, { signal }),
};
