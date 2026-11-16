#!/usr/bin/env python3
"""Capture a screenshot of the local service using Playwright."""

from pathlib import Path

from playwright.sync_api import sync_playwright

output = Path("docs/screenshots/service-home.png")
output.parent.mkdir(parents=True, exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1)
    page.goto("http://127.0.0.1:8080/", wait_until="networkidle")
    page.screenshot(path=str(output), full_page=True)
    browser.close()

print(output)
