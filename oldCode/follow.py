import os
import shutil
import json
import asyncio
import random
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

user_agents = [
    "Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.7.12) Gecko/20050915",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.7.6) Gecko/20050319",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; fr-FR; rv:1.7.11) Gecko/20050727",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.7.13) Gecko/20060414",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X; U; nb; rv:1.7.5) Gecko/20041110",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; nl-NL; rv:1.8.1.3) Gecko/20080722",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.5.1) Gecko/20031120",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1.11) Gecko/20071127",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; de-AT; rv:1.7.8) Gecko/20050511",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; de-AT; rv:1.7b) Gecko/20040421",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:0.9.7) Gecko/20011221",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; de-AT; rv:1.8b) Gecko/20050217",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.8b2) Gecko/20050702",
]


cwd = os.getcwd()


def get_browsers():
    global comment_browsers
    comment_browsers = os.listdir(cwd + "/commentBrowsers")
    comment_browsers.remove(".DS_Store")

    global all_browsers
    all_browsers = {}
    for folder in os.listdir(cwd):
        if "browsers" in folder:
            users = []
            for user in os.listdir(cwd + f"/{folder}"):
                if ".DS_Store" not in user:
                    users.append(user)

            all_browsers[folder] = users


def clean_browsers():
    cache_folders = [
        "Cache",
        "Code Cache",
        "Local Storage",
        "Session Storage",
        "Sessions",
    ]
    for browser_folder in all_browsers.keys():
        users = all_browsers[browser_folder]
        for user in users:
            path = cwd + f"/{browser_folder}/{user}/Default/"
            for cache_folder in cache_folders:
                try:
                    shutil.rmtree(path + cache_folder)
                except:
                    continue
    for user in comment_browsers:
        for cache_folder in cache_folders:
            try:
                shutil.rmtree(cwd + f"/commentBrowsers/{user}/Default/" + cache_folder)
            except:
                continue


get_browsers()
clean_browsers()
# print(tiktok_urls)
# print(browsers)


async def block_media(route, req):
    # "image", "media", "font", "stylesheet"
    if req.resource_type in {"x"}:
        await route.abort()


async def main():
    async with async_playwright() as p:

        async def find_comments(user, browsers_folder):

            browser = await p.chromium.launch_persistent_context(
                cwd + f"/{browsers_folder}/{user}",
                headless=False,
                user_agent=random.choice(user_agents),
                args=["--disable-webgl"]
                # viewport={"width": 400, "height": 600},
            )
            await browser.route("**/*", block_media)
            page = browser.pages[0]
            await stealth_async(page)
            for user in comment_browsers:
                try:
                    await page.goto(f"https://bot.sannysoft.com/", wait_until="load")
                except:
                    pass
                await page.wait_for_timeout(3345000)
            await page.close()
            await browser.close()

        for browser in all_browsers.keys():
            print(browser)
            await asyncio.gather(
                *(find_comments(user, browser) for user in all_browsers[browser])
            )

    clean_browsers()


asyncio.run(main())
