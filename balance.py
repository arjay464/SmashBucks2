import configparser

config = configparser.ConfigParser()
BalanceFilePath = "/home/pendleton/PycharmProjects/SmashBucks2/.venv/files/balance.ini"


async def initUserBalance(username: str) -> None:
    config.read(BalanceFilePath)
    config['Balance'][username] = "100"
    with open(BalanceFilePath, "w") as configfile:
        config.write(configfile)


async def addBalance(username: str, balance: int, name: str) -> str:
    if name == 'arjay_tg' or name == '_camden':
        config.read(BalanceFilePath)
        users = []
        for key, value in config.items('Balance'):
            users.append(key)
        if username in users:
            current_balance = config.getint("Balance", username)
            new_balance = current_balance + balance
            config['Balance'][username] = str(new_balance)
            with open(BalanceFilePath, 'w') as configfile:
                config.write(configfile)
            return "Gave "+str(username)+" "+str(balance)+"\nBalance: "+str(current_balance)+" -> "+str(new_balance)
        else:
            print(str(username))
            return "User: "+str(username)+" not found"
    else:
        return "Access Denied"


async def subBalance(username: str, balance: int, name: str) -> str:
    if name == 'arjay_tg' or name == '_camden':
        config.read(BalanceFilePath)
        users = []
        for key, value in config.items('Balance'):
            users.append(key)
        if username in users:
            current_balance = config.getint("Balance", username)
            new_balance = current_balance - balance
            config['Balance'][username] = str(new_balance)
            with open(BalanceFilePath, 'w') as configfile:
                config.write(configfile)
            return "Revoked " + str(balance) + " from " + str(username) + "\nBalance: " + str(current_balance) + " -> " + str(
                new_balance)
        else:
            print(str(username))
            return "User: " + str(username) + " not found"
    else:
        return "Access Denied"


async def botSubBalance(username: str, balance: int) -> str:
    config.read(BalanceFilePath)
    users = []
    for key, value in config.items('Balance'):
        users.append(key)
    if username in users:
        current_balance = config.getint("Balance", username)
        new_balance = current_balance - balance
        config['Balance'][username] = str(new_balance)
        with open(BalanceFilePath, 'w') as configfile:
            config.write(configfile)
        return "Revoked " + str(balance) + " from " + str(username) + "\nBalance: " + str(current_balance) + " -> " + str(
            new_balance)
    else:
        print(str(username))
        return "User: " + str(username) + " not found"


async def botAddBalance(username: str, balance: int) -> str:
    config.read(BalanceFilePath)
    users = []
    for key, value in config.items('Balance'):
        users.append(key)
    if username in users:
        current_balance = config.getint("Balance", username)
        new_balance = current_balance + balance
        config['Balance'][username] = str(new_balance)
        with open(BalanceFilePath, 'w') as configfile:
            config.write(configfile)
        return "Gave "+str(username)+" "+str(balance)+"\nBalance: "+str(current_balance)+" -> "+str(new_balance)
    else:
        print(str(username))
        return "User: "+str(username)+" not found"


async def getBalance(username: str) -> str:
    config.read(BalanceFilePath)
    for key, value in config.items("Balance"):
        if key == username:
            return "You have "+str(value)+" SmashBucks."


async def userBalance(username: str) -> int:
    config.read(BalanceFilePath)
    for key, value in config.items("Balance"):
        if key == username:
            return int(value)


async def getIntBalance(username: str) -> int:
    config.read(BalanceFilePath)
    for key, value in config.items("Balance"):
        if key == username:
            return value

