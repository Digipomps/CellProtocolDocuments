// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors
const { test, expect } = require('@playwright/test');

test('participant edits persist through reload on desktop and 375 px', async ({ page }, testInfo) => {
  test.setTimeout(180_000);
  const baseURL = process.env.ARENDALSUKA_PROFILE_BASE_URL || 'http://127.0.0.1:9094';
  expect(['127.0.0.1', 'localhost', '[::1]']).toContain(new URL(baseURL).hostname);
  const username = `profile-proof-${Date.now()}`;
  const registration = await page.request.post(new URL('/auth/register', baseURL).href, {
    data: { username, password: 'LocalSyntheticProfileProof!2026' },
  });
  expect(registration.ok(), await registration.text()).toBe(true);
  const url = new URL('/browserhead/webo', baseURL);
  url.searchParams.set('configurationName', 'Arendalsuka Min Profil');
  url.searchParams.set('configurationEndpoint', 'cell:///ArendalsukaParticipantProfile');
  const active = page.locator('[data-active-configuration="Arendalsuka Min Profil"]');
  const name = page.getByPlaceholder('F.eks. Cissi', { exact: true });
  const role = page.getByPlaceholder('F.eks. Rådgiver, digital politikk', { exact: true });
  const position = page.getByPlaceholder('F.eks. Ved Torvscenen', { exact: true });
  const favorites = page.getByLabel('Del mine lagrede arrangementer', { exact: true });
  const action = async (suffix, perform) => {
    const responsePromise = page.waitForResponse(response => {
      if (!response.url().includes('/browserhead/porthole/action') || response.request().method() !== 'POST') return false;
      return response.request().postDataJSON()?.keypath === `arendalsukaParticipantProfile.${suffix}`;
    }, { timeout: 30_000 });
    responsePromise.catch(() => {});
    await perform();
    const response = await responsePromise;
    expect(response.ok()).toBe(true);
    const envelope = await response.json();
    const result = envelope.result ?? envelope;
    expect(result, 'Profile writes must acknowledge an available persisted state.').toMatchObject({ isAvailable: true });
    await expect(active).toBeVisible();
    return result;
  };
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto(url.href, { waitUntil: 'domcontentloaded', timeout: 90_000 });
  await expect(active).toBeVisible({ timeout: 45_000 });
  await expect(name).toBeVisible();
  await expect(name).toHaveCSS('color', 'rgb(26, 28, 25)');
  const updatedName = await action('profile.setDisplayNameOverride', () => name.fill('Syntetisk deltaker'));
  expect(updatedName.displayNameOverride).toBe('Syntetisk deltaker');
  const updatedRole = await action('profile.setStilling', () => role.fill('Test av deltakerprofil'));
  expect(updatedRole.stilling).toBe('Test av deltakerprofil');
  const manual = await action('profile.setManualPositionLabel', () => position.fill('Ved testscenen'));
  expect(manual.positionSharing).toMatchObject({ mode: 'manual', manualLabel: 'Ved testscenen' });
  await expect(page.getByText('manual', { exact: true })).toBeVisible();
  await expect(favorites).not.toBeChecked();
  const shared = await action('state.favoritesSharingEnabled', () => favorites.click());
  expect(shared.favoritesSharingEnabled).toBe(true);
  await expect(favorites).toBeChecked();
  const png = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Wl6dS8AAAAASUVORK5CYII=';
  const photo = await action('profile.setPhoto', () => page.locator('input[type=file]').setInputFiles({
    name: 'synthetic-profile.png', mimeType: 'image/png', buffer: Buffer.from(png, 'base64'),
  }));
  expect(photo.photoDataURI).toBe(`data:image/png;base64,${png}`);
  await expect(page.locator('.skeleton-fileupload-status')).toHaveText('File sent to cell.');
  await expect(page.getByText('Profilbilde lagret', { exact: true })).toBeVisible();
  await page.reload({ waitUntil: 'domcontentloaded' });
  await expect(active).toBeVisible();
  await expect(name).toHaveValue('Syntetisk deltaker');
  await expect(page.getByText('Profilbilde lagret', { exact: true })).toBeVisible();
  await expect(role).toHaveValue('Test av deltakerprofil');
  await expect(position).toHaveValue('Ved testscenen');
  await expect(favorites).toBeChecked();
  const desktopScreenshot = testInfo.outputPath('profile-desktop.png');
  await page.screenshot({ path: desktopScreenshot, fullPage: true });
  await testInfo.attach('profile-desktop', { path: desktopScreenshot, contentType: 'image/png' });
  await page.setViewportSize({ width: 375, height: 812 });
  await expect(name).toBeVisible();
  await expect(favorites).toBeChecked();
  const disabled = await action('state.favoritesSharingEnabled', () => favorites.click());
  expect(disabled.favoritesSharingEnabled).toBe(false);
  await page.reload({ waitUntil: 'domcontentloaded' });
  await expect(active).toBeVisible();
  await expect(favorites).not.toBeChecked();
  await expect(name).toHaveValue('Syntetisk deltaker');
  const checkedIn = await action('profile.setCheckedInVenue', () => page.getByRole('combobox').selectOption({ label: 'Syntetisk testarena' }));
  expect(checkedIn.positionSharing).toMatchObject({ mode: 'checkin', checkedInVenueLabel: 'Syntetisk testarena' });
  await expect(page.getByText('checkin', { exact: true })).toBeVisible();
  const off = await action('profile.setPositionSharing', () => page.getByRole('button', { name: 'Av', exact: true }).click());
  expect(off.positionSharing.mode).toBe('off');
  await expect(page.getByText('off', { exact: true })).toBeVisible();
  await page.reload({ waitUntil: 'domcontentloaded' });
  await expect(active).toBeVisible();
  await expect(page.getByText('off', { exact: true })).toBeVisible();
  await expect(position).toHaveValue('');
  const removedPhoto = await action('profile.setPhoto', () => page.getByRole('button', { name: 'Fjern profilbilde', exact: true }).click());
  expect(removedPhoto.photoDataURI).toBeNull();
  await expect(page.getByText('Ingen profilbilde lagret', { exact: true })).toBeVisible();
  await page.reload({ waitUntil: 'domcontentloaded' });
  await expect(page.getByText('Ingen profilbilde lagret', { exact: true })).toBeVisible();
  const dimensions = await page.evaluate(() => ({ viewport: innerWidth, width: document.documentElement.scrollWidth }));
  expect(dimensions.width).toBe(dimensions.viewport);
  await expect(page.locator('body')).not.toContainText(/Something went wrong|Noe gikk galt|\bUnavailable\b|\bdenied\b/);
  const mobileScreenshot = testInfo.outputPath('profile-375.png');
  await page.screenshot({ path: mobileScreenshot, fullPage: true });
  await testInfo.attach('profile-375', { path: mobileScreenshot, contentType: 'image/png' });
});
