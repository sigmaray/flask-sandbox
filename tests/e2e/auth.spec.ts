import { expect, test } from "@playwright/test";

import { E2E_PASSWORD, E2E_USERNAME, login } from "./helpers/auth";

test.describe("Authentication", () => {
  test("redirects unauthenticated users to login", async ({ page }) => {
    await page.goto("/admin/cars/");
    await expect(page).toHaveURL(/\/login/);
    await expect(page.getByRole("heading", { name: "Admin login" })).toBeVisible();
  });

  test("shows error for invalid credentials", async ({ page }) => {
    await page.goto("/login");
    await page.getByLabel("Username").fill("e2e");
    await page.getByLabel("Password").fill("wrong-password");
    await page.getByRole("button", { name: "Log in" }).click();

    await expect(page).toHaveURL(/\/login/);
    await expect(page.getByText("Invalid username or password.")).toBeVisible();
  });

  test("logs in with valid credentials", async ({ page }) => {
    await login(page);

    await expect(page.getByRole("link", { name: "Cars", exact: true })).toBeVisible();
    await expect(page.getByText(E2E_USERNAME)).toBeVisible();
  });

  test("logs out and returns to login page", async ({ page }) => {
    await login(page);
    await page.getByRole("link", { name: "Log out" }).click();

    await expect(page).toHaveURL(/\/login/);
    await expect(page.getByRole("heading", { name: "Admin login" })).toBeVisible();
  });
});
