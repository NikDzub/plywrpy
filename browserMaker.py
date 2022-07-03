# -*- coding: utf-8 -*-

import os
import json
import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

cwd = os.getcwd()

users = ["dogosow1"]


async def block_media(route, req):
    # "image", "media", "font"
    if req.resource_type in {"image", "media", "font"}:
        await route.abort()


async def main():
    async with async_playwright() as p:

        async def main_bot(user):
            # cwd + f"/browsers/{user}"
            browser = await p.chromium.launch_persistent_context(
                cwd + f"/browsers0/{user}", headless=False
            )
            # await browser.route("**/*", block_media)
            page = await browser.new_page()
            await stealth_async(page)
            await page.goto(
                "https://www.tiktok.com/login/phone-or-email/email", wait_until="load"
            )
            await page.fill("input[placeholder~='Email']", user)
            await page.fill("input[type='password']", "abc123!@#")
            await page.wait_for_timeout(1000)
            await page.close()
            await browser.close()

        await asyncio.gather(*(main_bot(user) for user in users))


asyncio.run(main())
