from mayim import PostgresExecutor, query

from models.course import Course
from models.institute import Institute
from models.subject import Subject, CourseSubject
from typing import List


class InstituteExecutor(PostgresExecutor):

    @query("SELECT id, name FROM faculties")
    async def get_institutes(self) -> List[Institute]:
        ...

    @query("""
    WITH required_subjects AS (
    SELECT subject_id, ARRAY_AGG((depends_on_subject_id, name)) AS required_subjects
    FROM requirements_subjects AS rs
    LEFT JOIN subjects AS s
    ON s.id = rs.subject_id
    GROUP BY subject_id
    )
    SELECT id, name, credits, workload_hours_total, workload_hours_per_week, is_universal, permits_agenda_conflict,
        permits_preparation_situation, credits_requirements, approval_type, required_subjects, cs.type as type, cs.period as period
    FROM subjects AS s
    LEFT JOIN courses_subjects AS cs
    ON s.id = cs.subject_id
    LEFT JOIN required_subjects AS rs
    ON s.id = rs.subject_id
    WHERE cs.course_id = $course_id
    ORDER BY cs.period ASC, id ASC
    """)
    async def get_subjects_by_course_id(self, course_id) -> List[CourseSubject]:
        ...

    @query("""
    WITH required_subjects AS (
    SELECT subject_id, ARRAY_AGG((depends_on_subject_id, name)) AS required_subjects
    FROM requirements_subjects AS rs
    LEFT JOIN subjects AS s
    ON s.id = rs.subject_id
    GROUP BY subject_id
    ),
    institute_departments AS (
    SELECT id 
    FROM departments
    WHERE faculty_id = $institute_id
    )
    SELECT id, name, credits, workload_hours_total, workload_hours_per_week, is_universal, permits_agenda_conflict,
        permits_preparation_situation, credits_requirements, approval_type, required_subjects
    FROM subjects AS s
    LEFT JOIN required_subjects AS rs
    ON s.id = rs.subject_id
    WHERE s.department_id IN (SELECT * FROM institute_departments)
        AND s.is_universal = $is_universal
    """)
    async def get_subjects_by_institute_id(self, institute_id, is_universal) -> List[Subject]:
        ...

    @query("""
    WITH required_subjects AS (
    SELECT subject_id, ARRAY_AGG((depends_on_subject_id, name)) AS required_subjects
    FROM requirements_subjects AS rs
    LEFT JOIN subjects AS s
    ON s.id = rs.subject_id
    GROUP BY subject_id
    )

    SELECT id, name, credits, workload_hours_total, workload_hours_per_week, is_universal, permits_agenda_conflict,
        permits_preparation_situation, credits_requirements, approval_type, required_subjects
    FROM subjects AS s
    LEFT JOIN required_subjects AS rs
    ON s.id = rs.subject_id
    WHERE s.id = $subject_id
    """)
    async def get_subject_by_id(self, subject_id) -> Subject:
        ...

    @query("SELECT id, name, minimum_periods_qty, maximum_periods_qty FROM courses WHERE id = $course_id")
    async def get_course_by_id(self, course_id) -> Course:
        ...
