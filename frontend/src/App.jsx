import { useState } from "react";
import { api } from "./services/api";
import { useDashboard } from "./hooks/useDashboard";
import EntityForm from "./components/EntityForm";
import ConfirmDelete from "./components/ConfirmDelete";
import Metrics from "./components/Metrics";
import ActivityTable from "./components/ActivityTable";
import EvmChart from "./components/EvmChart";

export default function App() {
  const dashboard = useDashboard();
  const [dialog, setDialog] = useState(null);
  const [success, setSuccess] = useState("");
  const { project, activities, metrics, loading, error } = dashboard;
  const close = () => setDialog(null);
  const open = (value) => {
    setSuccess("");
    setDialog(value);
  };
  async function save(body) {
    if (dialog.kind === "project") {
      const saved = dialog.initial
        ? await api.updateProject(dialog.initial.id, body)
        : await api.createProject(body);
      dashboard.saveProject(saved);
    } else {
      if (dialog.initial)
        await api.updateActivity(dialog.projectId, dialog.initial.id, body);
      else await api.createActivity(dialog.projectId, body);
      dashboard.refreshDetails();
    }
    setSuccess(
      dialog.initial
        ? "Cambios guardados correctamente."
        : "Registro creado correctamente.",
    );
    close();
  }
  async function remove() {
    if (dialog.kind === "project") {
      await api.deleteProject(dialog.initial.id);
      dashboard.removeProject(dialog.initial.id);
    } else {
      await api.deleteActivity(dialog.projectId, dialog.initial.id);
      dashboard.refreshDetails();
    }
    setSuccess("Registro eliminado correctamente.");
    close();
  }
  return (
    <div className="app-shell">
      <a className="skip-link" href="#workspace">
        Saltar al contenido
      </a>
      <aside className="sidebar" aria-label="Navegación de proyectos">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true">
            T
          </span>
          <div>
            TRYCORE<span>PROJECT INTELLIGENCE</span>
          </div>
        </div>
        <div className="sidebar-heading">
          <span>PORTAFOLIO</span>
          <span className="count">{dashboard.projects.length}</span>
        </div>
        <button
          className="button sidebar-create"
          onClick={() => open({ kind: "project" })}
        >
          + Nuevo proyecto
        </button>
        {dashboard.projectsLoading && (
          <p className="sidebar-message" role="status">
            Cargando proyectos…
          </p>
        )}
        {dashboard.projectsError && (
          <div className="sidebar-message" role="alert">
            <p>{dashboard.projectsError}</p>
            <button
              className="button secondary"
              onClick={dashboard.refreshProjects}
            >
              Reintentar proyectos
            </button>
          </div>
        )}
        {!dashboard.projectsLoading &&
          !dashboard.projectsError &&
          dashboard.projects.length === 0 && (
            <p className="sidebar-message">Tu portafolio está vacío.</p>
          )}
        <nav aria-label="Proyectos" className="project-list">
          {dashboard.projects.map((item) => (
            <button
              key={item.id}
              aria-current={
                item.id === dashboard.selectedId ? "page" : undefined
              }
              onClick={() => {
                dashboard.setSelectedId(item.id);
                setSuccess("");
              }}
            >
              <span className="project-icon" aria-hidden="true">
                ▧
              </span>
              <span>{item.name}</span>
              <span className="nav-arrow" aria-hidden="true">
                ›
              </span>
            </button>
          ))}
        </nav>
        <div className="sidebar-footer">
          <span className="footer-line" />
          Earned Value Management
          <p>Presupuesto, avance y resultados en una sola vista.</p>
        </div>
      </aside>
      <div className="workspace">
        <header className="topbar">
          <span>
            Gestión de proyectos <span className="breadcrumb">/ Dashboard</span>
          </span>
          <span className="workspace-label">CONTROL EVM</span>
        </header>
        <main id="workspace">
          {success && (
            <div className="notice success" role="status">
              {success}
              <button
                aria-label="Cerrar mensaje"
                onClick={() => setSuccess("")}
              >
                ×
              </button>
            </div>
          )}
          {!project ? (
            <section className="welcome panel">
              <span className="welcome-icon" aria-hidden="true">
                ▧
              </span>
              <p className="eyebrow">Tu centro de control</p>
              <h1>
                {dashboard.projectsLoading
                  ? "Preparando tu portafolio"
                  : dashboard.projectsError
                    ? "No pudimos cargar los proyectos"
                    : "Cada proyecto comienza con un plan"}
              </h1>
              <p>
                {dashboard.projectsError
                  ? "Comprueba la conexión con el backend y vuelve a intentarlo."
                  : "Crea un proyecto y sus actividades para visualizar el presupuesto, el avance y el desempeño financiero."}
              </p>
              {!dashboard.projectsLoading && (
                <button
                  className="button primary"
                  onClick={() =>
                    dashboard.projectsError
                      ? dashboard.refreshProjects()
                      : open({ kind: "project" })
                  }
                >
                  {dashboard.projectsError
                    ? "Reintentar"
                    : "+ Crear primer proyecto"}
                </button>
              )}
            </section>
          ) : (
            <>
              <div className="page-heading">
                <div>
                  <p className="eyebrow">Resumen del proyecto</p>
                  <h1>{project.name}</h1>
                  <p className="project-description">
                    {project.description ||
                      "Sin descripción. Puedes añadirla al editar el proyecto."}
                  </p>
                </div>
                <div className="heading-actions">
                  <button
                    className="button secondary"
                    onClick={() => open({ kind: "project", initial: project })}
                  >
                    Editar proyecto
                  </button>
                  <button
                    className="button quiet-danger"
                    onClick={() =>
                      open({
                        kind: "project",
                        initial: project,
                        deleting: true,
                      })
                    }
                  >
                    Eliminar proyecto
                  </button>
                </div>
              </div>
              <div className="section-bar">
                <div>
                  <span className="section-dot" />
                  <strong>Desempeño consolidado</strong>
                  <span className="unit-label">Valores en COP</span>
                </div>
                <button
                  className="text-button"
                  disabled={loading}
                  onClick={dashboard.refreshDetails}
                >
                  ↻ Actualizar
                </button>
              </div>
              {loading ? (
                <div className="loading-state panel" role="status">
                  <span className="loading-dot" />
                  Cargando actividades e indicadores…
                </div>
              ) : error ? (
                <div className="notice error" role="alert">
                  <div>
                    <strong>No pudimos actualizar el dashboard</strong>
                    <p>{error}</p>
                  </div>
                  <button
                    className="button secondary"
                    onClick={dashboard.refreshDetails}
                  >
                    Reintentar indicadores
                  </button>
                </div>
              ) : (
                metrics && (
                  <>
                    <Metrics metrics={metrics} />
                    <p className="precision-note">
                      Importes presentados con dos decimales e índices con
                      cuatro. El valor original de la API se conserva.
                    </p>
                    <EvmChart activities={activities} />
                  </>
                )
              )}
              <section
                className="panel activities-panel"
                aria-labelledby="activities-title"
              >
                <div className="panel-heading">
                  <div>
                    <p className="eyebrow">Plan de trabajo</p>
                    <h2 id="activities-title">
                      Actividades{" "}
                      {!loading && !error && (
                        <span className="inline-count">
                          {activities.length}
                        </span>
                      )}
                    </h2>
                  </div>
                  <button
                    className="button primary"
                    disabled={loading || !!error}
                    onClick={() =>
                      open({ kind: "activity", projectId: project.id })
                    }
                  >
                    + Nueva actividad
                  </button>
                </div>
                {loading ? (
                  <p className="empty-inline">Cargando plan de trabajo…</p>
                ) : error ? (
                  <p className="empty-inline">
                    Actualiza los datos para continuar.
                  </p>
                ) : activities.length === 0 ? (
                  <div className="empty-activities">
                    <h3>Aún no hay actividades</h3>
                    <p>
                      Añade la primera actividad para empezar a medir el
                      desempeño de este proyecto.
                    </p>
                  </div>
                ) : (
                  <ActivityTable
                    activities={activities}
                    onEdit={(initial) =>
                      open({ kind: "activity", projectId: project.id, initial })
                    }
                    onDelete={(initial) =>
                      open({
                        kind: "activity",
                        projectId: project.id,
                        initial,
                        deleting: true,
                      })
                    }
                  />
                )}
              </section>
            </>
          )}
          <footer className="page-footer">
            <span>Trycore · Gestión de valor ganado</span>
            <span>Datos e indicadores de la API</span>
          </footer>
        </main>
      </div>
      {dialog &&
        (dialog.deleting ? (
          <ConfirmDelete
            title={`Eliminar ${dialog.kind === "project" ? "proyecto" : "actividad"}`}
            description={`¿Eliminar “${dialog.initial.name}”? ${dialog.kind === "project" ? "También se eliminarán todas sus actividades. " : ""}Esta acción no se puede deshacer.`}
            onConfirm={remove}
            onClose={close}
          />
        ) : (
          <EntityForm
            key={`${dialog.kind}-${dialog.initial?.id ?? "new"}`}
            kind={dialog.kind}
            initial={dialog.initial}
            onSave={save}
            onClose={close}
          />
        ))}
    </div>
  );
}
