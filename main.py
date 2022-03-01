"""
put usernames you wanna check in data/usernames.txt 
"""
import os
import asyncio
import aiohttp
import logging

logging.basicConfig(
    level=logging.INFO,
    format="\033[38;5;21m[\033[0m%(asctime)s.%(msecs)03d\033[38;5;21m] \033[0m%(message)s\033[0m", 
    datefmt="%H:%M:%S" 
)

class Checker(object):
    def __init__(self, delay: int) -> None:
        self.Usernames = [str(user) for user in open("data/usernames.txt", "r").read().splitlines()]
        self.checkedUsernames = [str(checked) for checked in open("data/checked_usernames.txt", "r").read().splitlines()]
        self.delay = delay
        self.clear = lambda: os.system("cls; clear")
        self.clear()

    async def checkUser(self, user: str):
        async with aiohttp.ClientSession() as HTTPClient:
            async with HTTPClient.get("https://github.com/{}".format(user)) as response:
                
                if (response.status in range(200, 299)):
                    logging.info("{} is not available.".format(user))
                    with open("data/checked_usernames.txt", "a+") as file:
                        file.write(user + "\n")

                elif (response.status == 404):
                    logging.info("{} is available!".format(user))
                    with open("data/available_usernames.txt", "a+") as file:
                        file.write(user + "\n")
                    with open("data/checked_usernames.txt", "a+") as file:
                        file.write(user + "\n")

                else:
                    logging.info(await response.text())
                
    async def start(self):
        for user in self.Usernames:
            if (user in self.checkedUsernames):
                logging.info("{} is already checked!".format(user))
            else:
                await self.checkUser(user)
                if self.delay != 0: await asyncio.sleep(self.delay)
        print()
        logging.info("Program is finished.")

if __name__ == "__main__":
    client = Checker(
        delay = int(input("\033[38;5;21m> \033[0mDelay Per Request \033[38;5;21m[\033[0mPut 0 If None\033[38;5;21m]: \033[0m"))
    )
    loop = asyncio.get_event_loop()
    try: loop.run_until_complete(client.start())
    except (Exception) as error: logging.error(error)
