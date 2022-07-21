from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import asyncio

import os
import shutil
import json


cwd = os.getcwd()


def get_browsers():
    global comment_browsers
    global all_browsers

    comment_browsers = os.listdir(cwd + "/commentBrowsers")
    comment_browsers.remove(".DS_Store")

    all_browsers = {}
    for folder in os.listdir(cwd):
        if "browsers" in folder:
            users = []
            for user in os.listdir(cwd + f"/{folder}"):
                if ".DS_Store" not in user:
                    users.append(user)

            all_browsers[folder] = users


get_browsers()


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


clean_browsers()


from playwright.async_api import async_playwright


async def cntx0():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            cwd + f"/browsers0/colegrr", headless=False
        )
        page = await browser.new_page()
        await stealth_async(page)
        await page.goto("https://www.tiktok.com")
        storage = await browser.storage_state(path="states/colegrr.json")
        await page.wait_for_timeout(1000)
        await browser.close()


async def no_cntx():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        await browser.new_context(storage_state="states/colegrr.json")

        page = await browser.contexts[0].new_page()
        await stealth_async(page)

        await page.goto(
            "https://www.tiktok.com/@clauzzzzzzzz/video/7058304647160745222"
        )
        print("colegrr")

        await page.wait_for_timeout(10000)

        vax_file = open("states/didujustvaxme.json")
        cookie_vax = json.load(vax_file)
        await browser.contexts[0].add_cookies(cookie_vax["cookies"])
        print("vax")

        await page.wait_for_timeout(10000)

        a00qq00bb_file = open("states/00qq00bb.json")
        cookie_00qq00bb = json.load(a00qq00bb_file)
        await browser.contexts[0].add_cookies(cookie_00qq00bb["cookies"])
        print("00qq00bb")

        await page.wait_for_timeout(5555555)
        await browser.close()


asyncio.run(cntx0())
# asyncio.run(no_cntx())
