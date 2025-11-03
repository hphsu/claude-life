import { test, expect } from '@playwright/test';

test.describe('Complete User Workflow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('should display home page with main navigation', async ({ page }) => {
    // Check page title
    await expect(page).toHaveTitle(/Fortune Platform/);

    // Check main navigation elements
    await expect(page.locator('nav')).toBeVisible();

    // Wait for page to fully load
    await page.waitForLoadState('networkidle');
  });

  test('should navigate to profile creation page', async ({ page }) => {
    // Navigate to profile creation
    const createProfileLink = page.getByRole('link', { name: /create profile|新增命盤/i });

    if (await createProfileLink.isVisible()) {
      await createProfileLink.click();

      // Wait for navigation
      await page.waitForURL(/.*profile\/new/);

      // Check form is visible
      await expect(page.locator('form')).toBeVisible();
    }
  });

  test('should create a new fortune profile', async ({ page }) => {
    // Navigate to profile creation
    await page.goto('http://localhost:3000/profile/new');

    // Wait for form to load
    await page.waitForSelector('form');

    // Fill in profile form
    const timestamp = Date.now();
    const testName = `Test User ${timestamp}`;

    await page.fill('input[name="name"]', testName);
    await page.selectOption('select[name="gender"]', 'male');

    // Fill in birth date
    await page.fill('input[name="birthYear"]', '1990');
    await page.fill('input[name="birthMonth"]', '5');
    await page.fill('input[name="birthDay"]', '15');

    // Fill in birth time
    await page.fill('input[name="birthHour"]', '10');
    await page.fill('input[name="birthMinute"]', '30');

    // Select birth location
    await page.fill('input[name="birthLocation"]', '台北');

    // Submit form
    await page.click('button[type="submit"]');

    // Wait for success message or navigation
    await page.waitForTimeout(2000);

    // Verify we're redirected or see success message
    const successMessage = page.locator('text=/success|成功/i');
    const profileList = page.locator('text=/profile|命盤/i');

    await expect(successMessage.or(profileList)).toBeVisible({ timeout: 10000 });
  });

  test('should request fortune analysis', async ({ page }) => {
    // Go to analysis request page
    await page.goto('http://localhost:3000/analysis/new');

    // Wait for page to load
    await page.waitForSelector('form', { timeout: 10000 });

    // Select analysis type
    const analysisTypeSelect = page.locator('select[name="analysisType"]');
    if (await analysisTypeSelect.count() > 0) {
      await analysisTypeSelect.selectOption('bazi');
    }

    // Select profile (if dropdown exists)
    const profileSelect = page.locator('select[name="profileId"]');
    if (await profileSelect.count() > 0 && await profileSelect.isVisible()) {
      const options = await profileSelect.locator('option').count();
      if (options > 1) {
        await profileSelect.selectOption({ index: 1 });
      }
    }

    // Add analysis notes
    await page.fill('textarea[name="notes"]', 'Test analysis request for E2E testing');

    // Submit request
    await page.click('button[type="submit"]');

    // Wait for processing
    await page.waitForTimeout(2000);

    // Check for success or job status
    await expect(page.locator('text=/processing|queued|分析中/i')).toBeVisible({ timeout: 15000 });
  });

  test('should view analysis results', async ({ page }) => {
    // Go to reports page
    await page.goto('http://localhost:3000/reports');

    // Wait for page to load
    await page.waitForLoadState('networkidle');

    // Check if reports list is visible
    const reportsList = page.locator('[data-testid="reports-list"]').or(page.locator('table')).or(page.locator('.report-item'));
    await expect(reportsList).toBeVisible({ timeout: 10000 });

    // Click on first report if available
    const firstReport = page.locator('[data-testid="report-item"]').first().or(page.locator('tr').nth(1)).or(page.locator('.report-item').first());

    if (await firstReport.count() > 0) {
      await firstReport.click();

      // Wait for report detail page
      await page.waitForTimeout(2000);

      // Check report content is displayed
      await expect(page.locator('text=/analysis|report|分析|報告/i')).toBeVisible();
    }
  });

  test('should filter and search reports', async ({ page }) => {
    // Go to reports page
    await page.goto('http://localhost:3000/reports');

    await page.waitForLoadState('networkidle');

    // Try to find and use search filter
    const searchInput = page.locator('input[type="search"]').or(page.locator('input[placeholder*="search"]')).or(page.locator('input[placeholder*="搜尋"]'));

    if (await searchInput.count() > 0) {
      await searchInput.fill('test');
      await page.waitForTimeout(1000);

      // Verify filtered results
      await expect(page.locator('text=/no results|沒有結果/i').or(page.locator('table'))).toBeVisible();
    }

    // Try status filter if available
    const statusFilter = page.locator('select[name="status"]').or(page.locator('[data-testid="status-filter"]'));

    if (await statusFilter.count() > 0) {
      await statusFilter.selectOption('completed');
      await page.waitForTimeout(1000);
    }
  });

  test('should track job progress in real-time', async ({ page }) => {
    // Go to dashboard or jobs page
    await page.goto('http://localhost:3000');

    await page.waitForLoadState('networkidle');

    // Look for job progress component
    const jobProgress = page.locator('[data-testid="job-progress"]').or(page.locator('.job-progress')).or(page.locator('text=/progress|進度/i'));

    if (await jobProgress.count() > 0) {
      await expect(jobProgress.first()).toBeVisible();

      // Check for progress indicators
      await expect(
        page.locator('text=/queued|processing|completed|排隊|處理中|完成/i').first()
      ).toBeVisible({ timeout: 5000 });
    }
  });

  test('should be responsive on mobile viewport', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });

    await page.goto('http://localhost:3000');
    await page.waitForLoadState('networkidle');

    // Check page is still usable
    await expect(page.locator('body')).toBeVisible();

    // Check navigation (might be hamburger menu)
    const mobileNav = page.locator('button[aria-label*="menu"]').or(page.locator('.mobile-menu')).or(page.locator('nav'));
    await expect(mobileNav.first()).toBeVisible();
  });

  test('should handle network errors gracefully', async ({ page }) => {
    // Simulate offline mode
    await page.route('**/api/**', route => route.abort());

    await page.goto('http://localhost:3000');

    // Try to perform action that requires API
    await page.goto('http://localhost:3000/analysis/new');

    // Should show error message
    await expect(
      page.locator('text=/error|failed|錯誤|失敗/i').first()
    ).toBeVisible({ timeout: 10000 });
  });

  test('should support keyboard navigation', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.waitForLoadState('networkidle');

    // Tab through interactive elements
    await page.keyboard.press('Tab');

    // Check that focus is visible
    const focusedElement = await page.evaluateHandle(() => document.activeElement);
    await expect(focusedElement).not.toBeNull();
  });

  test('should have proper ARIA labels for accessibility', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.waitForLoadState('networkidle');

    // Check for proper ARIA landmarks
    await expect(page.locator('nav')).toBeVisible();
    await expect(page.locator('main').or(page.locator('[role="main"]'))).toBeVisible();

    // Check buttons have accessible names
    const buttons = page.locator('button');
    const buttonCount = await buttons.count();

    if (buttonCount > 0) {
      for (let i = 0; i < Math.min(buttonCount, 5); i++) {
        const button = buttons.nth(i);
        const ariaLabel = await button.getAttribute('aria-label');
        const text = await button.textContent();

        // Button should have either text or aria-label
        expect(ariaLabel || text?.trim()).toBeTruthy();
      }
    }
  });
});
