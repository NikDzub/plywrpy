# npm run fam ; cd -- && cd desktop/code/plywrpy && python stst.py && cd -- && cd desktop/code/plywr &&
# sudo nvram -c ; sudo shutdown -r now
import os
import json
import asyncio
import random
from datetime import datetime


from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

cwd = os.getcwd()


head = False

comments_path = "./bioStates"
comment_states = os.listdir(comments_path)
# comment_states.remove(".DS_Store")

comments_0 = [
    "My New Pic",
    "DAMN🦊 Check our profile",
    "Check this,Look at my Pic 🦊",
    "My pictue lol 🦊",
    "Do u like my new picture?",
    "I Got a new picture now",
    "You are amaziinng!",
]
comments_1 = [
    "That is truly amazing!",
    "That was so unexpected",
    "I Just cant wait",
    "I Dont know how to react",
    "that was kinda cool",
]


tiktok_urls = json.load(open(cwd + "/urls.json", encoding="utf-8"))


states = os.listdir(cwd + "/states")
states.remove(".DS_Store")


async def block_media(route, req):
    # "image", "media", "font", "stylesheet"
    if req.resource_type in {"ximage", "media", "font", "stylesheet"}:
        try:
            await route.abort()
        except:
            pass


# -------------------------------------
async def main():

    print("\033[91m {}\033[00m".format(datetime.now().strftime("%H:%M:%S")))

    async with async_playwright() as p:

        async def comment_w_states(url):
            browser = await p.chromium.launch(headless=head)
            page = await browser.new_page()

            await stealth_async(page)
            await browser.contexts[0].route("**/*", block_media)
            state_file = open(f"{comments_path}/{comment_states[0]}")
            state_json = json.load(state_file)
            await browser.contexts[0].add_cookies(state_json["cookies"])

            await page.goto(url, wait_until="load")
            valid = await page.wait_for_selector(
                'div[data-e2e="comment-emoji-icon"]', timeout=2000
            )
            if valid == None:
                await page.close()
                await browser.close()
                print("🗑 " + "\033[91m {}\033[00m".format(url))
            else:
                randomized_states = random.sample(comment_states, len(comment_states))
                for state in randomized_states:

                    state_file = open(f"{comments_path}/{state}")
                    state_json = json.load(state_file)
                    await browser.contexts[0].add_cookies(state_json["cookies"])

                    await page.goto(url, wait_until="load")
                    await page.click('span[data-e2e="comment-icon"]')

                    await page.click('div[data-e2e="comment-emoji-icon"]')
                    com = random.choice(comments_1)
                    await page.keyboard.type(com)
                    await page.keyboard.press("Enter")
                    await page.wait_for_selector("text=Comment posted", timeout=5000)

                    # await page.bring_to_front()
                    # await page.wait_for_timeout(1000)
                    # storage = await browser.contexts[0].storage_state(
                    #     path=f"states/{state}"
                    # )
                await page.close()
                await browser.close()

        await asyncio.gather(*(comment_w_states(url) for url in tiktok_urls))

        print("\033[91m {}\033[00m".format(datetime.now().strftime("%H:%M:%S")))

        # -------------------------------------

        async def find_comments(url):

            browser = await p.chromium.launch(headless=head)

            await browser.new_context(storage_state="states/00qq00bb.json")
            await browser.contexts[0].route("**/*", block_media)
            page = await browser.contexts[0].new_page()
            await stealth_async(page)

            await page.goto(url, wait_until="load")
            await page.evaluate(
                """
                                document.querySelector('body').style.backgroundColor = 'yellow';
                                let comments = [
                                    "That is truly amazing",
                                    "That was so unexpected",
                                    "I Just cant wait",
                                    "I Dont know how to react",
                                    "that was kinda cool",
                                ];
                                document
                                    .querySelector('div[class*="DivCommentItemContainer"]')
                                    ?.scrollIntoView();
                                let scrollInt = setInterval(() => {
                                    window.scrollBy(0,2)
                                    window.scrollBy(0,-2)
                                document
                                    .querySelectorAll('div[class*="DivCommentItemContainer"]')
                                    .forEach((e) => {
                                      if (
                                        typeof e.textContent === 'string' &&
                                        comments.some((comment) => {
                                          return new RegExp(comment).test(e.textContent);
                                        })
                                      ) {
                                        //clearInterval(scrollInt);
                                        e.scrollIntoView();
                                        const atr = document.createAttribute('plywr');
                                        const liked = document.createAttribute('liked');
                                        e.setAttributeNode(atr);
                                        e.setAttribute('plywr', 'true');
                                        e.querySelectorAll('svg[fill="rgba(0, 0, 0, 1.0)"]').forEach(
                                        (e) => {
                                            e.setAttributeNode(liked);
                                            e.setAttribute('liked', 'false');
                                        }
                                        );
                                    }
                                    else {
                                        e.remove();
                                    }
                                    });
                                }, 3000);
                                setTimeout(() => {
                                  clearInterval(scrollInt);
                                  document.querySelector('body').style.backgroundColor = 'green';
                                }, 50000);
                                """
            )
            await page.wait_for_timeout(50000)
            found = await page.wait_for_selector('svg[liked="false"]', timeout=1000)
            if found != None:

                not_liked = await page.query_selector_all(
                    'div[plywr] [data-e2e="comment-like-count"]'
                )
                if len(not_liked) > 0:
                    print("\033[96m {}\033[00m".format(url))

                    for heart in not_liked:
                        await page.wait_for_timeout(1000)
                        await heart.click()

                    randomized_states = random.sample(states, len(states))
                    for state in randomized_states:
                        # dummy_browser = await p.chromium.launch(headless=head)

                        # await dummy_browser.new_context(storage_state=f"states/{state}")
                        # await dummy_browser.contexts[0].route("**/*", block_media)
                        # dummy_page = await dummy_browser.contexts[0].new_page()
                        # await stealth_async(dummy_page)

                        # await dummy_page.goto(url, wait_until="load")
                        # storage = await dummy_browser.contexts[0].storage_state(
                        #     path=f"states/{state}"
                        # )
                        # await dummy_page.close()
                        # await dummy_browser.close()

                        state_file = open(f"states/{state}")
                        state_json = json.load(state_file)
                        await browser.contexts[0].add_cookies(state_json["cookies"])

                        # await page.bring_to_front()

                        for heart in not_liked:
                            await page.wait_for_timeout(1000)
                            await heart.click()
                            await page.wait_for_timeout(1000)
                            await heart.click()
                            await page.wait_for_timeout(1000)

                        # print(f"{state} 💚")
            else:
                print("🔍❌ " + "\033[91m {}\033[00m".format(url))
            await page.close()
            await browser.close()

        await asyncio.gather(*(find_comments(url) for url in tiktok_urls))

    print("\033[91m {}\033[00m".format(datetime.now().strftime("%H:%M:%S")))


asyncio.run(main())
