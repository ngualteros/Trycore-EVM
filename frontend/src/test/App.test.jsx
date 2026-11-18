import { act, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, expect, it, vi } from "vitest";
import App from "../App";
import { api, ApiError } from "../services/api";

vi.mock("../services/api", async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual,
    api: Object.fromEntries(
      Object.keys(actual.api).map((key) => [key, vi.fn()]),
    ),
  };
});
const project = {
  id: 1,
  name: "Plataforma corporativa",
  description: "Proyecto de referencia",
};
const empty = {
  bac: "0",
  pv: "0",
  ev: "0",
  ac: "0",
  cv: "0",
  sv: "0",
  cpi: null,
  spi: null,
  eac: null,
  vac: null,
  cpi_interpretation: null,
  spi_interpretation: null,
};
const metrics = {
  bac: "60000000",
  pv: "35000000",
  ev: "33000000",
  ac: "37000000",
  cv: "-4000000",
  sv: "-2000000",
  cpi: "0.89189189189189189189",
  spi: "0.94285714285714285714",
  eac: "67272727.272727272727",
  vac: "-7272727.272727272727",
  cpi_interpretation: "desfavorable",
  spi_interpretation: "desfavorable",
};
const activity = {
  id: 10,
  project_id: 1,
  name: "Análisis",
  bac: "10000000",
  planned_progress_pct: "80",
  actual_progress_pct: "100",
  actual_cost: "9000000",
};
const activityMetrics = {
  ...empty,
  bac: "10000000",
  pv: "8000000",
  ev: "10000000",
  ac: "9000000",
  cv: "1000000",
  sv: "2000000",
  cpi: "1.111111111111111",
  spi: "1.25",
  eac: "9000000",
  vac: "1000000",
  cpi_interpretation: "favorable",
  spi_interpretation: "favorable",
};

beforeEach(() => {
  Object.values(api).forEach((mock) => mock.mockReset());
  api.listProjects.mockResolvedValue([project]);
  api.listActivities.mockResolvedValue([]);
  api.projectEvm.mockResolvedValue(empty);
  api.activityEvm.mockResolvedValue(activityMetrics);
});

