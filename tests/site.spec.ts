import { expect, test } from '@playwright/test';

test('home page renders primary navigation', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByRole('heading', { name: 'Propr Review Demo' })).toBeVisible();
  await expect(page.getByRole('link', { name: 'Propr Review Demo' }).nth(1)).toHaveAttribute('href', '/');
  await expect(page.getByRole('link', { name: 'Blog' })).toHaveAttribute('href', '/blog/');
  await expect(page.getByRole('link', { name: 'About' })).toHaveAttribute('href', '/about/');
});

test('about page renders markdown content', async ({ page }) => {
  await page.goto('/about/');

  await expect(page.getByRole('heading', { name: 'About' })).toBeVisible();
  await expect(page.getByText('markdown is compiled into static HTML at build time')).toBeVisible();
});

test('blog listing renders articles in date order', async ({ page }) => {
  await page.goto('/blog/');

  await expect(page.getByRole('heading', { name: 'Blog' })).toBeVisible();
  const articleLinks = page.locator('.article-card h2 a');
  await expect(articleLinks).toHaveText([
    'Welcome to the Demo',
    'Reviewing Pull Requests Effectively',
  ]);
});

test('article page renders content and back link', async ({ page }) => {
  await page.goto('/blog/welcome-to-the-demo/');

  await expect(page.getByRole('heading', { name: 'Welcome to the Demo' })).toBeVisible();
  await expect(page.getByRole('link', { name: 'Back to Blog' })).toHaveAttribute('href', '/blog/');
  await expect(page.getByText('the build step turns it into a page')).toBeVisible();
});

test('second article route is reachable directly', async ({ page }) => {
  await page.goto('/blog/reviewing-pull-requests-effectively/');

  await expect(page.getByRole('heading', { name: 'Reviewing Pull Requests Effectively' })).toBeVisible();
  await expect(page.getByText('routing, rendering, and build behavior')).toBeVisible();
});
