import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.db.database import Base, get_db
from app.db.models.pricing import PriceCandle
from dotenv import load_dotenv
import os.path
from app.main import app



# 🔥 Use absolute path from project root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dotenv_path = os.path.join(ROOT_DIR, ".env.test")
print(dotenv_path)
load_dotenv(dotenv_path)

# (Optional) Debug
print("Loaded POSTGRES_USER =", os.getenv("POSTGRES_USER"))

# ✅ Now read the vars after loading
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# ✅ Confirm loaded values
print("Loaded DATABASE_URL env values:", POSTGRES_USER, POSTGRES_HOST, POSTGRES_DB)

# Now safely construct the DATABASE_URL
DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Set up SQLAlchemy
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Recreate tables before test session
@pytest.fixture(scope="session", autouse=True)
def set_test_db():
    print("✅ Creating test database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    columns = inspector.get_columns("price_candles")
    print("\n🧩 price_candles table columns:")
    for col in columns:
        print(f" - {col['name']} ({col['type']})")

@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


