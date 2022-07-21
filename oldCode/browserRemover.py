import os
import shutil

remove = [
    "simbaklat",
    "yungbankst",
    "whoisptto",
    "okmarkzuc",
    "sharkonuss",
    "bejen65",
    "gefbezos",
    "jaywarzs",
    "yungfurfur",
    "yungfafii",
    "yoforam3",
]


def remove_browsers():
    cwd = os.getcwd()
    for user in remove:
        shutil.rmtree(cwd + "/browsers2/" + user)
        print(cwd + "/browsers2/" + user + " removed")


remove_browsers()
