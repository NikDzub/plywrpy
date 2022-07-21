# npm run fam ; cd -- && cd desktop/code/plywrpy && python myl.py && cd -- && cd desktop/code/plywr &&
# nvram -c && sudo shutdown -r now
import os
import shutil
import json
import asyncio
import random
from datetime import datetime

now = datetime.now()

from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

head = False

comments = ["Thats preety sweet", "I Like it picasso", "My pic"]

cwd = os.getcwd()


tiktok_urls = json.load(open(cwd + "/urls.json", encoding="utf-8"))
comented_urls = []


def get_browsers():
    global comment_browsers
    comment_browsers = {}
    for folder in os.listdir(cwd):
        if "commentBrowsers" in folder:
            users = []
            for user in os.listdir(cwd + f"/{folder}"):
                if ".DS_Store" not in user:
                    users.append(user)

            comment_browsers[folder] = users


states = os.listdir(cwd + "/states")
states.remove(".DS_Store")
comment_states = os.listdir(cwd + "/commentStates")
comment_states.remove(".DS_Store")


def clean_browsers():
    cache_folders = [
        "Cache",
        "Code Cache",
        "Local Storage",
        "Session Storage",
        "Sessions",
    ]
    for user in comment_browsers:
        for cache_folder in cache_folders:
            try:
                shutil.rmtree(cwd + f"/commentBrowsers/{user}/Default/" + cache_folder)
            except:
                continue


async def block_media(route, req):
    # "image", "media", "font", "stylesheet"
    if req.resource_type in {"image", "media", "font", "stylesheet"}:
        try:
            await route.abort()
        except:
            pass


get_browsers()
# -------------------------------------
async def main():

    print("\033[91m {}\033[00m".format(now.strftime("%H:%M:%S")))

    async with async_playwright() as p:

        async def comment_w_states(url):
            browser = await p.chromium.launch(headless=head)
            page = await browser.new_page()

            await stealth_async(page)
            # await browser.contexts[0].route("**/*", block_media)
            state_file = open(f"commentStates/camptopoback1989.json")
            state_json = json.load(state_file)
            await browser.contexts[0].add_cookies(state_json["cookies"])

            await page.goto(url, wait_until="load")
            valid = await page.wait_for_selector(
                'div[data-e2e="comment-emoji-icon"]', timeout=2000
            )
            if valid == None:
                await page.close()
                print("🗑 " + "\033[91m {}\033[00m".format(url))
            else:
                for state in comment_states:
                    state_file = open(f"commentStates/{state}")
                    state_json = json.load(state_file)
                    await browser.contexts[0].add_cookies(state_json["cookies"])

                    # await page.reload(wait_until="load")

                    await page.click('div[data-e2e="comment-emoji-icon"]')
                    com = random.choice(comments)
                    await page.keyboard.type(com)
                    await page.keyboard.press("Enter")

                    await page.wait_for_selector("text=Comment posted")
                    await page.bring_to_front()
                    await page.wait_for_timeout(1000)
                await page.close()
                await browser.close()

        await asyncio.gather(*(comment_w_states(url) for url in tiktok_urls))

        print("\033[91m {}\033[00m".format(now.strftime("%H:%M:%S")))

        # -------------------------------------

        async def find_comments(url):

            browser = await p.chromium.launch(headless=head)

            await browser.new_context(storage_state="states/_google_vl64ye84.json")
            await browser.contexts[0].route("**/*", block_media)
            page = await browser.contexts[0].new_page()
            await stealth_async(page)

            await page.goto(url, wait_until="load")
            await page.evaluate(
                """
                                document.querySelector('body').style.backgroundColor = 'yellow';
                                let comments = [
                                    "Thats preety sweet",
                                    "My pic",
                                    "I Like it picasso"
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
                                }, 90000);
                                """
            )
            await page.wait_for_timeout(90000)
            found = await page.wait_for_selector('svg[liked="false"]', timeout=1000)
            if found != None:

                not_liked = await page.query_selector_all(
                    'div[plywr] [data-e2e="comment-like-count"]'
                )
                if len(not_liked) > 0:
                    print("\033[96m {}\033[00m".format(url))
                    for heart in not_liked:
                        await heart.click()
                        await page.wait_for_timeout(2000)

                    for state in states:
                        state_file = open(f"states/{state}")
                        state_json = json.load(state_file)
                        await browser.contexts[0].add_cookies(state_json["cookies"])
                        await page.bring_to_front()
                        for heart in not_liked:
                            await heart.click()
                            await page.wait_for_timeout(2000)
                            await heart.click()
                            await page.wait_for_timeout(2000)

                        # print(f"{state} 💚")
            else:
                print("🔍❌ " + "\033[91m {}\033[00m".format(url))
            await page.close()
            await browser.close()

        await asyncio.gather(*(find_comments(url) for url in tiktok_urls))

    clean_browsers()
    print("\033[91m {}\033[00m".format(now.strftime("%H:%M:%S")))


asyncio.run(main())
