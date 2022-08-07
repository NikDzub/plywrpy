from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import asyncio
import shutil
import os
import random

head = False
edit_profile = True
edit_user_name = False


# 👤 states
states_path = "./allStates/giftStates"
states = os.listdir(states_path)
if ".DS_Store" in states:
    states.remove(".DS_Store")

# 🖼 pfps
pic_path = "./media/pfps/gift"
pics = os.listdir(pic_path)
if ".DS_Store" in pics:
    pics.remove(".DS_Store")

# 📝 bios
bio_line_1 = [
    "Looking for The Gift? 🔍",
]
bios_line_2 = ["Google it > [ site:4gift.site ]"]


names = ["Read Bio"]

# handles
async def block_media(route, req):
    if req.resource_type in {"ximage", "media", "font", "xstylesheet"}:
        try:
            await route.abort()
        except:
            pass


async def get_user_id(res):
    try:
        body = await res.body()
        decoded_body = eval(body)
        if "user_id" in decoded_body["data"]:
            global id
            id = decoded_body["data"]["user_id"]
    except:
        pass


print(
    "\033[96m {}\033[00m".format(f"edit={edit_profile} -- {states_path} -- {pic_path}")
)


# ▶️
async def main():
    i = 0
    states_len = len(states)
    async with async_playwright() as p:
        for state in states:
            i = i + 1
            global id
            id = False

            state = state.replace(".json", "")

            browser = await p.chromium.launch(headless=head)
            await browser.new_context(storage_state=f"./{states_path}/{state}.json")
            await browser.contexts[0].route("**/*", block_media)
            page = await browser.contexts[0].new_page()
            await stealth_async(page)

            # get user id (if logged)
            page.on("response", lambda res: get_user_id(res))
            await page.goto("https://www.tiktok.com", wait_until="load")
            await page.reload(wait_until="load")
            await page.goto("https://www.tiktok.com/search/user?q=", wait_until="load")
            await page.wait_for_timeout(2000)

            if id != False:
                await page.goto(f"https://www.tiktok.com/@{id}", wait_until="load")

                if edit_profile:
                    # pfp🖼
                    page.on(
                        "filechooser",
                        lambda file_chooser: file_chooser.set_files(
                            f"{pic_path}/{random.choice(pics)}"
                        ),
                    )
                    await page.click("text=Edit profile")
                    await page.click('input[type="file"]')
                    await page.click("text=Apply")
                    await page.wait_for_timeout(500)
                    # pfp🖼

                    # user name
                    if edit_user_name:
                        await page.fill(
                            'input[placeholder="Username"]',
                            f"1_new_gift_{i}",
                        )
                        await page.wait_for_timeout(1000)
                    # user name

                    # bio
                    await page.fill(
                        'textarea[data-e2e="edit-profile-bio-input"]',
                        random.choice(bio_line_1),
                    )
                    await page.wait_for_timeout(1500)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(1500)
                    await page.keyboard.type(random.choice(bios_line_2))
                    await page.wait_for_timeout(1500)
                    # bio

                    # display name
                    await page.fill(
                        'input[placeholder="Name"]',
                        random.choice(names),
                    )
                    await page.wait_for_timeout(1500)
                    # display name

                    await page.click('button[data-e2e="edit-profile-save"]')

                    if edit_user_name:
                        await page.click(
                            'button[data-e2e="set-username-popup-confirm"]'
                        )
                    await page.wait_for_timeout(3000)

                # save
                await browser.contexts[0].storage_state(
                    path=f"{states_path}/{state}.json"
                )
                # save
                print(f"[{i}/{states_len}]{state} ✅")

            else:
                print(f"[{i}/{states_len}]{state} ❌")
                cwd = os.getcwd()
                sp = states_path.replace("./", "")  # "allStates/likeStates"
                shutil.move(
                    f"{cwd}/{sp}/{state}.json",
                    f"{cwd}/allStates/brokenStates/{state}.json",
                )
                # os.remove(f"{states_path}/{state}.json")

            await page.close()
            await browser.close()


asyncio.run(main())