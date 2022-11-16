import os
import json
import asyncio
import random
from datetime import datetime
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

head = False

# 👤 states
comments_path = "./allStates/newStates"
comment_states = os.listdir(comments_path)
if ".DS_Store" in comment_states:
    comment_states.remove(".DS_Store")

like_path = "./allStates/likeStates"
like_states = os.listdir(like_path)
if ".DS_Store" in like_states:
    like_states.remove(".DS_Store")

repliers = os.listdir("./allStates/likeStates")

searcher = "./allStates/oneOnly/ihptto.json"


# handles
async def block_media(route, req):
    if req.resource_type in {"image", "media", "font", "stylesheet", "css"}:
        try:
            await route.abort()
        except:
            pass


# START


async def main():
    async with async_playwright() as p:

        async def find_url():
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
            # await browser.contexts[0].route("**/*", block_media)

            state_file = open(f"{searcher}")
            state_json = json.load(state_file)
            await browser.contexts[0].add_cookies(state_json["cookies"])

            await page.goto("https://www.tiktok.com/live", wait_until="load")
            await page.click("text=Click to watch LIVE", timeout=5000)

            await page.click("div[data-e2e='live-side-more-button']")
            all_views = await page.query_selector_all("div[data-e2e='person-count']")
            for view in all_views:
                view_count = await view.inner_text()
                print(view_count)
            print("hereee")
            await page.wait_for_timeout(43543435)

        await find_url()

    #     print("\n💬" + "\033[96m {}\033[00m".format(datetime.now().strftime("%H:%M")))

    #     j = len(like_states) * len(tiktok_urls)
    #     global i
    #     i = 0
    #     global c
    #     c = 0

    #     static_like_states = []
    #     for state in like_states:
    #         state_file = open(f"{like_path}/{state}")
    #         state_json = json.load(state_file)
    #         static_like_states.append([state_json["cookies"], state])
    #     random.shuffle(static_like_states)

    #     jsEval = open("./jsEval.js").read()

    #     async def find_comments(url):

    #         # 💚💚💚💚
    #         start_time = datetime.now()
    #         for state in static_like_states:
    #             if (datetime.now() - start_time).seconds > 60 * 25:
    #                 # max time
    #                 break

    #             global i
    #             global c
    #             i += 1
    #             print("\r" + f" [{i} / {j}] [{c}]", end="")

    #             browser = await p.chromium.launch(headless=head)
    #             page = await browser.new_page()
    #             await stealth_async(page)
    #             await browser.contexts[0].route("**/*", block_media)
    #             await browser.contexts[0].add_cookies(state[0])
    #             await page.goto(url, wait_until="load")

    #             not_avl = await page.wait_for_selector(
    #                 "text=Video currently unavailable", timeout=1000
    #             )
    #             if not_avl != None:
    #                 break

    #             await page.evaluate(jsEval)
    #             await page.click("text=Add comment...", timeout=5000)

    #             if i < 20:
    #                 await page.wait_for_timeout(60000)
    #                 hearts = await page.query_selector_all(
    #                     'span[data-e2e="comment-like-count"]'
    #                 )
    #                 if hearts != None and hearts.__len__() > 0:
    #                     for heart in hearts:
    #                         await heart.click()
    #                         c += 1
    #                         print("\r" + f" [{i} / {j}] [{c}]", end="")
    #                         await page.wait_for_timeout(2000)
    #                 # found = await page.wait_for_selector("div[plywr]", timeout=1000)

    #             else:
    #                 hearts = await page.query_selector_all(
    #                     'span[data-e2e="comment-like-count"]'
    #                 )
    #                 if hearts != None and hearts.__len__() > 0:
    #                     for heart in hearts:
    #                         await heart.click()
    #                         c += 1
    #                         print("\r" + f" [{i} / {j}] [{c}]", end="")
    #                         await page.wait_for_timeout(2000)
    #                 # found = await page.wait_for_selector("div[plywr]", timeout=20000)

    #             # if found != None:
    #             #     not_liked = await page.query_selector_all(
    #             #         'div[plywr] svg[fill="rgba(22, 24, 35, 1)"]'
    #             #     )
    #             #     if len(not_liked) > 0:
    #             #         for heart in not_liked:
    #             #             await heart.click()
    #             #             await page.wait_for_timeout(1000)
    #             #             c += 1
    #             #             print("\r" + f" [{i} / {j}] [{c}]", end="")

    #             # reply
    #             # r = [1, 0, 0]
    #             # if state[1] in repliers and random.choice(r) == 1:
    #             #     await page.click(
    #             #         'span[data-e2e="comment-reply-1"]', timeout=1000
    #             #     )
    #             #     await page.keyboard.type(random.choice(reply_comments))
    #             #     await page.keyboard.press("Enter")
    #             #     # await page.wait_for_timeout(1000)

    #             # else:
    #             #     pass
    #             # print("🔍❌ " + "\033[91m {}\033[00m".format(url))

    #             # save
    #             await browser.contexts[0].storage_state(path=f"{like_path}/{state[1]}")
    #             # save
    #             # 💚💚💚💚

    #             await page.close()
    #             await browser.close()

    #     await asyncio.gather(*(find_comments(url) for url in tiktok_urls))

    # print("\n🏁" + "\033[96m {}\033[00m".format(datetime.now().strftime("%H:%M")))


asyncio.run(main())
