from sanic import Sanic, Request
from sanic.response import json, text
from sanic_ext import Extend, openapi
from sanic import exceptions
from mayim.extension import SanicMayimExtension
from models.institute import Institute
from models.subject import Subject
from executors import InstituteExecutor
from typing import List
import os


app = Sanic("institute-service")
app.ctx.db = f"postgres://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}?{os.environ['DB_OPTIONS']}"

Extend.register(
    SanicMayimExtension(
        executors=[InstituteExecutor],
        dsn=app.ctx.db
    )
)

@app.get("/healthcheck")
async def healthcheck(request):
    return text("RUNNING")

@app.get("/institutes")
@openapi.response(List[Institute])
async def get_institutes(request: Request, executor: InstituteExecutor):
    try:
        institutes = await executor.get_institutes()
        return json({"institutes": [institute.__dict__ for institute in institutes]} , ensure_ascii=False, default=str)
    except Exception as e:
        return exceptions.ServerError(f"{e}")

@app.get("/institutes/subjects/<institute_id>")
@openapi.response(List[Subject])
async def get_subjects_by_institute_id(request: Request, institute_id: str,  executor: InstituteExecutor):
    try:
        subjects = await executor.get_subjects_by_institute_id(institute_id)
        return json({"subsjects": [subject.__dict__ for subject in subjects]} , ensure_ascii=False, default=str)
    except Exception as e:
        return exceptions.ServerError(f"{e}")

@app.get("/institutes/universal-subjects/<institute_id>")
@openapi.response(List[Subject])
async def get_universal_subjects_by_institute_id(request: Request, institute_id: str,  executor: InstituteExecutor):
    try:
        subjects = await executor.get__universal_subjects_by_institute_id(institute_id)
        return json({"subsjects": [subject.__dict__ for subject in subjects]} , ensure_ascii=False, default=str)
    except Exception as e:
        return exceptions.ServerError(f"{e}")

@app.get("/course/subjects/<course_id>")
@openapi.response(List[Subject])
async def get_subjects_by_course_id(request: Request, course_id: str,  executor: InstituteExecutor):
    try:
        subjects = await executor.get_subjects_by_course_id(course_id)
        return json({"subsjects": [subject.__dict__ for subject in subjects]} , ensure_ascii=False, default=str)
    except Exception as e:
        return exceptions.ServerError(f"{e}")

@app.get("subject/<subject_id>")
async def get_subject_by_id(request: Request, subject_id: str,  executor: InstituteExecutor):
    try:
        subject = await executor.get_subject_by_id(subject_id)
        return json( subject.__dict__ , ensure_ascii=False, default=str)
    except Exception as e:
        return exceptions.ServerError(f"{e}")
    
if __name__ == '__main__':
    app.run(host="app", port=8000)

