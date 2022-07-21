import os
import shutil
import json
import asyncio
import random
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async


# npm run fam ; cd -- && cd desktop/code/plywrpy && python myl.py && cd -- && cd desktop/code/plywr &&
head = True


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
    "bon bas il faut sortir la ventouse à chiot 😅😅",
    "PARTI 3 SLiME XXL EN POLYSTYRÈNE",
    "Tu as fait quoi au toilette",
    "_vl64ye84",
]


user_agents = [
    "Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.7.12) Gecko/20050915",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.7.6) Gecko/20050319",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; fr-FR; rv:1.7.11) Gecko/20050727",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.7.13) Gecko/20060414",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X; U; nb; rv:1.7.5) Gecko/20041110",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; nl-NL; rv:1.8.1.3) Gecko/20080722",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.5.1) Gecko/20031120",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1.11) Gecko/20071127",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; de-AT; rv:1.7.8) Gecko/20050511",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; de-AT; rv:1.7b) Gecko/20040421",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:0.9.7) Gecko/20011221",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; de-AT; rv:1.8b) Gecko/20050217",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.8b2) Gecko/20050702",
]

get_urls()
get_browsers()
clean_browsers()


async def block_media(route, req):
    # "image", "media", "font", "stylesheet"
    if req.resource_type in {"image", "media", "font", "stylesheet"}:
        try:
            await route.abort()
        except:
            pass


async def main():
    async with async_playwright() as p:

        async def commenters_browsers(commenter):
            browser = await p.chromium.launch_persistent_context(
                cwd + f"/commentBrowsers/{commenter}",
                headless=head,
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
                        rejecting_values = (
                            "sdfvl64ye84",
                            "ihptto",
                            "cojeb65",
                            "colegrr",
                            "gigiwex3",
                        )
                        short_url = page.url.replace("https://www.tiktok.com/", "")

                        try:
                            await page.wait_for_selector(
                                'div[class*="DivCommentListContainer"]', timeout=10000
                            )
                            all_comments = await page.text_content(
                                'div[class*="DivCommentListContainer"]'
                            )
                            allready_commented = any(
                                rejecting_value in all_comments
                                for rejecting_value in rejecting_values
                            )
                            if allready_commented:
                                await page.close()
                                try:
                                    tiktok_urls.remove(page.url)
                                    print(f"REMOVED > {page.url} 🗑")
                                except:
                                    pass
                            else:
                                await page.click('div[class*="DivLikeWrapper"]')
                                await page.click('div[data-e2e="comment-emoji-icon"]')
                                random_comment = random.choice(comments)
                                await page.keyboard.type(random_comment)
                                await page.keyboard.press("Enter")
                                try:
                                    await page.wait_for_selector("text=Comment posted")
                                    await page.bring_to_front()
                                    await page.click('div[class*="DivLikeWrapper"]')
                                    await page.wait_for_timeout(2020)
                                    await page.click(
                                        'button[class*="ButtonActionItem"]'
                                    )
                                    await page.wait_for_timeout(333)
                                    print(
                                        f"{commenter} 💬✅ {random_comment} > {short_url}"
                                    )
                                except:
                                    print(
                                        f"{commenter} 💬❌ {random_comment} > {short_url}"
                                    )
                                await page.close()
                        except:
                            await page.close()
                            try:
                                tiktok_urls.remove(page.url)
                                print(f"VIDEO ISNT AVIALBLE {page.url} 🗑")
                            except:
                                pass

                await post_comment()
            await browser.close()

        await asyncio.gather(
            *(commenters_browsers(commenter) for commenter in comment_browsers)
        )

        async def find_comments(user, browsers_folder):

            browser = await p.chromium.launch_persistent_context(
                cwd + f"/{browsers_folder}/{user}",
                headless=head,
                # viewport={"width": 400, "height": 600},
            )
            await browser.route("**/*", block_media)
            page = browser.pages[0]
            await stealth_async(page)
            await page.goto("https://www.tiktok.com/search?q=")
            try:
                # await page.wait_for_selector(
                #    'div[data-e2e="inbox-icon"]', timeout=10000
                # )
                print("bleh")
            except:
                print(f"⛔️⛔️⛔️ {browsers_folder}/{user}>NOT CONNECTED ⛔️⛔️⛔️")
                await browser.close()
                pass
            else:

                for url in tiktok_urls:
                    url_page = await browser.new_page()
                    await stealth_async(url_page)
                    await url_page.goto(url, wait_until="domcontentloaded", timeout=0)

                for page in browser.pages:

                    async def scroll_pages(page):
                        if "video" in page.url:
                            await page.click('button[class*="ButtonActionItem"]')
                            await page.evaluate(
                                """
                                document.querySelector('body').style.backgroundColor = 'grey';
                                let comments = [
                                  "can you see my pic",
                                  "vl64ye84"
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

                print(f"{user} > LOADING... COMMENTS ⏳")
                await page.wait_for_timeout(60000)
                print(f"{user} > LOADED!!! COMMENTS ⌛️")

                for page in browser.pages:
                    if "video" in page.url:
                        short_url = page.url.replace("https://www.tiktok.com/", "")
                        not_liked = await page.query_selector_all('svg[liked="false"]')
                        if len(not_liked) > 0:
                            for heart in not_liked:
                                # await page.bring_to_front()
                                await heart.click()
                                await page.wait_for_timeout(3040)
                                print(f"{user} 💚 {page.url}")
                                urls_comment_found.update(url_page)
                                print(urls_comment_found)
                        else:
                            print(f"{user} ❌ {short_url}")

                        await page.close()

                await browser.close()

        for browser in all_browsers.keys():
            if len(tiktok_urls) > 0:
                print(f"{browser} 🤖")
                await asyncio.gather(
                    *(find_comments(user, browser) for user in all_browsers[browser])
                )

    clean_browsers()


asyncio.run(main())
