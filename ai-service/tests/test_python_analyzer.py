from analyzers.python_analyzer import PythonAnalyzer


def test_extracts_python_classes_methods_and_functions():
    source = """
class AuthService:
    def authenticate(self, token):
        return token


def validate_token(token):
    return True
""".strip()

    analyzer = PythonAnalyzer()

    facts = analyzer.analyze(
        filename="src/auth.py",
        source_code=source,
    )

    assert facts.parse_status == "success"

    assert len(facts.classes) == 1
    assert facts.classes[0].name == "AuthService"

    assert len(facts.methods) == 1
    assert facts.methods[0].class_name == "AuthService"
    assert facts.methods[0].method_name == "authenticate"

    assert len(facts.functions) == 1
    assert facts.functions[0].name == "validate_token"

def test_extracts_python_imports():
    source = """
import os
import requests
from fastapi import FastAPI
from sqlalchemy.orm import Session
""".strip()

    analyzer = PythonAnalyzer()

    facts = analyzer.analyze(
        filename="src/app.py",
        source_code=source,
    )

    assert facts.parse_status == "success"

    assert len(facts.imports) == 4

    packages = [item.package for item in facts.imports]

    assert "os" in packages
    assert "requests" in packages
    assert "fastapi" in packages
    assert "sqlalchemy" in packages

def test_extracts_relative_python_imports():
    source = """
from .utils import helper
from ..models import User
""".strip()

    analyzer = PythonAnalyzer()

    facts = analyzer.analyze(
        filename="src/auth/service.py",
        source_code=source,
    )

    assert facts.parse_status == "success"
    assert len(facts.imports) == 2

    statements = [item.statement for item in facts.imports]
    packages = [item.package for item in facts.imports]

    assert "from .utils import helper" in statements
    assert "from ..models import User" in statements

    assert ".utils" in packages
    assert "..models" in packages

def test_handles_python_parse_error():
    source = """
def broken_function(
    return True
""".strip()

    analyzer = PythonAnalyzer()

    facts = analyzer.analyze(
        filename="src/broken.py",
        source_code=source,
    )

    assert facts.parse_status == "parse_error"
    assert facts.parse_error is not None
    assert facts.classes == []
    assert facts.methods == []
    assert facts.functions == []

def test_handles_empty_python_file():
    analyzer = PythonAnalyzer()

    facts = analyzer.analyze(
        filename="empty.py",
        source_code="",
    )

    assert facts.parse_status == "success"
    assert facts.line_count == 0
    assert facts.file_size_bytes == 0
    assert facts.classes == []
    assert facts.methods == []
    assert facts.functions == []
    assert facts.imports == []

def test_extracts_fastapi_endpoint():
    source = """
from fastapi import FastAPI

app = FastAPI()


@app.get("/users")
def get_users():
    return {"users": []}
""".strip()

    analyzer = PythonAnalyzer()

    facts = analyzer.analyze(
        filename="src/api.py",
        source_code=source,
    )

    assert facts.parse_status == "success"
    assert len(facts.api_endpoints) == 1

    endpoint = facts.api_endpoints[0]

    assert endpoint.method == "GET"
    assert endpoint.path == "/users"
    assert endpoint.handler_name == "get_users"


def test_extracts_multiple_fastapi_endpoints():
    source = """
from fastapi import FastAPI

app = FastAPI()


@app.get("/users")
def get_users():
    return {"users": []}


@app.post("/users")
def create_user():
    return {"created": True}


@app.put("/users/{user_id}")
def update_user(user_id: int):
    return {"updated": user_id}


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    return {"deleted": user_id}
""".strip()

    analyzer = PythonAnalyzer()

    facts = analyzer.analyze(
        filename="src/api.py",
        source_code=source,
    )

    assert facts.parse_status == "success"
    assert len(facts.api_endpoints) == 4

    endpoints = {
        (endpoint.method, endpoint.path, endpoint.handler_name)
        for endpoint in facts.api_endpoints
    }

    assert ("GET", "/users", "get_users") in endpoints
    assert ("POST", "/users", "create_user") in endpoints
    assert ("PUT", "/users/{user_id}", "update_user") in endpoints
    assert ("DELETE", "/users/{user_id}", "delete_user") in endpoints


def test_extracts_router_and_async_fastapi_endpoints():
    source = """
from fastapi import APIRouter

router = APIRouter()


@router.get("/users")
async def get_users():
    return {"users": []}


@router.post("/users")
async def create_user():
    return {"created": True}
""".strip()

    analyzer = PythonAnalyzer()

    facts = analyzer.analyze(
        filename="src/routes.py",
        source_code=source,
    )

    assert facts.parse_status == "success"
    assert len(facts.api_endpoints) == 2

    endpoints = {
        (endpoint.method, endpoint.path, endpoint.handler_name)
        for endpoint in facts.api_endpoints
    }

    assert ("GET", "/users", "get_users") in endpoints
    assert ("POST", "/users", "create_user") in endpoints



def test_extracts_fastapi_endpoint_line_range():
    source = """
from fastapi import FastAPI

app = FastAPI()


@app.get("/users")
def get_users():
    return {"users": []}
""".strip()

    analyzer = PythonAnalyzer()

    facts = analyzer.analyze(
        filename="src/api.py",
        source_code=source,
    )

    assert facts.parse_status == "success"
    assert len(facts.api_endpoints) == 1

    endpoint = facts.api_endpoints[0]

    assert endpoint.method == "GET"
    assert endpoint.path == "/users"
    assert endpoint.handler_name == "get_users"

    assert endpoint.line_start == 6
    assert endpoint.line_end == 8