from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import asyncio
import os
import random
from datetime import datetime


# python jstLike.py &&

head = False

# 👤 states
states_path = "./allStates/newStates"
states = os.listdir(states_path)
if ".DS_Store" in states:
    states.remove(".DS_Store")

famous = [
    "forbes",
    "wizard_of_frogz",
    "doitnowcc",
    "beasteater",
    "shaq",
    "lilnasx",
    "briandadeyanara",
    "jimena.jimenezr",
    "jdpantoja",
    "homm9k",
    "flavinhalouise",
    "spider_slack",
    "its.michhh",
    "abbieherbert",
    "virginiafonseca",
    "donaldducc",
    "yungfafii",
    "youngfurfur",
    "flyysouljah",
    "carew_ellington",
    "samanthayve",
    "rafaelsantos",
    "chantegeyser",
    "trippydraws",
    "chrissychlapecka",
    "xowiejones",
    "itsari.aleise",
    "emmanortss",
    "ladbible",
    "dermdoctor",
    "karna.val",
    "luara",
    "onlyjayus",
    "the_mannii",
    "harryjowsey",
    "heytonytv",
    "alexisnikole",
    "wisdm8",
    "parkerlocke",
    "mikaylanogueira",
    "maddiwinter",
    "devonrodriguezart",
    "brotherofcolor",
    "unique.planet",
    "_vector_",
    "eldoradomax",
    "daviddobrik",
    "mads.yo",
    "lalalandkindcafe",
    "pamibabyy",
    "ten_yujin",
    "leaelui",
    "zusjeofficial",
    "jessechrisss",
    "brookemonk_",
    "realprinceea",
    "amauryguichon",
    "jennypopach",
    "miladmirg",
    "happierthanever",
    "meredithduxbury",
    "mimiermakeup",
    "thispronto",
    "millane",
    "kodiyakredd",
    "miafaithe",
    "tarayummy",
    "daniellecohn",
    "finneas",
    "richardzoumalan",
    "nickaustinn",
    "steveharvey",
    "latto777",
    "rug",
    "shlatfish",
    "anwar",
    "annabananaxdddd",
    "anokhinalz",
    "bhadbhabie",
    "jeremylynch",
    "splack",
    "nessaabarrett",
    "soymichellemarti",
    "mackenzieziegler",
    "haileybieber",
    "megnutt02",
    "gc6ge600",
    "gc9we900",
    "miakhalifa",
    "sjbleau",
    "thegr8khalid",
    "billnye",
    "jackblack",
    "daddyyankee",
    "marcanthony",
    "livbedumb",
    "mileycyrus",
    "jlo",
    "brunomars",
    "mariahcarey",
    "camilacabello",
    "imkevinhart",
    "snoopdogg",
    "karolg",
    "willsmith",
    "taylorswift",
    "edsheeran",
    "vancityreynolds",
    "gordonramsayofficial",
    "ladygaga",
    "rosssmith",
    "jondretto",
    "hannahstocking",
    "marsaimartin",
    "bayashi.tiktok",
    "javiluna",
    "johnmarcvanwyk3",
    "mariahandbill",
    "panseriyusuf",
    "souljaboytv",
    "ondreazlopez",
    "adamw",
    "jarypatel",
    "itsdanielmac",
    "danilis_boom",
    "ttlyteala",
    "nikitadragun",
    "belitskaydi",
    "vhackerr",
    "shakira",
    "billieeilish",
    "abiel.yrd",
    "riwww",
    "badbaarbie",
    "avemoves",
    "itsavage",
    "fordjawaun",
    "katiana.kay",
    "barsa.n",
    "thatswatson",
    "fabiola.baglieri",
    "sherinicolee",
    "momonatamada",
    "therock",
    "charlyjordan",
    "gb6ae150",
    "mozkla13",
    "boomba.klat",
    "gb9ae900",
    "sabrinacarpenter",
    "guinnessworldrecords",
    "gc5we500",
    "gb6ae170",
    "outkastrep",
    "user73lg3tvf42",
    "themermaidscale",
    "coltyy",
    "shawnmendes",
    "lukedavidson_",
    "xobrooklynne",
    "gabrielabee",
    "ehbeefamily",
    "celinaspookyboo",
    "imaffaf",
    "rolyn_jay",
    "moderngoalkeeper",
    "ayypatrick",
    "anthonyriveras",
    "eloisefouladgar",
    "rus.alien",
    "mattzworld",
    "benazelart",
    "lisina15",
    "larissamanoela",
    "rileyhubatka",
    "absorber",
    "its.tmariee",
    "ashleytisdale",
    "lala_sadii",
    "nicolegarcia",
    "ivanantoniochacon",
    "derkslurp",
    "bluefacebleedem",
    "king.science",
    "theyeeetbaby",
    "newt",
    "annaxsitar",
    "paigezilba",
    "iamkelianne",
    "lowcarbstateofmind",
    "ayaatanjali_",
    "nattinatasha",
    "jxdn",
    "maxtaylorlifts",
    "blakegray",
    "sueco",
    "itspierreboo",
    "quenblackwell",
    "imdimpey",
    "mikasalamanca",
    "zeth",
    "scottkress_",
    "ninja",
    "wheezyfitness2.0",
    "billlnai",
    "liamsilk",
    "swaghoe666",
    "ramizeinn",
    "tubbynugget",
    "gevids",
    "jessvalortiz",
    "bigdaddydmurph",
    "lilireinhart",
    "thedrewlynch",
    "alexwaarren",
    "lourdasprec",
    "candacecameronb",
    "zolotova_vero",
    "jailyneojeda",
    "tommyunold",
    "imbaddiesonly",
    "otakoyakisoba",
    "noeneubanks",
    "peetmontzingo",
    "marcusolin",
    "jena",
    "munchie.michelle",
    "sssniperwolf",
    "rybkatwinsofficial",
    "esthalla",
    "itsjennadavis",
    "zhcyt",
    "cyrusdobre",
    "preston",
    "sofiedossi",
    "swagboyq",
    "youneszarou",
    "scottsreality",
    "mmmjoemele",
    "kingbach",
    "jostasy",
    "candyken",
    "keemokazi",
    "malutrevejo",
    "coileray",
    "lexibrookerivera",
    "colie.1",
    "jordynjones",
    "marinelabezer",
    "pierson",
    "jaykindafunny8",
    "lynaperezxo",
    "sommerray",
    "letwins",
    "topperguild",
    "cainguzman",
    "lance210",
    "adinross",
    "loganpaul",
    "mrbeast",
    "bradleymartyn",
    "jakepaul",
    "savv.labrant",
    "dobretwins",
    "itsjojosiwa",
    "avani",
    "babyariel",
    "dixiedamelio",
    "spencerx",
    "justmaiko",
    "domelipa",
    "cznburak",
    "lorengray",
    "bellapoarch",
    "dababy",
    "nickiminaj",
    "xoteam",
    "kyliejenner",
    "addisonre",
    "jamescharles",
    "javierr",
    "zachking",
    "stokestwins",
    "brentrivera",
    "angryreactions",
    "jasonderulo",
    "junya1gou",
    "ox_zung",
    "khaby.lame",
]

