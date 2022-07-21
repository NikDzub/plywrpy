# -*- coding: utf-8 -*-
# 60 siodenabald1974
import os
import json
import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

cwd = os.getcwd()


users = open("./usrsunform.txt")

bios = ["🐼 I Got you FREE TikTok Coins, Google The CODE in my Picture! 🦊"]


async def block_media(route, req):
    # "image", "media", "font"
    if req.resource_type in {"ximage", "media", "font"}:
        await route.abort()


async def main():
    for user in users:
        user = user.split(":")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            # await browser.route("**/*", block_media)
            page = await browser.new_page()
            await stealth_async(page)
            page.on(
                "filechooser",
                lambda file_chooser: file_chooser.set_files("./pfpics/00qq00bb.png"),
            )

            await page.goto(
                "https://www.tiktok.com/login/phone-or-email/email",
                wait_until="load",
            )
            await page.wait_for_selector("form input")
            await page.fill("input[placeholder~='Email']", user[0])
            await page.fill("input[type='password']", user[1])
            await page.click("button[type='submit']")
            try:
                # await page.wait_for_selector("text=Login Success", timeout=30000)
                await page.wait_for_url(
                    "https://www.tiktok.com/foryou?lang=en", timeout=30000
                )
                if page.url != "https://www.tiktok.com/foryou?lang=en":
                    raise TypeError("Didnt login")
            except:
                print(f"{user[0]} ❌")
            else:

                await page.goto(f"https://www.tiktok.com/@{user[0]}", wait_until="load")
                await page.click("text=Edit profile")
                await page.click('input[type="file"]')
                await page.click("text=Apply")
                await page.fill('textarea[data-e2e="edit-profile-bio-input"]', bios[0])
                await page.click('button[data-e2e="edit-profile-save"]')
                await page.wait_for_timeout(1000)

                storage = await browser.contexts[0].storage_state(
                    path=f"newStates/{user[0]}.json"
                )
                print(f"{user[0]} ✅")

            # await page.close()
            await browser.close()


asyncio.run(main())
