import json

from models.igg_account import IGGAccount
from models.igg_id import IGGID
from models.character import Character


class ConfigLoader:

    @staticmethod
    def load_accounts(path="config/accounts.json"):

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        accounts = []

        for account_data in data["accounts"]:

            account = IGGAccount(
                account_data["email"]
            )

            for igg_data in account_data["igg_ids"]:

                igg_id = IGGID(
                    igg_data["id"]
                )

                for character_data in igg_data["characters"]:

                    character = Character(
                        character_data["id"],
                        character_data["nickname"],
                        character_data["enabled"]
                    )

                    igg_id.add_character(
                        character
                    )

                account.add_igg_id(
                    igg_id
                )

            accounts.append(
                account
            )

        return accounts