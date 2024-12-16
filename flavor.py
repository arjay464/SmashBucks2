import random

BegRejectionsGeneralFilePath = "/home/pendleton/PycharmProjects/SmashBucks2/.venv/files/beg_rejections_general.txt"
BegRejectionsEliFilePath = "/home/pendleton/PycharmProjects/SmashBucks2/.venv/files/beg_rejections_eli.txt"
BegRejectionsNoahFilePath = "/home/pendleton/PycharmProjects/SmashBucks2/.venv/files/beg_rejections_noah.txt"


async def get_beg_rejections_general() -> str:
    with open(BegRejectionsGeneralFilePath) as f:
        lines = f.readlines()
    r = random.randint(0, len(lines)-1)
    return lines[r]


async def get_beg_rejections_noah() -> str:
    with open(BegRejectionsNoahFilePath) as f:
        lines = f.readlines()
    r = random.randint(0, len(lines)-1)
    return lines[r]


async def get_beg_rejections_eli() -> str:
    with open(BegRejectionsEliFilePath) as f:
        lines = f.readlines()
    r = random.randint(0, len(lines)-1)
    return lines[r]
