# npm run fam ; cd -- && cd desktop/code/plywrpy && python wrlo2.py && cd -- && cd desktop/code/plywr &&
# sudo nvram -c ; sudo shutdown -r now
import os
import json
import asyncio
import random
from datetime import datetime
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

cwd = os.getcwd()

head = True
comments = [
    "I was wondering why the frisbee kept getting bigger and bigger, but then it hit me.",
    "Most people are shocked when they find out how bad I am as an electrician.",
    "What did Yoda say when he saw himself in 4k?",
    "Why did the blue jay get in trouble at school?",
    "What social event do spiders love to attend?",
    "What is brown, hairy and wears sunglasses?",
    "Why can't you ever tell a joke around glass?",
    "6:30 is the best time on a clock, hands down.",
    "What goes up and down but doesn't move?",
    "If April showers bring May flowers, what do May flowers bring?",
    "What's the difference between a hippo and a Zippo?",
    "How do you find Will Smith in a snowstorm?",
    "What is orange and sounds like a parrot?",
    "Why did Tigger go to the bathroom?",
    "What do you call a snail on a ship?",
    "I travel all around the world, but never leave the corner. What am I?",
    "What type of music do rabbits listen to?",
    "I have a neck but no head, and I wear a cap. What am I?",
    "In what sort of glass should you never pour expensive wine?",
    "There are two monkeys on a tree and one jumps off. Why does the other monkey jump too?",
    "There are 30 cows in a field, and 28 chickens. How many didn't?",
    "Why did Snap, Crackle and Pop get scared?",
]

tiktok_urls = json.load(open(cwd + "/urls.json", encoding="utf-8"))

comments_path = "./bioStates"
comment_states = os.listdir(comments_path)
# comment_states.remove(".DS_Store")

states = os.listdir(cwd + "/states")
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
                    await page.reload(wait_until="domcontentloaded")

                    valid_in_state = await page.locator(
                        'span[data-e2e="comment-icon"]'
                    ).is_visible()
                    if valid_in_state:
                        # await page.click("video")
                        await page.click('span[data-e2e="comment-icon"]', timeout=1000)
                        await page.click(
                            'div[data-e2e="comment-emoji-icon"]', timeout=1000
                        )
                        com = random.choice(comments)
                        await page.keyboard.type(com)
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
            static_states.append(state_json["cookies"])

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
                await browser.contexts[0].add_cookies(state)
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

                else:
                    pass
                    # print("🔍❌ " + "\033[91m {}\033[00m".format(url))

                await page.close()
                await browser.close()

        await asyncio.gather(*(find_comments(url) for url in tiktok_urls))

    print("\n🏁" + "\033[96m {}\033[00m".format(datetime.now().strftime("%H:%M:%S")))


asyncio.run(main())
