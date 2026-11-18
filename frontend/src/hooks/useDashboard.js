import { useCallback, useEffect, useState } from "react";
import { api } from "../services/api";

export function useDashboard() {
  const [projects, setProjects] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [projectsLoadedVersion, setProjectsLoadedVersion] = useState(-1);
  const [projectsError, setProjectsError] = useState("");
  const [projectVersion, setProjectVersion] = useState(0);
  const [detailVersion, setDetailVersion] = useState(0);
  const [detail, setDetail] = useState({
    id: null,
    loading: false,
    activities: [],
    metrics: null,
    error: "",
  });

  useEffect(() => {
    const controller = new AbortController();
    api
      .listProjects(controller.signal)
      .then((items) => {
        if (controller.signal.aborted) return;
        setProjects(items);
        setSelectedId((id) =>
          items.some((item) => item.id === id) ? id : (items[0]?.id ?? null),
        );
      })
      .catch((error) => {
        if (!controller.signal.aborted) setProjectsError(error.message);
      })
      .finally(() => {
        if (!controller.signal.aborted)
          setProjectsLoadedVersion(projectVersion);
      });
    return () => controller.abort();
  }, [projectVersion]);

  useEffect(() => {
    if (selectedId == null) return;
    const controller = new AbortController();
    async function load() {
      try {
        const [activities, metrics] = await Promise.all([
          api.listActivities(selectedId, controller.signal),
          api.projectEvm(selectedId, controller.signal),
        ]);
        if (controller.signal.aborted) return;
        const rows = await Promise.all(
          activities.map(async (activity) => ({
            ...activity,
            evm: await api.activityEvm(
              selectedId,
              activity.id,
              controller.signal,
            ),
          })),
        );
        if (!controller.signal.aborted)
          setDetail({
            id: selectedId,
            version: detailVersion,
            loading: false,
            activities: rows,
            metrics,
            error: "",
          });
      } catch (error) {
        if (!controller.signal.aborted)
          setDetail({
            id: selectedId,
            version: detailVersion,
            loading: false,
            activities: [],
            metrics: null,
            error: error.message,
          });
      }
    }
    load();
    return () => controller.abort();
  }, [selectedId, detailVersion]);

  const refreshDetails = useCallback(
    () => setDetailVersion((value) => value + 1),
    [],
  );
  const refreshProjects = useCallback(() => {
    setProjectsError("");
    setProjectVersion((value) => value + 1);
  }, []);
  const saveProject = (project) => {
    setProjects((items) =>
      items.some((item) => item.id === project.id)
        ? items.map((item) => (item.id === project.id ? project : item))
        : [...items, project],
    );
    setSelectedId(project.id);
  };
  const removeProject = (id) => {
    const remaining = projects.filter((item) => item.id !== id);
    setProjects(remaining);
    setSelectedId(remaining[0]?.id ?? null);
  };
  const currentDetail =
    detail.id === selectedId && detail.version === detailVersion
      ? detail
      : {
          activities: [],
          metrics: null,
          error: "",
          loading: selectedId != null,
        };
  return {
    projects,
    selectedId,
    setSelectedId,
    projectsLoading: projectsLoadedVersion !== projectVersion,
    projectsError,
    refreshProjects,
    project: projects.find((item) => item.id === selectedId),
    ...currentDetail,
    refreshDetails,
    saveProject,
    removeProject,
  };
}
