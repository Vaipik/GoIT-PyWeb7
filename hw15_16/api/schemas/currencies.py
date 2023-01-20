from typing import Union

from pydantic import BaseModel


class Currency(BaseModel):

    bank: str
    currency: str
    rate_sell: float
    rate_buy: float
    timestamp: Union[str, None]
