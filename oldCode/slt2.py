import os
import shutil
import json
import asyncio
import random
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async


cwd = os.getcwd()


def get_urls():
    file_path = open(cwd + "/urls.json", encoding="utf-8")
    global tiktok_urls
    tiktok_urls = json.load(file_path)


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


comments = [
    "Look my name 🙀😀2",
    "Check my name out sweet",
    "Readd my namee PEACE🙀🙀🙀",
    "READ MY NAMEE LOVE🇺🇸",
]

get_urls()
get_browsers()
clean_browsers()
# print(tiktok_urls)
# print(browsers)


async def block_media(route, req):
    # "image", "media", "font", "stylesheet"
    if req.resource_type in {"image", "media", "font", "stylesheet"}:
        await route.abort()


async def main():
    async with async_playwright() as p:

        async def commenters_browsers(commenter):
            browser = await p.chromium.launch_persistent_context(
                cwd + f"/commentBrowsers/{commenter}", headless=False
            )
            await browser.route("**/*", block_media)
            page = browser.pages[0]
            await stealth_async(page)
            await page.goto("https://www.tiktok.com/search?q=", wait_until="load")

            for url in tiktok_urls:
                url_page = await browser.new_page()
                await stealth_async(url_page)
                await url_page.goto(url)

            for page in browser.pages:

                async def post_comment():
                    if "@" in page.url:
                        short_url = page.url.replace("https://www.tiktok.com/", "")
                        # random reply
                        await page.bring_to_front()
                        await page.click('span[data-e2e="comment-reply-1"]')
                        random_comment = random.choice(comments)
                        await page.keyboard.type(random_comment)
                        await page.keyboard.press("Enter")
                        await page.click('span[data-e2e="comment-like-count"]')
                        await page.wait_for_selector("text=Comment posted")
                        # actual comment
                        random_comment = random.choice(comments)
                        await page.keyboard.type(random_comment)
                        await page.keyboard.press("Enter")
                        await page.wait_for_selector("text=Comment posted")
                        await page.click('span[data-e2e="comment-like-count"]')
                        #
                        await page.bring_to_front()
                        print(f"{commenter} >> {random_comment} >> {short_url}")
                        await page.wait_for_timeout(1000)
                        await page.close()

                await post_comment()
            await browser.close()

        await asyncio.gather(
            *(commenters_browsers(commenter) for commenter in comment_browsers)
        )

        async def find_comments(user, browsers_folder):

            browser = await p.chromium.launch_persistent_context(
                cwd + f"/{browsers_folder}/{user}",
                headless=False,
                # viewport={"width": 400, "height": 600},
            )
            await browser.route("**/*", block_media)
            page = browser.pages[0]
            await stealth_async(page)
            await page.goto("https://www.tiktok.com/search?q=")
            try:
                await page.wait_for_selector(
                    'div[data-e2e="inbox-icon"]', timeout=10000
                )
            except:
                print(f"{user} is not connected")
                await browser.close()
            else:

                for url in tiktok_urls:
                    url_page = await browser.new_page()
                    await stealth_async(url_page)
                    await url_page.goto(url, wait_until="domcontentloaded")

                for page in browser.pages:

                    async def scroll_pages(page):
                        if "@" in page.url:
                            # await page.bring_to_front()
                            # await page.wait_for_selector(
                            #     'div[class*="DivCommentItemContainer"]:last-child'
                            # )

                            await page.evaluate(
                                """
                                let comments = [
                                  "vl64ye84",
                                  "1",
                                  "lsdfsdfets gosdf dudesfdsf"
                                ];
                                document
                                    .querySelector('div[class*="DivCommentItemContainer"]')
                                    ?.scrollIntoView();
                                let scrollInt = setInterval(() => {
                                    window.scrollBy(0,5)
                                    window.scrollBy(0,-5)
                                document
                                    .querySelectorAll('div[class*="DivCommentItemContainer"]')
                                    .forEach((e) => {
                                      if (
                                        typeof e.textContent === 'string' &&
                                        comments.some((comment) => {
                                          return new RegExp(comment).test(e.textContent);
                                        })
                                      ) {
                                        clearInterval(scrollInt);
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
                                """
                            )

                    await scroll_pages(page)

                print(f"{user} started loading comments")
                await page.wait_for_timeout(90000)
                print(f"{user} stoped loading comments")

                for page in browser.pages:
                    if "@" in page.url:
                        short_url = page.url.replace("https://www.tiktok.com/", "")
                        await page.bring_to_front()
                        try:
                            print("timeout")
                            await page.wait_for_selector(
                                'svg[liked="false"]', timeout=1000
                            )
                            not_liked = await page.query_selector_all(
                                'svg[liked="false"]'
                            )
                            for heart in not_liked:
                                await page.bring_to_front()
                                await heart.click()
                                await page.wait_for_timeout(3000)
                                print(f"{user} <3 {page.url}")
                        except:
                            print(f"{user} NOT FOUND {short_url}")
                        await page.close()

                await browser.close()

        for browser in all_browsers.keys():
            print(browser)
            await asyncio.gather(
                *(find_comments(user, browser) for user in all_browsers[browser])
            )

    clean_browsers()


asyncio.run(main())
