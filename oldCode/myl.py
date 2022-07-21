# npm run fam ; cd -- && cd desktop/code/plywrpy && python myl.py && cd -- && cd desktop/code/plywr &&
import os
import shutil
import json
import asyncio
import random
from datetime import datetime

now = datetime.now()

from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

head = True

comments = ["Check My Bio g"]

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

        async def comment_fore_br(commenter, browser_folder):

            browser = await p.chromium.launch_persistent_context(
                cwd + f"/{browser_folder}/{commenter}", headless=head
            )

            await browser.route("**/*", block_media)
            page = browser.pages[0]
            await stealth_async(page)
            await page.goto("https://www.tiktok.com/search?q=", wait_until="load")

            for url in tiktok_urls:
                url_page = await browser.new_page()
                await stealth_async(url_page)
                await url_page.goto(url, wait_until="load")
                valid = await url_page.wait_for_selector(
                    'div[data-e2e="comment-emoji-icon"]', timeout=2000
                )
                if valid == None:
                    await url_page.close()
                    print("🗑 " + "\033[91m {}\033[00m".format(url))

            for page in browser.pages:

                async def post_comment():
                    if "@" in page.url:
                        short_url = page.url.replace("https://www.tiktok.com/", "")
                        await page.click('div[data-e2e="comment-emoji-icon"]')

                        cur_top_com = await page.wait_for_selector(
                            'p[data-e2e="comment-level-1"]'
                        )
                        cur_top_com = await cur_top_com.inner_text()
                        cur_top_com = cur_top_com.replace("@", "")

                        com = random.choice(comments)

                        await page.keyboard.type(com)
                        await page.keyboard.press("Enter")
                        await page.bring_to_front()
                        await page.wait_for_selector("text=Comment posted")
                        # await page.click('span[data-e2e="comment-like-count"]')
                        await page.wait_for_timeout(2000)

                        # await page.keyboard.type(random.choice(comments))
                        # await page.keyboard.press("Enter")
                        # await page.wait_for_selector("text=Comment posted")
                        # await page.click('span[data-e2e="comment-like-count"]')
                        print(
                            com.split(" ")[0]
                            + "..💬"
                            + "\033[94m {}\033[00m".format(short_url)
                        )
                        if page.url not in comented_urls:
                            comented_urls.append(page.url)
                        await page.wait_for_timeout(1000)
                        await page.close()

                await post_comment()
            await browser.close()

        for browser_folder in comment_browsers.keys():
            await asyncio.gather(
                *(
                    comment_fore_br(user, browser_folder)
                    for user in comment_browsers[browser_folder]
                )
            )
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
                                    ""Check My Bio g"",
                                    "Check my avatar",
                                    "I Googled it"
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
