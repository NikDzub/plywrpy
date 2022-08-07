import asyncio
import os


cwd = os.getcwd()

states = os.listdir(cwd + "/states")
states.remove(".DS_Store")


async def main():

    for state in states:
        if "sesmonkdextbert1975" in state:
            print(state)
        else:
            print(f"{state}   badd")
            # os.remove(f"states/{state}")


asyncio.run(main())
