# npm run fam ; cd -- && cd desktop/code/plywrpy && python myl.py && cd -- && cd desktop/code/plywr &&
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
    "Its So easy, Check my pic",
    "Check my pic",
    "Look At My Pfp",
    "Google 00qq00bb",
    "Google VL64YE84",
]
cwd = os.getcwd()

tiktok_urls = json.load(open(cwd + "/urls.json", encoding="utf-8"))


states = os.listdir(cwd + "/states")
comment_states = os.listdir(cwd + "/commentStates")
states.remove(".DS_Store")
comment_states.remove(".DS_Store")


async def block_media(route, req):
    # "image", "media", "font", "stylesheet"
    if req.resource_type in {"image", "media", "font", "stylesheet"}:
        try:
            await route.abort()
        except:
            pass


async def main():
    print("\033[96m {}\033[00m".format(datetime.now().strftime("%H:%M:%S")))

    async with async_playwright() as p:

        async def comment_w_states(url):
            print("\033[96m {}\033[00m".format(url))
            browser = await p.chromium.launch(headless=head)
            page = await browser.new_page()
            await stealth_async(page)
            await browser.contexts[0].route("**/*", block_media)

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
                print("🗑 Can't comment" + "\033[91m {}\033[00m".format(url))
            else:
                for state in comment_states:
                    state_file = open(f"commentStates/{state}")
                    state_json = json.load(state_file)
                    await browser.contexts[0].add_cookies(state_json["cookies"])
                    await page.goto(url, wait_until="load")

                    await page.click('span[data-e2e="comment-icon"]')
                    await page.click('div[data-e2e="comment-emoji-icon"]')
                    com = random.choice(comments)
                    await page.keyboard.type(com)
                    await page.keyboard.press("Enter")
                    await page.wait_for_selector("text=Comment posted")

                    storage = await browser.contexts[0].storage_state(
                        path=f"commentStates/{state}"
                    )
                await page.close()
                await browser.close()

        # await asyncio.gather(*(comment_w_states(url) for url in tiktok_urls))

        print(
            "Done Commenting"
            + "\033[96m {}\033[00m".format(datetime.now().strftime("%H:%M:%S"))
        )

        async def find_comments(url):

            browser = await p.chromium.launch(headless=head)
            await browser.new_context(storage_state="states/ihptto.json")
            page = await browser.contexts[0].new_page()
            await stealth_async(page)
            await browser.contexts[0].route("**/*", block_media)

            await page.goto(url, wait_until="load")

            await page.evaluate(
                """
                    document.querySelector('body').style.backgroundColor = 'yellow';
                    let comments = [
                        'deserve',
                        'Its So easy, Check my pic',
                        'Check my pic',
                        'Look At My Pfp',
                        'Google 00qq00bb',
                        'Google VL64YE84',
                        ];
                    document
                    .querySelector('div[class*="DivCommentItemContainer"]')
                    ?.scrollIntoView();
                    let scrollInt = setInterval(() => {
                    window.scrollBy(0, 2);
                    window.scrollBy(0, -2);
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
                            e.querySelectorAll('svg[fill="rgba(0, 0, 0, 1.0)"]').forEach((e) => {
                            e.setAttributeNode(liked);
                            e.setAttribute('liked', 'false');
                            });
                        } else {
                            e.remove();
                        }
                        });
                    document.querySelector('body').style.backgroundColor = 'blue';
                    }, 3000);
                    setTimeout(() => {
                    clearInterval(scrollInt);
                    document.querySelector('body').style.backgroundColor = 'green';
                    }, 10000);
                    """
            )
            await page.wait_for_timeout(15000)
            found = await page.wait_for_selector('svg[liked="false"]', timeout=1000)

            if found != None:
                not_liked = await page.query_selector_all(
                    'div[plywr] [data-e2e="comment-like-count"]'
                )
                if len(not_liked) > 0:
                    # print("\033[96m {}\033[00m".format(url))

                    for state in states:
                        print(state)

                        temp_browser = await p.chromium.launch(headless=True)
                        temp_page = await temp_browser.new_page()
                        await stealth_async(temp_page)
                        await temp_browser.contexts[0].route("**/*", block_media)

                        state_file = open(f"states/{state}")
                        state_json = json.load(state_file)
                        await temp_browser.contexts[0].add_cookies(
                            state_json["cookies"]
                        )

                        await temp_page.goto(url, wait_until="load")
                        sess_sto = await temp_page.evaluate(
                            """
                            () => {
                            let sessionArray = [];
                            for (let key in window.sessionStorage) {
                                if (typeof window.sessionStorage[key] == 'string') {
                                let vk = [];
                                vk.push(key, window.sessionStorage[key]);
                                console.log(vk);
                                sessionArray.push(vk);
                                }
                            }
                            return sessionArray;
                            };

                        """
                        )
                        storage = await temp_browser.contexts[0].storage_state(
                            path=f"states/{state}"
                        )
                        await temp_page.close()
                        await temp_browser.close()
                        # _______________________________________
                        state_file = open(f"states/{state}")
                        state_json = json.load(state_file)
                        # await browser.contexts[0].clear_cookies()
                        await browser.contexts[0].add_cookies(state_json["cookies"])
                        loc_sto = state_json["origins"][0]["localStorage"]

                        # await page.evaluate("window.localStorage.clear()")
                        # await page.evaluate("window.sessionStorage.clear()")
                        for val in loc_sto:

                            await page.evaluate(
                                """val => {
                            window.localStorage.setItem(val.name, val.value);
                            }""",
                                val,
                            )
                        for val in sess_sto:
                            print(val)
                            await page.evaluate(
                                """val => {
                            window.sessionStorage.setItem(val[0], val[1]);
                            }""",
                                val,
                            )

                        print("new")
                        for heart in not_liked:
                            await heart.click()
                            print("click1")
                            await page.wait_for_timeout(2000)
                            await heart.click()
                            print("click2")
                            await page.wait_for_timeout(2000)

            else:
                pass
                # print("🔍❌ " + "\033[91m {}\033[00m".format(url))

            await page.close()
            await browser.close()

        await asyncio.gather(*(find_comments(url) for url in tiktok_urls))

    print("\033[96m {}\033[00m".format(datetime.now().strftime("%H:%M:%S")))


asyncio.run(main())
