class AccountInfo:
    def __init__(
        self,
        account_id: str | int,
        address: str,
        proxy: str | None = None,
    ) -> None:
        self.account_id = account_id
        self.address = address.lower()
        self.proxy = proxy
        self.tokens: float | 0 = 0
