import json
from typing import List

from transactions.models import Transaction

with open("coinlist.json") as f:
    coin_list: dict = json.load(f)


def get_transaction_objects(docs: List[dict]) -> List[Transaction]:
    transactions = []

    for doc in docs:
        doc["id"] = str(doc.pop("_id"))
        doc["coin"] = coin_list.get("Data", {}).get(doc["assetId"])
        transactions.append(Transaction.parse_obj(doc))

    return transactions
