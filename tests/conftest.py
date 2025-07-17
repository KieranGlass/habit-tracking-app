import pytest
from databases.create_test_db import TestDatabase

@pytest.fixture
def test_db():
    db = TestDatabase()
    yield db
    db.close()