from mayim import PostgresExecutor, query
from models.institute import Institute
from models.subject import Subject
from typing import List

class InstituteExecutor(PostgresExecutor):

    @query("SELECT id, name FROM faculties")
    async def get_institutes(self) -> List[Institute]:
        ...
    
    @query("""
    WITH required_subjects AS (
    SELECT subject_id, ARRAY_AGG(depends_on_subject_id) as required_subjects
    FROM requirements_subjects as rs
    LEFT JOIN subjects as s
    ON s.id = rs.subject_id
    GROUP BY subject_id
    )
    SELECT id, name, credits, workload_hours_total, workload_hours_total, is_universal, permits_agenda_conflict,
        permits_preparation_situation, credits_requirements, approval_type, required_subjects
    FROM subjects as s
    LEFT JOIN courses_subjects as cs
    ON s.id = cs.subject_id
    LEFT JOIN required_subjects as rs
    ON s.id = rs.subject_id
    WHERE cs.course_id = $course_id
    """)
    async def get_subjects_by_course_id(self, course_id) -> List[Subject]:
        ...