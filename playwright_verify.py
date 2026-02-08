#!/usr/bin/env python3
"""
Playwright verification script for Python Practice Dashboard
"""

from playwright.sync_api import sync_playwright
import sys

def verify_and_capture():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 900})
        page = context.new_page()

        # Capture console logs
        console_logs = []
        page.on("console", lambda msg: console_logs.append(f"{msg.type}: {msg.text}"))

        # Capture errors
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))

        print("Opening http://localhost:5001...")
        page.goto("http://localhost:5001", wait_until="networkidle")

        # Wait for content to load
        page.wait_for_selector("text=Python Practice Dashboard", timeout=10000)

        # Check if skills loaded
        skills_loaded = page.evaluate("""() => {
            const basics = document.getElementById('basics');
            return basics && basics.children.length > 0;
        }
        """)

        print(f"Skills loaded: {skills_loaded}")

        # Take screenshot
        screenshot_path = "/Users/mkazi/60 Projects/screenshots/starters/starter-57.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"Screenshot saved to: {screenshot_path}")

        # Print console logs
        if console_logs:
            print("\nConsole logs:")
            for log in console_logs:
                print(f"  {log}")

        # Print errors
        if errors:
            print("\nPage errors:")
            for err in errors:
                print(f"  ERROR: {err}")

        # Check for any visible errors on page
        page_content = page.content()
        if "error" in page_content.lower() and "traceback" in page_content.lower():
            print("\nWARNING: Error content detected in page!")
            errors.append("Error content in page")

        browser.close()

        # Return success status
        if errors:
            print(f"\nVerification FAILED: {len(errors)} errors found")
            return False
        else:
            print("\nVerification PASSED: No errors found")
            return True

if __name__ == "__main__":
    success = verify_and_capture()
    sys.exit(0 if success else 1)
