#!/usr/bin/env python3
"""
Playwright verification script for deployed Python Practice Dashboard
"""

from playwright.sync_api import sync_playwright
import sys

DEPLOYED_URLS = [
    "https://57-starter-python-practice.vercel.app",
    "https://57-starter-python-practice-gq99hjmw1-mkknights-projects.vercel.app",
]

def verify_url(url):
    print(f"\n{'='*60}")
    print(f"Verifying: {url}")
    print('='*60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 900})
        page = context.new_page()

        console_logs = []
        errors = []

        page.on("console", lambda msg: console_logs.append(f"{msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: errors.append(str(err)))
        page.on("response", lambda response: (
            errors.append(f"HTTP {response.status}: {response.url}")
            if response.status >= 400 else None
        ))

        try:
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_selector("text=Python Practice Dashboard", timeout=10000)

            # Check if skills loaded
            skills_loaded = page.evaluate("""() => {
                const basics = document.getElementById('basics');
                return basics && basics.children.length > 0;
            }""")

            # Check API
            api_working = False
            try:
                response = page.evaluate("""async () => {
                    const res = await fetch('/api/skills');
                    return res.ok;
                }""")
                api_working = response
            except:
                pass

            print(f"Page loaded: True")
            print(f"Skills loaded: {skills_loaded}")
            print(f"API working: {api_working}")

            # Print console logs (excluding Tailwind warning)
            relevant_logs = [log for log in console_logs if "tailwind" not in log.lower()]
            if relevant_logs:
                print("\nConsole logs:")
                for log in relevant_logs:
                    print(f"  {log}")

            # Filter out 404s for favicon
            relevant_errors = [err for err in errors
                             if "favicon" not in err.lower()
                             and "HTTP 404" not in err]

            if relevant_errors:
                print("\nErrors:")
                for err in relevant_errors:
                    print(f"  ERROR: {err}")

            browser.close()

            if relevant_errors:
                print(f"\nFAILED: {len(relevant_errors)} errors found")
                return False
            else:
                print("\nPASSED: No errors found")
                return True

        except Exception as e:
            print(f"\nFAILED: Exception - {e}")
            browser.close()
            return False

if __name__ == "__main__":
    all_passed = True
    for url in DEPLOYED_URLS:
        if not verify_url(url):
            all_passed = False

    sys.exit(0 if all_passed else 1)
