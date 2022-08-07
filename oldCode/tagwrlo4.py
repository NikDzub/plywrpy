# npm run fam ; cd -- && cd desktop/code/plywrpy && python wrlo2.py && cd -- && cd desktop/code/plywr &&
# sudo nvram -c ; sudo shutdown -r now
import os
import json
import asyncio
import random
from datetime import datetime
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async


head = False
comments = [
    " what??",
]
reply_comments = [
    "lol i googled it and got a giftcard thank you",
    "whats going on here?",
    "wtf? gogole 33tk66kt",
    "yall should try this",
    "ty",
    "amazing can i do it again?",
    "damn google the code",
    "what code?",
    "just google 33tk66kt",
    "what the...",
    "omg did someone tried it?",
    "damn thats sickk.. thanks bro",
    "omg thank you i got 50$ giftcard",
    " omg thanks for the giftcards",
    " thank you again",
    " can i do it again if i allready got a giftcard?" " omg i worked!!",
    "it works",
    " damn this works lol",
    " wow it worked for me",
]

tiktok_urls = json.load(open("./urls.json", encoding="utf-8"))

comments_path = "./realStates"
comment_states = os.listdir(comments_path)
if ".DS_Store" in comment_states:
    comment_states.remove(".DS_Store")
repliers = os.listdir("./realStates")

states = os.listdir("./states")
states.remove(".DS_Store")


async def block_media(route, req):
    # "image", "media", "font", "stylesheet"
    if req.resource_type in {"image", "media", "font", "stylesheet"}:
        try:
            await route.abort()
        except:
            pass


# async def block_all(route, req):
#     try:
#         await route.abort()
#     except:
#         pass


async def main():
    print("🏁" + "\033[96m {}\033[00m".format(datetime.now().strftime("%H:%M:%S")))

    async with async_playwright() as p:

        f = len(comment_states) * len(tiktok_urls)
        global d
        d = 0

        async def comment_w_states(url):

            print("\033[96m {}\033[00m".format(url))
            browser = await p.chromium.launch(headless=head)
            page = await browser.new_page()
            await stealth_async(page)
            await browser.contexts[0].route("**/*", block_media)
            # await browser.contexts[0].route(
            #     "https://www.tiktok.com/node/share/discover*", block_all
            # )
            # await browser.contexts[0].route(
            #     "https://www.tiktok.com/api/user/list*", block_all
            # )
            # await browser.contexts[0].route(
            #     "https://www.tiktok.com/api/recommend*", block_all
            # )

            state_file = open(f"states/ihptto.json")
            state_json = json.load(state_file)
            await browser.contexts[0].add_cookies(state_json["cookies"])

            await page.goto(url, wait_until="load")
            valid = await page.wait_for_selector(
                'div[data-e2e="comment-emoji-icon"]', timeout=2000
            )
            if valid == None:
                tiktok_urls.remove(url)
                await page.close()
                await browser.close()
                print("🗑 Can't comment[0]" + "\033[91m {}\033[00m".format(url))
            else:
                for state in comment_states:
                    state_file = open(f"{comments_path}/{state}")
                    state_json = json.load(state_file)
                    await browser.contexts[0].add_cookies(state_json["cookies"])
                    await page.reload(wait_until="load")

                    valid_in_state = await page.locator(
                        'span[data-e2e="comment-icon"]'
                    ).is_visible()
                    if valid_in_state:
                        # await page.click("video")
                        await page.click(
                            'div[data-e2e="comment-emoji-icon"]', timeout=1000
                        )
                        r = round(random.uniform(0, 10))
                        await page.click(
                            f'div[data-e2e="comment-emoji-group"] li[data-index="{r}"]'
                        )
                        await page.keyboard.type("@re50er500")
                        await page.wait_for_timeout(1000)
                        await page.click('div[data-e2e="comment-at-list"]')
                        com = random.choice(comments)
                        await page.keyboard.type(com)
                        await page.wait_for_timeout(1000)
                        await page.keyboard.press("Enter")
                        await page.wait_for_selector(
                            "text=Comment posted", timeout=10000
                        )
                        global d
                        d += 1
                        print("\r" + f" [{d} / {f}]", end="")

                        # storage = await browser.contexts[0].storage_state(
                        #     path=f"commentStates/{state}"
                        # )

                await page.close()
                await browser.close()

        await asyncio.gather(*(comment_w_states(url) for url in tiktok_urls))

        print("\n💬" + "\033[96m {}\033[00m".format(datetime.now().strftime("%H:%M:%S")))

        j = len(states) * len(tiktok_urls)
        global i
        i = 0
        global c
        c = 0

        static_states = []
        for state in states:
            state_file = open(f"states/{state}")
            state_json = json.load(state_file)
            static_states.append([state_json["cookies"], state])

        jsEval = open("./jsEval.js").read()

        async def find_comments(url):

            for state in static_states:

                global i
                global c
                i += 1
                print("\r" + f" [{i} / {j}] [{c}]", end="")

                browser = await p.chromium.launch(headless=head)
                page = await browser.new_page()
                await stealth_async(page)
                await browser.contexts[0].route("**/*", block_media)
                await browser.contexts[0].add_cookies(state[0])
                await page.goto(url, wait_until="load")

                not_avl = await page.wait_for_selector(
                    "text=Video currently unavailable", timeout=1000
                )
                if not_avl != None:
                    break

                await page.evaluate(jsEval)

                if i < 10:
                    await page.wait_for_timeout(21000)
                    found = await page.wait_for_selector(
                        'svg[liked="false"]', timeout=1000
                    )
                else:
                    found = await page.wait_for_selector(
                        'svg[liked="false"]', timeout=20000
                    )

                if found != None:
                    not_liked = await page.query_selector_all(
                        'div[plywr] [data-e2e="comment-like-count"]'
                    )
                    if len(not_liked) > 0:
                        for heart in not_liked:
                            await heart.click()
                            c += 1
                            print("\r" + f" [{i} / {j}] [{c}]", end="")
                            await page.wait_for_timeout(1000)
                    # reply
                    if state[1] in repliers:
                        await page.click(
                            'span[data-e2e="comment-reply-1"]', timeout=1000
                        )
                        await page.keyboard.type(random.choice(reply_comments))
                        await page.keyboard.press("Enter")
                        await page.wait_for_timeout(1000)

                else:
                    pass
                    # print("🔍❌ " + "\033[91m {}\033[00m".format(url))

                await page.close()
                await browser.close()

        await asyncio.gather(*(find_comments(url) for url in tiktok_urls))

    print("\n🏁" + "\033[96m {}\033[00m".format(datetime.now().strftime("%H:%M:%S")))


asyncio.run(main())
