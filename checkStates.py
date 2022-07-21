from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import asyncio
import os
import json


async def block_media(route, req):
    # "image", "media", "font", "stylesheet"
    if req.resource_type in {"image", "media", "font", "stylesheet"}:
        try:
            await route.abort()
        except:
            pass


head = False
cwd = os.getcwd()

states = os.listdir(cwd + "/states")
states.remove(".DS_Store")


async def main():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=head)

        await browser.new_context()
        await browser.contexts[0].route("**/*", block_media)
        page = await browser.contexts[0].new_page()
        await stealth_async(page)
        await page.goto("https:www.tiktok.com", wait_until="load")
        needs_update = []
        for state in states:
            # print(state)
            state_file = open(f"states/{state}")
            state_json = json.load(state_file)
            await browser.contexts[0].add_cookies(state_json["cookies"])
            await page.reload(wait_until="load")
            try:
                await page.wait_for_selector('div[data-e2e="inbox-icon"]', timeout=1000)
                # print(state + " good")
            except:
                needs_update.append(state)
                print(state + " needs update")
        print(needs_update)
        await page.close()
        await browser.close()


asyncio.run(main())
