import { expect, it, vi } from "vitest";
import { api } from "../services/api";

it("sends strings to the exact nested endpoint and handles 204", async () => {
  const fetch = vi.fn().mockResolvedValue({ ok: true, status: 204 });
  vi.stubGlobal("fetch", fetch);
  const body = { name: "Analysis", bac: "99999999999999.99" };
  await api.updateActivity(2, 3, body);
  expect(fetch).toHaveBeenCalledWith(
    "/api/projects/2/activities/3",
    expect.objectContaining({ method: "PUT", body: JSON.stringify(body) }),
  );
  expect(await api.deleteProject(2)).toBeNull();
});
it("translates 422 into field errors without exposing backend details", async () => {
  vi.stubGlobal(
    "fetch",
    vi
      .fn()
      .mockResolvedValue({
        ok: false,
        status: 422,
        json: async () => ({
          detail: [{ loc: ["body", "bac"], msg: "private backend detail" }],
        }),
      }),
  );
  await expect(api.createActivity(1, {})).rejects.toMatchObject({
    status: 422,
    fields: { bac: expect.stringContaining("BAC") },
  });
});
it("handles network errors and preserves aborts", async () => {
  const fetch = vi
    .fn()
    .mockRejectedValueOnce(new Error("offline"))
    .mockRejectedValueOnce(new DOMException("Aborted", "AbortError"));
  vi.stubGlobal("fetch", fetch);
  await expect(api.listProjects()).rejects.toThrow("No se pudo conectar");
  await expect(api.listProjects()).rejects.toMatchObject({
    name: "AbortError",
  });
});
