import { expect, type Page } from "@playwright/test";

export const E2E_USERNAME = "e2e";
export const E2E_PASSWORD = "e2e-pass";

export async function login(page: Page): Promise<void> {
  await page.goto("/login");
  await page.getByLabel("Username").fill(E2E_USERNAME);
  await page.getByLabel("Password").fill(E2E_PASSWORD);
  await page.getByRole("button", { name: "Log in" }).click();
  await expect(page).toHaveURL(/\/admin\/cars/);
}
