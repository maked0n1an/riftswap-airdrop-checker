import asyncio
import sys
import time
from decimal import Decimal
from typing import (
    Any, Coroutine, List
)


from min_lib.models.account_info import AccountInfo
from min_lib.models.checker import Checker
from min_lib.models.writer import Writer
from min_lib.utils.config import ACCOUNT_NAMES, ACCOUNTS
from user_data.settings.settings import IS_ACCOUNT_NAMES
from min_lib.utils.helpers import format_output


def greetings():
    name_label = "========= RiftSwap Airdrop checker for Zora mints ========="
    brand_label = "========== Author: M A K E D 0 N 1 A N =========="
    telegram = "======== https://t.me/crypto_maked0n1an ========"

    print("")
    format_output(name_label)
    format_output(brand_label)
    format_output(telegram)


def end_of_work():
    exit_label = "========= The bot has ended it's work! ========="
    format_output(exit_label)
    sys.exit()


def is_bot_setuped_to_start():
    end_bot = False

    if len(ACCOUNTS) == 0:
        print("Don't imported accounts' addresses in 'accounts.txt'!")
        return end_bot

    return True


def get_accounts():
    accounts: List[AccountInfo] = []

    if IS_ACCOUNT_NAMES:
        for account_id, address in zip(ACCOUNT_NAMES, ACCOUNTS):
            account = AccountInfo(
                account_id=account_id,
                address=address
            )
            accounts.append(account)
    else:
        for account_id, address in enumerate(ACCOUNTS, start=1):
            account = AccountInfo(
                account_id=account_id,
                address=address
            )
            accounts.append(account)

    return accounts


async def run_module(module, account: AccountInfo):
    return await module(account)


def measure_time_for_all_work(start_time: float):
    end_time = round(time.time() - start_time, 2)
    seconds = round(end_time % 60, 2)
    minutes = int(end_time // 60) if end_time > 60 else 0
    hours = int(end_time // 3600) if end_time > 3600 else 0

    print(
        (
            f"Spent time: "
            f"{hours} hours {minutes} minutes {seconds} seconds"
        )
    )


async def main():
    total_tokens: Decimal = 0
    tasks: List[Coroutine[Any, Any, AccountInfo]] = []
    accounts = get_accounts()

    for account in accounts:
        checker = Checker(account)
        tasks.append(checker.check_for_eligibility())

    results = await asyncio.gather(*tasks)

    for account in results:
        writer = Writer(account)

        total_tokens += account.tokens
        await writer.write_to_csv()

    Writer.write_total_result(total_tokens)


if __name__ == '__main__':
    greetings()

    if not is_bot_setuped_to_start():
        exit_label = "========= The bot has ended it's work! ========="
        format_output(exit_label)
        sys.exit()

    start_time = time.time()

    print("The bot has started to measure time for all work")

    asyncio.run(main())

    measure_time_for_all_work(start_time)
    end_of_work()
