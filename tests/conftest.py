import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Use a separate SQLite database for testing
# SQLite is a lightweight database that lives in a single file
# Perfect for tests - no setup needed, easy to delete
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    # Create all tables before each test
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after each test
    # This ensures every test starts with a clean empty database
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def override_db(setup_database):
    # Override the get_db dependency to use test database instead of real database
    def get_test_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_test_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client(override_db):
    return TestClient(app)