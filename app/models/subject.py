from dataclasses import dataclass
from typing import List

@dataclass
class RequiredSubjects:
    id: int
    name: str

@dataclass
class Subject:
    id: int
    name: str
    credits: int
    workload_hours_total: int
    workload_hours_per_week: int
    is_universal: bool
    permits_agenda_conflict: bool
    permits_preparation_situation: bool
    credits_requirements: int
    approval_type: int
    required_subjects: List[RequiredSubjects]

    def __post_init__(self):
        if self.required_subjects and type(self.required_subjects[0]) == tuple:
            self.required_subjects = [RequiredSubjects(*subject).__dict__ for subject in self.required_subjects]


        