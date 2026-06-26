import { expect, test } from "@playwright/test";

import { login } from "./helpers/auth";

test.describe("Cars admin", () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test("lists cars and opens create form", async ({ page }) => {
    await expect(page.getByRole("link", { name: "Create" })).toBeVisible();
    await expect(page.getByRole("columnheader", { name: "Make" })).toBeVisible();
    await expect(page.getByRole("columnheader", { name: "Model" })).toBeVisible();

    await page.getByRole("link", { name: "Create" }).click();
    await expect(page).toHaveURL(/\/admin\/cars\/new/);
    await expect(page.getByLabel("Make")).toBeVisible();
    await expect(page.getByLabel("Model")).toBeVisible();
    await expect(page.getByLabel("Year")).toBeVisible();
  });

  test("creates a new car", async ({ page }) => {
    const make = `E2E-${Date.now()}`;

    await page.getByRole("link", { name: "Create" }).click();
    await page.getByLabel("Make").fill(make);
    await page.getByLabel("Model").fill("TestModel");
    await page.getByLabel("Year").fill("2024");
    await page.getByLabel("Color").fill("Blue");
    await page.getByLabel("Price").fill("1500000");
    await page.getByRole("button", { name: "Save", exact: true }).click();

    await expect(page).toHaveURL(/\/admin\/cars\//);
    await expect(page.getByRole("cell", { name: make, exact: true })).toBeVisible();
    await expect(page.getByRole("cell", { name: "TestModel", exact: true })).toBeVisible();
  });
});
