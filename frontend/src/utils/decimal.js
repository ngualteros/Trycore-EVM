// Display-only decimal rounding. Source strings are never replaced or converted to float.
export function formatDecimal(value, places = 2) {
  if (value == null) return "No calculable";
  const match = String(value).match(
    /^(-?)(\d+)(?:\.(\d*))?(?:[eE]([+-]?\d+))?$/,
  );
  if (!match) return "Valor no disponible";
  const [, sign, integer, fraction = "", exponent = "0"] = match;
  const digits = integer + fraction;
  const point = integer.length + Number(exponent);
  const whole = point <= 0 ? "0" : digits.slice(0, point).padEnd(point, "0");
  const decimals =
    point < 0 ? "0".repeat(-point) + digits : digits.slice(Math.max(0, point));
  const retained = decimals.padEnd(places + 1, "0");
  let scaled =
    BigInt(whole || "0") * 10n ** BigInt(places) +
    BigInt(retained.slice(0, places) || "0");
  if (retained[places] >= "5") scaled += 1n;
  const result = scaled.toString().padStart(places + 1, "0");
  const grouped = (places ? result.slice(0, -places) : result).replace(
    /\B(?=(\d{3})+(?!\d))/g,
    ".",
  );
  return `${sign && scaled !== 0n ? "−" : ""}${grouped}${places ? "," + result.slice(-places) : ""}`;
}

export function formatMoney(value) {
  return value == null ? "No calculable" : `$ ${formatDecimal(value)}`;
}

export function validateProject(values) {
  const errors = {};
  if (!values.name.trim()) errors.name = "Escribe un nombre.";
  else if ([...values.name].length > 150)
    errors.name = "El nombre admite hasta 150 caracteres.";
  return errors;
}

export function normalizeDecimal(value) {
  return value.trim().replace(",", ".");
}

export function validateActivity(values) {
  const errors = validateProject(values);
  for (const key of [
    "bac",
    "planned_progress_pct",
    "actual_progress_pct",
    "actual_cost",
  ]) {
    const value = normalizeDecimal(values[key]);
    if (!/^\d+(?:\.\d+)?$/.test(value)) {
      errors[key] = "Escribe un valor no negativo, sin separadores de miles.";
      continue;
    }
    const [whole, fraction = ""] = value.split(".");
    if (/[1-9]/.test(fraction.slice(2))) {
      errors[key] = "Se permiten hasta dos decimales.";
      continue;
    }
    const cents =
      BigInt(whole) * 100n + BigInt(fraction.slice(0, 2).padEnd(2, "0"));
    const maximum = key.endsWith("_pct") ? 10000n : 9999999999999999n;
    if (cents > maximum)
      errors[key] = key.endsWith("_pct")
        ? "El porcentaje debe estar entre 0 y 100."
        : "El importe máximo es 99.999.999.999.999,99.";
  }
  return errors;
}
