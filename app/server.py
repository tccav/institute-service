import json_logging
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from sanic import Sanic, Request
from sanic.response import json, text
from sanic_ext import Extend, openapi
from sanic import exceptions
from mayim.extension import SanicMayimExtension

import telemetry
from models.course import Course
from models.institute import Institute
from models.subject import Subject
from executors import InstituteExecutor
from validator import validate_is_universal_param
from typing import List
import os

resource = Resource(attributes={
    SERVICE_NAME: "institute-service"
})
tracer_provider = TracerProvider(resource=resource)
tracer_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=os.environ['OTEL_BASE_URL'], insecure=True))
tracer_provider.add_span_processor(tracer_processor)
trace.set_tracer_provider(tracer_provider)

app = Sanic("institute-service")
json_logging.init_sanic(enable_json=True)
json_logging.init_request_instrument(app)

app.ctx.db = f"postgres://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:" \
             f"{os.environ['DB_PORT']}/{os.environ['DB_NAME']}?{os.environ['DB_OPTIONS']}"

Extend.register(
    SanicMayimExtension(
        executors=[InstituteExecutor],
        dsn=app.ctx.db
    )
)


@app.get("/healthcheck")
async def healthcheck(_):
    return text("RUNNING")


@app.get("/institutes")
@telemetry.start_as_current_http_span()
@openapi.response(200, List[Institute])
async def get_institutes(_: Request, executor: InstituteExecutor):
    try:
        institutes = await executor.get_institutes()
        return json({"institutes": [institute.__dict__ for institute in institutes]}, ensure_ascii=False, default=str)
    except Exception as e:
        raise exceptions.ServerError(f"{e}")


@app.get("/institutes/<institute_id>/subjects")
@telemetry.start_as_current_http_span()
@openapi.response(200, List[Subject])
async def get_subjects_by_institute_id(request: Request, institute_id: str, executor: InstituteExecutor):
    try:
        is_universal = request.args.get("isUniversal", default="false").lower()
        validate_is_universal_param(is_universal)

        subjects = await executor.get_subjects_by_institute_id(institute_id, is_universal)
        return json({"subjects": [subject.__dict__ for subject in subjects]}, ensure_ascii=False, default=str)
    except ValueError as e:
        raise exceptions.BadRequest(f"{e}")
    except Exception as e:
        raise exceptions.ServerError(f"{e}")


@app.get("/courses/<course_id>/subjects/")
@telemetry.start_as_current_http_span()
@openapi.response(200, List[Subject])
async def get_subjects_by_course_id(_: Request, course_id: str, executor: InstituteExecutor):
    try:
        subjects = await executor.get_subjects_by_course_id(course_id)
        return json({"subjects": [subject.__dict__ for subject in subjects]}, ensure_ascii=False, default=str)
    except Exception as e:
        raise exceptions.ServerError(f"{e}")


@app.get("/courses/<course_id>")
@telemetry.start_as_current_http_span()
@openapi.response(200, Course)
async def get_course_by_id(_: Request, course_id: str, executor: InstituteExecutor):
    try:
        course = await executor.get_course_by_id(course_id)
        return json(course.__dict__, ensure_ascii=False, default=str)
    except Exception as e:
        raise exceptions.ServerError(f"{e}")


@app.get("/subjects/<subject_id>")
@telemetry.start_as_current_http_span()
@openapi.response(200, Subject)
async def get_subject_by_id(_: Request, subject_id: str, executor: InstituteExecutor):
    try:
        subject = await executor.get_subject_by_id(subject_id)
        return json(subject.__dict__, ensure_ascii=False, default=str)
    except Exception as e:
        raise exceptions.ServerError(f"{e}")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ['APP_PORT']), access_log=True)
