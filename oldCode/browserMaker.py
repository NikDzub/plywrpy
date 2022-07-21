# -*- coding: utf-8 -*-

import os
import json
import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

cwd = os.getcwd()

comment_browsers = os.listdir(cwd + "/commentBrowsers")
comment_browsers.remove(".DS_Store")


users = ["vl64ye84_"]


async def block_media(route, req):
    # "image", "media", "font"
    if req.resource_type in {"image", "media", "font"}:
        await route.abort()


async def main():
    async with async_playwright() as p:

        async def main_bot(user):
            # cwd + f"/browsers2/{user}"
            browser = await p.chromium.launch_persistent_context(
                cwd + f"/commentBrowsers/{user}", headless=False
            )
            # await browser.route("**/*", block_media)
            page = await browser.new_page()
            await stealth_async(page)
            await page.goto(
                "https://www.tiktok.com/login/phone-or-email/email", wait_until="load"
            )
            await page.wait_for_selector(
                'h3[data-e2e="video-author-uniqueid"]', timeout=23423434
            )
            storage = await browser.storage_state(path=f"states/{user}.json")
            await page.close()
            await browser.close()

        await asyncio.gather(*(main_bot(user) for user in comment_browsers))


asyncio.run(main())
