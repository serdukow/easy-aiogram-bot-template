import subprocess
import re

required_packages = [
    "environs",
    "structlog",
    "sqlalchemy",
    "orjson",
    "pytz",
    "fastapi",
    "uvicorn",
    "pytest",
    "babel",
    "aiogram",
]


def test_required_packages():
    """
    Check if required packages are installed.
    """
    result = subprocess.run(["poetry", "show"], capture_output=True, text=True)
    installed_packages = result.stdout

    for package in required_packages:
        pattern = rf"^{package}\s"
        assert re.search(pattern, installed_packages, re.MULTILINE), f"Package {package} is not installed!"
