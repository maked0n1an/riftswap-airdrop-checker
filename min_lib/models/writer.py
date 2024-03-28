import csv
from pathlib import Path

from min_lib.models.account_info import AccountInfo

total_point = 0


class Writer:
    FOLDER_NAME = 'user_data/results'
    FILE_NAME = 'results'

    def __init__(self, account_info: AccountInfo):
        self.account_info = account_info
        self.create_folder()
        self.full_path = Path(self.FOLDER_NAME) / (self.FILE_NAME + '.csv')

    @classmethod
    def create_folder(cls):
        relative_path = Path(cls.FOLDER_NAME)
        relative_path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def write_total_result(total_tokens: int):
        with open(Writer(None).full_path, 'a', newline='') as file:
            writer = csv.writer(file)
            print('==============================')
            print(f"Total tokens: {total_tokens}")
            print('==============================')
            writer.writerow(['total_amount', total_tokens])

    async def write_to_csv(self):
        with open(self.full_path, 'a', newline='') as file:
            writer = csv.writer(file)

            if file.tell() == 0:
                writer.writerow(['account_id', 'address', 'tokens'])

            writer.writerow([
                self.account_info.account_id,
                self.account_info.address,
                self.account_info.tokens
            ])
