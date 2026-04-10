import { describe, expect, it } from "vitest";
import { pnlClass } from "./format";

describe("pnlClass", () => {
  it("returns profit for non-negative", () => {
    expect(pnlClass(0)).toBe("profit");
    expect(pnlClass(1)).toBe("profit");
  });

  it("returns loss for negative", () => {
    expect(pnlClass(-1)).toBe("loss");
  });
});
