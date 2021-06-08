import os
from pathlib import Path
from typing import Generator

import pytest
from starlette.testclient import TestClient

from src import app

ROOT_DIR = Path(os.path.dirname(__file__))


@pytest.fixture()
def http_client() -> Generator[TestClient, None, None]:
    client = TestClient(app)
    yield client
