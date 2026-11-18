import { describe, expect, it } from "vitest";
import {
  formatDecimal,
  formatMoney,
  validateActivity,
  validateProject,
} from "../utils/decimal";

const valid = {
  name: "Actividad",
  bac: "100",
  actual_cost: "0",
  planned_progress_pct: "80",
  actual_progress_pct: "0",
};
describe("Decimal presentation and validation", () => {
  it.each([
    ["99999999999999.99", "99.999.999.999.999,99"],
    ["60000000", "60.000.000,00"],
    ["-7272727.27272727272727", "−7.272.727,27"],
    ["1.005", "1,01"],
    ["9.999", "10,00"],
    ["1E+7", "10.000.000,00"],
    ["1E-3", "0,00"],
  ])("formats %s without binary float conversion", (value, expected) =>
    expect(formatDecimal(value)).toBe(expected),
  );
  it("distinguishes null from zero and preserves source", () => {
    expect(formatMoney(null)).toBe("No calculable");
    expect(formatMoney("0")).toBe("$ 0,00");
    const original = "0.89189189189189189189";
    expect(formatDecimal(original, 4)).toBe("0,8919");
    expect(original).toBe("0.89189189189189189189");
  });
  it.each([
    ["bac", "-1"],
    ["bac", "100000000000000"],
    ["bac", "0.001"],
    ["bac", "NaN"],
    ["actual_cost", ""],
    ["planned_progress_pct", "100.01"],
    ["actual_progress_pct", "-0.01"],
  ])("rejects invalid %s=%s", (key, value) =>
    expect(validateActivity({ ...valid, [key]: value })[key]).toBeTruthy(),
  );
  it("accepts exact limits and comma decimals", () => {
    expect(
      validateActivity({
        ...valid,
        bac: "99999999999999.99",
        actual_progress_pct: "100",
        actual_cost: "1,2300",
      }),
    ).toEqual({});
    expect(validateProject({ name: "   " }).name).toBeTruthy();
    expect(validateProject({ name: "a".repeat(151) }).name).toBeTruthy();
  });
});