comments = ["ong", "😦", "🧐🧐", "🙃 lol", "thats right", "cool", ":)", "hey!"]

# handles
async def block_media(route, req):
    if req.resource_type in {"image", "media", "font", "stylesheet"}:
        try:
            await route.abort()
        except:
            pass


print(f"{states_path}")

# ▶️
async def main():

    async with async_playwright() as p:
        for state in states:

            browser = await p.chromium.launch(
                headless=head,
                # proxy={
                #     "server": "http://nproxy.site:10558",
                #     "username": "aZ1nUR",
                #     "password": "SYtmUSzaC8yF",
                # },
            )

            await browser.new_context(storage_state=f"{states_path}/{state}")
            await browser.contexts[0].route("**/*", block_media)
            page = await browser.contexts[0].new_page()
            await stealth_async(page)

            await page.goto(
                f"https://www.tiktok.com/@{random.choice(famous)}", wait_until="load"
            )
            await page.click("video")
            await page.reload(wait_until="load")
            await page.wait_for_timeout(5000)

            vid_valid = await page.locator(
                'div[data-e2e="comment-emoji-icon"]'
            ).is_visible()

            if vid_valid:
                await page.wait_for_selector('p[data-e2e="view-more-1"]')

                async def click_all(selector, *com):
                    j = await page.query_selector_all(selector)
                    for i in j:
                        await page.wait_for_timeout(1000)
                        await i.click()
                        if com:
                            await page.keyboard.type(random.choice(comments))
                            await page.keyboard.press("Enter")
                            await page.wait_for_selector(
                                "text=Reply sent", timeout=5000
                            )
                            await page.wait_for_timeout(1000)

                await click_all('p[data-e2e="view-more-1"]')
                await click_all('p[data-e2e="view-more-2"]')
                await click_all('span[data-e2e="comment-reply-2"]', 666)
                await click_all('span[data-e2e="comment-like-count"]')
                # save
                await browser.contexts[0].storage_state(path=f"{states_path}/{state}")
                # save

            print(datetime.now().strftime("%H:%M"))
            print(state)
            print(page.url)
            await page.close()
            await browser.close()


asyncio.run(main())
