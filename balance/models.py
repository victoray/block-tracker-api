from typing import Optional

from common.models import Ownable


class Balance(Ownable):
    amount: float = 0
    change: float = 0
    change1h: float = 0
    change24h: float = 0
    change1w: float = 0
    change1m: float = 0
    change1y: float = 0
    assetId: Optional[str]
