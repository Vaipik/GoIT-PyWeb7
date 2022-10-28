from dataclasses import dataclass


@dataclass
class IPAddress:

    address: str
    port: int
    