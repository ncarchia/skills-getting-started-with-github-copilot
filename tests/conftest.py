import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as _activities


@pytest.fixture
def client():
    """FastAPI test client for making requests against the app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    """ 
    Save a deep copy of the original activities dictionary, yield control
    to the test, and restore the dictionary afterwards.

    This ensures each test starts with a fresh, known state.
    """
    original = copy.deepcopy(_activities)
    yield
    _activities.clear()
    _activities.update(original)
