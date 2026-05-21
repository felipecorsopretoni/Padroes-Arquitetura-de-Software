from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Customer:
    name: str
    customer_type: str
