import json
import aiohttp

from min_lib.models.account_info import AccountInfo
from min_lib.models.token_amount import TokenAmount

total_point = 0


class Checker:
    def __init__(self, account_info: AccountInfo):
        self.account_info = account_info
        self.account_info.address = account_info.address.lower()

    def format_display(self, message):
        print(
            f"{self.account_info.account_id:10} | {self.account_info.address:45} | {message} |"
        )

    async def check_for_eligibility(self) -> AccountInfo:
        url = "https://api-riftswap.online/api/Airdrop/CheckAddress"
        params = {
            'address': self.account_info.address
        }
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en;q=0.9,de-DE;q=0.8,de;q=0.7,ru-RU;q=0.6,ru;q=0.5,en-US;q=0.4',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url=url,
                    params=params,
                    headers=headers,
                    proxy=self.account_info.proxy
                ) as response:
                    if response.status == 200:
                        return await self._get_json(response)
                    else:
                        print(
                            f"{self.account_info.account_id:4} | "
                            f"{self.account_info.address:44} | Failed with status code: {response.status}"
                        )
        except aiohttp.ClientError as e:
            self.format_display(f"An error occured: {e}")

        return self.account_info

    async def _get_json(self, response: aiohttp.ClientSession) -> AccountInfo:
        try:
            drop = await response.json()
            tokens_wei = drop['result']['tokenAmountString']
            tokens = TokenAmount(
                amount=tokens_wei,
                decimals=18,
                wei=True
            )

            self.account_info.tokens = tokens.Ether

            return self.account_info
        except json.JSONDecodeError:
            self.format_display(
                "Cannot unpacked JSON, problem with connection etc.")

            return self.account_info
