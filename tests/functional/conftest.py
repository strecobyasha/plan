import asyncio
from dataclasses import dataclass
from typing import Any, Optional

import aiohttp
import psycopg2
import pytest
from multidict import CIMultiDictProxy
from psycopg2.extras import DictCursor, register_uuid

from .settings import CONFIG
from .utils.data_generators.operation_products import \
    OperationProductsDataGenerator
from .utils.data_generators.operations import OperationsDataGenerator
from .utils.data_generators.part_operations import PartOperationsDataGenerator
from .utils.data_generators.part_sections import PartSectionsDataGenerator
from .utils.data_generators.part_units import PartUnitsDataGenerator
from .utils.data_generators.parts import PartsDataGenerator
from .utils.data_generators.products import ProductsDataGenerator
from .utils.data_generators.sections import SectionsDataGenerator
from .utils.data_generators.unit_operations import UnitOperationsDataGenerator
from .utils.data_generators.unit_sections import UnitSectionsDataGenerator
from .utils.data_generators.unit_units import UnitUnitsDataGenerator
from .utils.data_generators.units import UnitsDataGenerator

SERVICE_URL = f'{CONFIG.API.URL}:{CONFIG.API.PORT}{CONFIG.API.API_PATH}/{CONFIG.API.API_VERSION}/'


@dataclass
class HTTPResponse:
    body: dict[str, Any]
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
async def pg_cursor():
    conn = psycopg2.connect(**CONFIG.DB.dsn(), cursor_factory=DictCursor)
    conn.autocommit = True
    _pg_cursor = conn.cursor()
    register_uuid()
    yield _pg_cursor
    _pg_cursor.close()
    conn.close()


@pytest.fixture(scope='session')
async def session():
    connector = aiohttp.TCPConnector(force_close=True)
    session = aiohttp.ClientSession(connector=connector)
    yield session
    await session.close()


@pytest.fixture
def make_request(session):
    async def inner(
        method: str,
        target: str,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
        json: Optional[dict[list]] = None,
    ) -> HTTPResponse:
        params = params or {}
        headers = headers or {}
        json = json or {}
        url = SERVICE_URL + target
        async with getattr(session, method)(url, json=json, headers=headers, params=params) as response:
            return HTTPResponse(body=await response.json(), headers=response.headers, status=response.status)

    return inner


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def generate_sections(pg_cursor):
    data_generator = SectionsDataGenerator(conn=pg_cursor)
    yield await data_generator.load()
    await data_generator.clean()


@pytest.fixture(scope='session')
async def generate_parts(pg_cursor):
    data_generator = PartsDataGenerator(conn=pg_cursor)
    yield await data_generator.load()
    await data_generator.clean()


@pytest.fixture(scope='session')
async def generate_units(pg_cursor):
    data_generator = UnitsDataGenerator(conn=pg_cursor)
    yield await data_generator.load()
    await data_generator.clean()


@pytest.fixture(scope='session')
async def generate_operations(pg_cursor):
    data_generator = OperationsDataGenerator(conn=pg_cursor)
    yield await data_generator.load()
    await data_generator.clean()


@pytest.fixture(scope='session')
async def generate_products(pg_cursor):
    data_generator = ProductsDataGenerator(conn=pg_cursor)
    yield await data_generator.load()
    await data_generator.clean()


@pytest.fixture(scope='session')
async def generate_part_operations(pg_cursor):
    data_generator = PartOperationsDataGenerator(conn=pg_cursor)
    yield await data_generator.load()
    await data_generator.clean()


@pytest.fixture(scope='session')
async def generate_part_sections(pg_cursor):
    data_generator = PartSectionsDataGenerator(conn=pg_cursor)
    yield await data_generator.load()
    await data_generator.clean()


@pytest.fixture(scope='session')
async def generate_unit_sections(pg_cursor):
    data_generator = UnitSectionsDataGenerator(conn=pg_cursor)
    yield await data_generator.load()
    await data_generator.clean()


@pytest.fixture(scope='session')
async def generate_part_units(pg_cursor):
    data_generator = PartUnitsDataGenerator(conn=pg_cursor)
    yield await data_generator.load()
    await data_generator.clean()


@pytest.fixture(scope='session')
async def generate_unit_units(pg_cursor):
    data_generator = UnitUnitsDataGenerator(conn=pg_cursor)
    yield await data_generator.load()
    await data_generator.clean()


@pytest.fixture(scope='session')
async def generate_unit_operations(pg_cursor):
    data_generator = UnitOperationsDataGenerator(conn=pg_cursor)
    yield await data_generator.load()
    await data_generator.clean()


@pytest.fixture(scope='session')
async def generate_operation_products(pg_cursor):
    data_generator = OperationProductsDataGenerator(conn=pg_cursor)
    yield await data_generator.load()
    await data_generator.clean()
