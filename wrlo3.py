import os
import json
import asyncio
import random
from datetime import datetime
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

# npm run fam ; cd -- && cd desktop/code/plywrpy && python wrlo3.py && cd -- && cd desktop/code/plywr &&
# sudo nvram -c ; sudo shutdown -r now


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


# 💬 comments
comments = [
    "Google O83NC63",
    "OMG Google That > O83NC63",
    "Google This Code O83NC63",
    "Google Search for O83NC63",
    "Did you Google O83NC63?",
    "Hey Google this special CODE : O83NC63",
    "Omg google search O83NC63",
    "Go to 4gift.site in the browser",
]
reply_comments = [
    "yo",
    "lol",
    "Nice",
    "lol look at his bio",
    "yall should try this i just got a 50$ giftcard from this, just google site:4gift.site",
    "please answer in dm",
    "reply pls",
    "i allready got 10 gifts",
    "🥹",
    "🐼",
    "merci pour le cadeau 👀",
    "gracias por el regalo",
    "شكرا على الهدية",
    "hediye için teşekkürler",
    "omg it works?",
    "🥰 Thank you sir",
    "He recibido una tarjeta regalo, thank you",
    "J'ai reçu une carte-cadeau",
    "merci pour le cadeau 🥰",
    "i didnt knew its working lol",
    "google 33tk66kt",
    "wow díky",
    "waw diolch am yr anrheg 😄",
    "哇，谢谢你的礼物 😁",
    "Great...",
    "who are you people?",
]

tiktok_urls = json.load(open("./urls.json", encoding="utf-8"))

# handles
async def block_media(route, req):
    if req.resource_type in {"image", "media", "font", "stylesheet", "css"}:
        try:
            await route.abort()
        except:
            pass


print(f"{comments_path}[ {len(comment_states)} 💬] {like_path}[{ len(like_states)} 💚]")

# ▶️
async def main():
    print("🏁" + "\033[96m {}\033[00m".format(datetime.now().strftime("%H:%M")))

    async with async_playwright() as p:

        f = len(comment_states) * len(tiktok_urls)
        global d
        d = 0

        async def comment_w_states(url):

            print("\033[96m {}\033[00m".format(url))
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

            state_file = open(f"{comments_path}/{comment_states[0]}")
            state_json = json.load(state_file)
            await browser.contexts[0].add_cookies(state_json["cookies"])

            await page.goto(url, wait_until="load")
            valid = await page.wait_for_selector(
                'div[data-e2e="comment-emoji-icon"]', timeout=10000
            )

            if valid == None:
                tiktok_urls.remove(url)
                await page.close()
                await browser.close()
                print("🗑 Can't comment[0]" + "\033[91m {}\033[00m".format(url))

            else:
                static_comment_states = []
                for state in comment_states:
                    state_file = open(f"{comments_path}/{state}")
                    state_json = json.load(state_file)
                    static_comment_states.append([state_json["cookies"], state])
                random.shuffle(static_comment_states)

                # 💬💬💬💬
                for state in static_comment_states:
                    state_file = open(f"{comments_path}/{state[1]}")
                    state_json = json.load(state_file)
                    await browser.contexts[0].add_cookies(state_json["cookies"])
                    await page.reload(wait_until="load")

                    await page.click("text=Add comment...", timeout=5000)

                    com = random.choice(comments)
                    await page.keyboard.type(com)
                    await page.keyboard.press("Enter")

                    comment_posted = await page.wait_for_selector(
                        "text=Comment posted", timeout=10000
                    )

                    global d
                    if (
                        comment_posted != None
                        and await comment_posted.inner_text() == "Comment posted"
                    ):
                        d += 1
                        await page.click('span[data-e2e="comment-like-count"]')
                        await page.wait_for_timeout(2000)
                    print("\r" + f" [{d} / {f}]", end="")

                    # save
                    await browser.contexts[0].storage_state(
                        path=f"{comments_path}/{state[1]}"
                    )
                    # save
                    # 💬💬💬💬

                await page.close()
                await browser.close()

        await asyncio.gather(*(comment_w_states(url) for url in tiktok_urls))

        print("\n💬" + "\033[96m {}\033[00m".format(datetime.now().strftime("%H:%M")))

        j = len(like_states) * len(tiktok_urls)
        global i
        i = 0
        global c
        c = 0

        static_like_states = []
        for state in like_states:
            state_file = open(f"{like_path}/{state}")
            state_json = json.load(state_file)
            static_like_states.append([state_json["cookies"], state])
        random.shuffle(static_like_states)

        jsEval = open("./jsEval.js").read()

        async def find_comments(url):

            # 💚💚💚💚
            start_time = datetime.now()
            for state in static_like_states:
                if (datetime.now() - start_time).seconds > 60 * 25:
                    # max time
                    break

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
                await page.click("text=Add comment...", timeout=5000)

                if i < 20:
                    await page.wait_for_timeout(60000)
                    hearts = await page.query_selector_all(
                        'span[data-e2e="comment-like-count"]'
                    )
                    if hearts != None and hearts.__len__() > 0:
                        for heart in hearts:
                            await heart.click()
                            c += 1
                            print("\r" + f" [{i} / {j}] [{c}]", end="")
                            await page.wait_for_timeout(2000)
                    # found = await page.wait_for_selector("div[plywr]", timeout=1000)

                else:
                    hearts = await page.query_selector_all(
                        'span[data-e2e="comment-like-count"]'
                    )
                    if hearts != None and hearts.__len__() > 0:
                        for heart in hearts:
                            await heart.click()
                            c += 1
                            print("\r" + f" [{i} / {j}] [{c}]", end="")
                            await page.wait_for_timeout(2000)
                    # found = await page.wait_for_selector("div[plywr]", timeout=20000)

                # if found != None:
                #     not_liked = await page.query_selector_all(
                #         'div[plywr] svg[fill="rgba(22, 24, 35, 1)"]'
                #     )
                #     if len(not_liked) > 0:
                #         for heart in not_liked:
                #             await heart.click()
                #             await page.wait_for_timeout(1000)
                #             c += 1
                #             print("\r" + f" [{i} / {j}] [{c}]", end="")

                # reply
                # r = [1, 0, 0]
                # if state[1] in repliers and random.choice(r) == 1:
                #     await page.click(
                #         'span[data-e2e="comment-reply-1"]', timeout=1000
                #     )
                #     await page.keyboard.type(random.choice(reply_comments))
                #     await page.keyboard.press("Enter")
                #     # await page.wait_for_timeout(1000)

                # else:
                #     pass
                # print("🔍❌ " + "\033[91m {}\033[00m".format(url))

                # save
                await browser.contexts[0].storage_state(path=f"{like_path}/{state[1]}")
                # save
                # 💚💚💚💚

                await page.close()
                await browser.close()

        await asyncio.gather(*(find_comments(url) for url in tiktok_urls))

    print("\n🏁" + "\033[96m {}\033[00m".format(datetime.now().strftime("%H:%M")))


asyncio.run(main())
