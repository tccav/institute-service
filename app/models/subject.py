from dataclasses import dataclass
from typing import List

@dataclass
class Subject:
    id: int
    name: str
    credits: int
    workload_hours_total: int
    workload_hours_total: int
    is_universal: bool
    permits_agenda_conflict: bool
    permits_preparation_situation: bool
    credits_requirements: int
    approval_type: int
    required_subjects: List[int]
