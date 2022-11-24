import os
import json
import asyncio
import random
from datetime import datetime
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

head = False

# 👤 states
live_path = "./allStates/liveStates"
live_states = os.listdir(live_path)
if ".DS_Store" in live_states:
    live_states.remove(".DS_Store")

searcher = "./allStates/oneOnly/ihptto.json"

# 🔧 handles
async def block_media(route, req):
    if req.resource_type in {"image", "media", "font", "stylesheet", "css"}:
        try:
            await route.abort()
        except:
            pass


async def main():
    urls = []
    async with async_playwright() as p:

        # 🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊

        async def find_urls():
            browser = await p.chromium.launch(
                headless=head,
                # proxy={
                #     "server": "http://nproxy.site:10558",
                #     "username": "aZ1nUR",
                #     "password": "SYtmUSzaC8yF",
                # },
            )
            page = await browser.new_page()
            await stealth_async(page)
            await browser.contexts[0].route("**/*", block_media)

            state_file = open(f"{searcher}")
            state_json = json.load(state_file)
            await browser.contexts[0].add_cookies(state_json["cookies"])
            # ⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️

            await page.goto("https://www.tiktok.com/live", wait_until="load")
            await page.click("text=Click to watch LIVE", timeout=5000)
            await page.click("div[data-e2e='live-side-more-button']")
            await page.wait_for_selector("text=See less")

            all_views = await page.query_selector_all("div[data-e2e='person-count']")

            chosen_k = []
            for view in all_views:
                view_count = await view.inner_text()
                if "K" in view_count:
                    chosen_k.append([view, view_count.replace("K", "")])
            chosen_k.sort(key=lambda x: x[1], reverse=True)

            await chosen_k[0][0].click()

            urls.append(page.url)
            print(page.url)

            await page.close()
            await browser.close()

        await find_urls()

        # 🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊🦊

        async def spam_urls(state):

            browser = await p.chromium.launch(
                headless=head,
                # proxy={
                #     "server": "http://nproxy.site:10558",
                #     "username": "aZ1nUR",
                #     "password": "SYtmUSzaC8yF",
                # },
            )
            page = await browser.new_page()
            await stealth_async(page)
            await browser.contexts[0].route("**/*", block_media)

            state_file = open(f"{live_path}/{state}")
            state_json = json.load(state_file)
            await browser.contexts[0].add_cookies(state_json["cookies"])
            # ⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️⚙️

            await page.goto(urls[0], wait_until="load")
            await page.wait_for_selector("div[data-e2e='chat-message']", timeout=60000)

            await page.click("div[data-e2e='comment-emoji-icon']")
            await page.wait_for_timeout(20000)
            print("start commenting")

            comments = [
                "GOOGLE THIS > O83NC63 😋😮",
                "GOOGLE SEARCH THIS > O83NC63 😮",
                "OMG GOOGLE O83NC63  😮",
                "😮 GOOGLE THIS > O83NC63 😮",
                "Google search O83NC63 , FREE GIFT",
                "FREE COINS - Google O83NC63",
                "FREE COINS - Google Search : O83NC63",
                "OMG OMG FREE COINS - Google Search : O83NC63",
            ]

            for i in range(5):
                await page.keyboard.type(random.choice(comments), delay=100)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(5000)

            print("finish")
            await page.wait_for_timeout(34324324)
            await page.close()
            await browser.close()

        await asyncio.gather(*(spam_urls(state) for state in live_states))


asyncio.run(main())
