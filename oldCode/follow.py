# -*- coding: utf-8 -*-
# 100 sidurchroti1972
import os
import random
import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

cwd = os.getcwd()


users = os.listdir("./newStates")
users.remove(".DS_Store")


async def block_media(route, req):
    # "image", "media", "font"
    if req.resource_type in {"image", "media", "font"}:
        await route.abort()


async def main():
    for user in users:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            browser = await browser.new_context(storage_state=f"./newStates/{user}")
            await browser.route("**/*", block_media)
            page = await browser.new_page()
            await stealth_async(page)

            for u in users:
                if u != user:
                    print(u)
                    u = u.replace(".json", "")
                    await page.goto(
                        f"https://www.tiktok.com/@{u}",
                        wait_until="load",
                    )
                    follow_btn = await page.wait_for_selector(
                        'button[data-e2e="follow-button"]', timeout=5000
                    )
                    await follow_btn.click(timeout=1000)
                    await page.wait_for_timeout(3000)

            # await page.close()
            await browser.close()


asyncio.run(main())