it("renders empty activities and null indicators without treating them as zero", async () => {
  render(<App />);
  expect(
    await screen.findByRole("heading", { name: "Plataforma corporativa" }),
  ).toBeInTheDocument();
  expect(await screen.findByText("Aún no hay actividades")).toBeInTheDocument();
  expect(screen.getAllByText("No calculable").length).toBeGreaterThan(2);
  expect(api.projectEvm).toHaveBeenCalledTimes(1);
  expect(api.activityEvm).not.toHaveBeenCalled();
});
it("handles an empty portfolio and creates a project", async () => {
  api.listProjects.mockResolvedValue([]);
  api.createProject.mockResolvedValue(project);
  const user = userEvent.setup();
  render(<App />);
  await user.click(
    await screen.findByRole("button", { name: "+ Crear primer proyecto" }),
  );
  await user.type(screen.getByLabelText("Nombre"), project.name);
  await user.click(screen.getByRole("button", { name: "Guardar" }));
  expect(
    await screen.findByRole("heading", { name: project.name }),
  ).toBeInTheDocument();
  expect(api.createProject).toHaveBeenCalledWith({
    name: project.name,
    description: null,
  });
});
it("renders network errors and retries", async () => {
  api.listProjects.mockRejectedValueOnce(
    new ApiError("No se pudo conectar con la API.", 0),
  );
  const user = userEvent.setup();
  render(<App />);
  expect(await screen.findByRole("alert")).toHaveTextContent(
    "No se pudo conectar",
  );
  await user.click(
    screen.getByRole("button", { name: "Reintentar proyectos" }),
  );
  expect(
    await screen.findByRole("heading", { name: project.name }),
  ).toBeInTheDocument();
});
it("validates forms and refreshes table, metrics and chart after creating an activity", async () => {
  const user = userEvent.setup();
  render(<App />);
  await screen.findByText("Aún no hay actividades");
  await user.click(screen.getByRole("button", { name: "+ Nueva actividad" }));
  await user.click(screen.getByRole("button", { name: "Guardar" }));
  expect(screen.getByText("Escribe un nombre.")).toBeInTheDocument();
  expect(api.createActivity).not.toHaveBeenCalled();
  await user.type(screen.getByLabelText("Nombre"), "Análisis");
  for (const [label, value] of [
    ["Presupuesto total (BAC) COP", "10000000"],
    ["Avance planificado %", "80"],
    ["Avance real %", "100"],
    ["Costo ejecutado (AC) COP", "9000000"],
  ]) {
    await user.type(screen.getByLabelText(label), value);
  }
  api.createActivity.mockResolvedValue(activity);
  api.listActivities.mockResolvedValue([activity]);
  api.projectEvm.mockResolvedValue(metrics);
  await user.click(screen.getByRole("button", { name: "Guardar" }));
  expect(
    await screen.findByRole("rowheader", { name: "Análisis" }),
  ).toBeInTheDocument();
  expect(screen.getByText("$ 60.000.000,00")).toBeInTheDocument();
  expect(screen.getByText("0,8919")).toBeInTheDocument();
  expect(
    screen.getByRole("img", { name: /Comparación de PV/ }),
  ).toHaveTextContent("$ 8.000.000,00");
  expect(api.createActivity).toHaveBeenCalledWith(1, {
    name: "Análisis",
    bac: "10000000",
    planned_progress_pct: "80",
    actual_progress_pct: "100",
    actual_cost: "9000000",
  });
  expect(api.listActivities).toHaveBeenCalledTimes(2);
  expect(api.projectEvm).toHaveBeenCalledTimes(2);
});
it("edits and deletes an activity only after confirmation, then reloads indicators", async () => {
  api.listActivities.mockResolvedValue([activity]);
  api.projectEvm.mockResolvedValue(activityMetrics);
  const user = userEvent.setup();
  render(<App />);
  await user.click(
    await screen.findByRole("button", { name: "Editar actividad Análisis" }),
  );
  await user.clear(screen.getByLabelText("Costo ejecutado (AC) COP"));
  await user.type(screen.getByLabelText("Costo ejecutado (AC) COP"), "9500000");
  api.updateActivity.mockResolvedValue({ ...activity, actual_cost: "9500000" });
  api.listActivities.mockResolvedValue([
    { ...activity, actual_cost: "9500000" },
  ]);
  api.projectEvm.mockResolvedValue({ ...activityMetrics, ac: "9500000" });
  await user.click(screen.getByRole("button", { name: "Guardar" }));
  await waitFor(() =>
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument(),
  );
  await user.click(
    await screen.findByRole("button", { name: "Eliminar actividad Análisis" }),
  );
  expect(api.deleteActivity).not.toHaveBeenCalled();
  await user.click(screen.getByRole("button", { name: "Cancelar" }));
  expect(api.deleteActivity).not.toHaveBeenCalled();
  await user.click(
    screen.getByRole("button", { name: "Eliminar actividad Análisis" }),
  );
  api.deleteActivity.mockResolvedValue(null);
  api.listActivities.mockResolvedValue([]);
  api.projectEvm.mockResolvedValue(empty);
  await user.click(
    screen.getByRole("button", { name: "Confirmar eliminación" }),
  );
  expect(await screen.findByText("Aún no hay actividades")).toBeInTheDocument();
  expect(api.deleteActivity).toHaveBeenCalledWith(1, 10);
});
it("shows 422 errors in the form and keeps entered values", async () => {
  api.createProject.mockRejectedValue(
    new ApiError("Revisa los campos.", 422, { name: "Nombre inválido." }),
  );
  const user = userEvent.setup();
  render(<App />);
  await user.click(screen.getByRole("button", { name: "+ Nuevo proyecto" }));
  await user.type(screen.getByLabelText("Nombre"), "Duplicado");
  await user.click(screen.getByRole("button", { name: "Guardar" }));
  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Revisa los campos",
  );
  expect(screen.getByLabelText("Nombre")).toHaveValue("Duplicado");
  expect(screen.getByText("Nombre inválido.")).toBeInTheDocument();
});
it("edits and deletes projects with explicit cascade confirmation", async () => {
  const user = userEvent.setup();
  render(<App />);
  await user.click(
    await screen.findByRole("button", { name: "Editar proyecto" }),
  );
  await user.clear(screen.getByLabelText("Nombre"));
  await user.type(screen.getByLabelText("Nombre"), "Actualizado");
  api.updateProject.mockResolvedValue({ ...project, name: "Actualizado" });
  await user.click(screen.getByRole("button", { name: "Guardar" }));
  expect(
    await screen.findByRole("heading", { name: "Actualizado" }),
  ).toBeInTheDocument();
  await user.click(screen.getByRole("button", { name: "Eliminar proyecto" }));
  expect(screen.getByRole("dialog")).toHaveTextContent(
    "También se eliminarán todas sus actividades",
  );
  expect(api.deleteProject).not.toHaveBeenCalled();
  api.deleteProject.mockResolvedValue(null);
  await user.click(
    screen.getByRole("button", { name: "Confirmar eliminación" }),
  );
  expect(
    await screen.findByRole("heading", {
      name: "Cada proyecto comienza con un plan",
    }),
  ).toBeInTheDocument();
});
it("ignores late responses from a previously selected project", async () => {
  let resolveFirst;
  api.listProjects.mockResolvedValue([project, { id: 2, name: "Segundo" }]);
  api.listActivities.mockImplementation((id) =>
    id === 1
      ? new Promise((resolve) => {
          resolveFirst = resolve;
        })
      : Promise.resolve([]),
  );
  api.projectEvm.mockImplementation((id) =>
    Promise.resolve(id === 1 ? metrics : empty),
  );
  const user = userEvent.setup();
  render(<App />);
  await user.click(await screen.findByRole("button", { name: /Segundo/ }));
  await screen.findByText("Aún no hay actividades");
  await act(async () => resolveFirst([activity]));
  expect(screen.getByRole("heading", { name: "Segundo" })).toBeInTheDocument();
  expect(screen.queryByText("$ 60.000.000,00")).not.toBeInTheDocument();
  expect(
    within(
      screen.getByRole("region", { name: "Indicadores consolidados" }),
    ).getAllByText("No calculable").length,
  ).toBeGreaterThan(0);
});
