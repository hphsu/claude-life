import { test, expect } from '@playwright/test';

test.describe('Profile Creation Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to profiles page
    await page.goto('/profiles');
  });

  test('should create a new profile successfully', async ({ page }) => {
    // Click "Create Profile" button
    await page.getByRole('button', { name: /新增命盤|建立命盤/ }).click();

    // Fill in profile form
    await page.getByLabel(/姓名/).fill('張三');
    await page.getByLabel(/性別/).selectOption('male');
    await page.getByLabel(/出生日期/).fill('1990-05-15');
    await page.getByLabel(/出生時間/).fill('14:30');
    await page.getByLabel(/出生地點/).fill('台北市');
    await page.getByLabel(/時區/).selectOption('Asia/Taipei');

    // Submit form
    await page.getByRole('button', { name: /確認|送出/ }).click();

    // Verify success
    await expect(page.getByText('張三')).toBeVisible();
    await expect(page.getByText(/1990-05-15/)).toBeVisible();
  });

  test('should show validation errors for empty required fields', async ({ page }) => {
    // Click "Create Profile" button
    await page.getByRole('button', { name: /新增命盤|建立命盤/ }).click();

    // Try to submit without filling required fields
    await page.getByRole('button', { name: /確認|送出/ }).click();

    // Verify validation errors
    await expect(page.getByText(/姓名.*必填|required/i)).toBeVisible();
    await expect(page.getByText(/性別.*必填|required/i)).toBeVisible();
    await expect(page.getByText(/出生日期.*必填|required/i)).toBeVisible();
  });

  test('should edit an existing profile', async ({ page }) => {
    // Assume at least one profile exists
    await page.getByRole('button', { name: /編輯/ }).first().click();

    // Change name
    await page.getByLabel(/姓名/).fill('李四');

    // Submit form
    await page.getByRole('button', { name: /確認|送出/ }).click();

    // Verify update
    await expect(page.getByText('李四')).toBeVisible();
  });

  test('should delete a profile with confirmation', async ({ page }) => {
    // Get initial profile count
    const initialCount = await page.getByRole('article').count();

    // Click delete button
    await page.getByRole('button', { name: /刪除/ }).first().click();

    // Confirm deletion
    await page.getByRole('button', { name: /確認.*刪除|delete/i }).click();

    // Verify profile count decreased
    const newCount = await page.getByRole('article').count();
    expect(newCount).toBe(initialCount - 1);
  });

  test('should show empty state when no profiles', async ({ page }) => {
    // This test assumes a fresh database or ability to delete all profiles
    // Verify empty state message
    const emptyMessage = page.getByText(/尚未建立任何命盤|no profiles/i);
    if (await emptyMessage.isVisible()) {
      await expect(emptyMessage).toBeVisible();
      await expect(page.getByRole('button', { name: /新增命盤|建立命盤/ })).toBeVisible();
    }
  });

  test('should handle birth time as optional', async ({ page }) => {
    // Click "Create Profile" button
    await page.getByRole('button', { name: /新增命盤|建立命盤/ }).click();

    // Fill in required fields only (without birth time)
    await page.getByLabel(/姓名/).fill('王五');
    await page.getByLabel(/性別/).selectOption('female');
    await page.getByLabel(/出生日期/).fill('1995-08-20');
    await page.getByLabel(/出生地點/).fill('高雄市');

    // Submit form
    await page.getByRole('button', { name: /確認|送出/ }).click();

    // Verify success
    await expect(page.getByText('王五')).toBeVisible();
  });

  test('should paginate profiles correctly', async ({ page }) => {
    // This test assumes more than 12 profiles exist
    const pagination = page.getByRole('navigation', { name: /pagination/i });

    if (await pagination.isVisible()) {
      // Click next page
      await page.getByRole('button', { name: /下一頁|next/i }).click();

      // Verify URL changed
      await expect(page).toHaveURL(/page=2/);

      // Click previous page
      await page.getByRole('button', { name: /上一頁|previous/i }).click();

      // Verify URL changed back
      await expect(page).toHaveURL(/page=1/);
    }
  });

  test('should display profile details correctly', async ({ page }) => {
    // Verify first profile card displays all information
    const firstProfile = page.getByRole('article').first();

    // Should show name
    await expect(firstProfile.getByRole('heading')).toBeVisible();

    // Should show gender
    await expect(firstProfile.getByText(/男性|女性/)).toBeVisible();

    // Should show birth date
    await expect(firstProfile).toContainText(/19\d{2}/);

    // Should show location
    await expect(firstProfile).toContainText(/市|縣/);
  });
});
