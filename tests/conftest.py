import asyncio
from datetime import timedelta
import json
from io import BytesIO

import pytest
import pytest_asyncio
from faker import Faker
from httpx import ASGITransport, AsyncClient
from pydantic.types import PaymentCardBrand
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.api.deps import get_session
from src.app import create_app
from src.config import get_settings
from src.infrastucture.db import Base
from src.models import AreaOfInterest, Project

settings = get_settings()
TEST_DATABASE_NAME = "test_database"
DATABASE_URL = (
    f"postgresql+asyncpg://{settings.database.user}:{settings.database.password}"
    f"@{settings.database.host}:{settings.database.port}/{TEST_DATABASE_NAME}"
)

engine = create_async_engine(DATABASE_URL, echo=False, future=True, poolclass=NullPool)
faker = Faker()


def create_test_database():
    admin_engine = create_engine(
        f"postgresql://{settings.database.user}:{settings.database.password}"
        f"@{settings.database.host}:{settings.database.port}/postgres"
    )

    with admin_engine.connect() as conn:
        conn.execute(text("COMMIT"))
        conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DATABASE_NAME};"))
        conn.execute(text(f"CREATE DATABASE {TEST_DATABASE_NAME}"))


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    create_test_database()


@pytest_asyncio.fixture
async def test_db():
    testing_async_session = async_sessionmaker(engine, expire_on_commit=False)
    session = testing_async_session()
    try:
        await create_tables()
        yield session
        await session.close()
        await drop_tables()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


@pytest.fixture
def app():
    return create_app()


@pytest_asyncio.fixture
async def client(test_db, app):
    app.dependency_overrides[get_session] = lambda: test_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as test_client:
        yield test_client


@pytest.fixture
def geojson():
    return {
        "type": "Feature",
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [
                        [-52.8430645648562, -5.63351005831322],
                        [-52.8289481608136, -5.674529420529012],
                        [-52.8114438198008, -5.6661010219506664],
                        [-52.8430645648562, -5.63351005831322],
                    ]
                ]
            ],
        },
    }


@pytest.fixture
def geojson_file(geojson):
    file_content = json.dumps(geojson).encode("utf-8")
    file = ("geojson.json", BytesIO(file_content), "application/json")
    return file


@pytest.fixture
def create_project(test_db, geojson):
    async def create_project(**kwargs):
        start_date = kwargs.get(
            "start_date", faker.date_between(start_date="-1y", end_date="today")
        )
        end_date = kwargs.get(
            "end_date", start_date + timedelta(days=faker.random_int(min=30, max=365))
        )

        project = Project(
            name=kwargs.get("name", faker.word()),
            description=kwargs.get("description", faker.text(max_nb_chars=200)),
            start_date=start_date,
            end_date=end_date,
        )

        area_of_interest_data = kwargs.get("geojson_data", geojson)

        area_of_interest = AreaOfInterest(
            geojson_data=area_of_interest_data, project_id=project.id
        )

        project.area_of_interest = area_of_interest

        test_db.add(project)
        await test_db.commit()
        return project

    return create_project
