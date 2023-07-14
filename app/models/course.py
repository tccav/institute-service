from dataclasses import dataclass


@dataclass
class Course:
    id: str
    name: str
    minimum_periods_qty: int
    maximum_periods_qty: int
