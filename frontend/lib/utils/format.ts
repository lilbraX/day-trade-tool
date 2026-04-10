export function pnlClass(value: number): string {
  return value >= 0 ? "profit" : "loss";
}
