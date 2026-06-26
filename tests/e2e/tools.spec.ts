import { expect, test } from "@playwright/test";

import { login } from "./helpers/auth";

test.describe("Tools", () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    await page.goto("/admin/tools/");
  });

  test("shows tools page with car seeding controls", async ({ page }) => {
    await expect(page.getByRole("heading", { name: "Tools", level: 1 })).toBeVisible();
    await expect(page.getByText(/Current table size:/)).toBeVisible();
    await expect(page.getByRole("button", { name: "Seed with samples" })).toBeVisible();
    await expect(page.getByRole("button", { name: "Clear and seed" })).toBeVisible();
    await expect(page.getByRole("button", { name: "Clear cars" })).toBeVisible();
  });

  test("clears and seeds sample cars", async ({ page }) => {
    page.once("dialog", (dialog) => dialog.accept());
    await page.getByRole("button", { name: "Clear and seed" }).click();

    await expect(page.getByText(/Added \d+ cars/)).toBeVisible();
    await expect(page.getByText(/Current table size:/)).toContainText("2000");
  });

  test("clears all cars", async ({ page }) => {
    page.once("dialog", (dialog) => dialog.accept());
    await page.getByRole("button", { name: "Clear cars" }).click();

    await expect(page.getByText(/Cars table cleared|already empty/)).toBeVisible();
    await expect(page.getByText(/Current table size:/)).toContainText("0");
  });
});
