from flask import Blueprint, Flask
from flask_migrate import Migrate
from flask_pydantic_spec import FlaskPydanticSpec

from api.containers.accounting.accounting import \
    ServiceContainer as AccountingServiceContainer
from api.containers.planning.schedule import \
    ServiceContainer as ScheduleServiceContainer
from api.containers.structure.operation import \
    ServiceContainer as OperationServiceContainer
from api.containers.structure.part import \
    ServiceContainer as PartServiceContainer
from api.containers.structure.product import \
    ServiceContainer as ProductServiceContainer
from api.containers.structure.section import \
    ServiceContainer as SectionServiceContainer
from api.containers.structure.unit import \
    ServiceContainer as UnitServiceContainer
from core.config import CONFIG, INTERACTION_CONFIG

from .models.base import db

migrate = Migrate()
spec = FlaskPydanticSpec('flask', title='FACTORY API', version=CONFIG.APP.API_VERSION, path=CONFIG.APP.SWAGGER_PATH)


def register_di_containers():
    PartServiceContainer()
    OperationServiceContainer()
    ProductServiceContainer()
    SectionServiceContainer()
    UnitServiceContainer()
    AccountingServiceContainer()
    ScheduleServiceContainer()


def register_blueprints(app):
    root_bp = Blueprint('root', __name__, url_prefix=f'/api/{CONFIG.APP.API_VERSION}')

    from api.endpoints.v1.structure.part import bp as part_bp
    root_bp.register_blueprint(part_bp)

    from api.endpoints.v1.structure.operation import bp as operation_bp
    root_bp.register_blueprint(operation_bp)

    from api.endpoints.v1.structure.product import bp as product_bp
    root_bp.register_blueprint(product_bp)

    from api.endpoints.v1.structure.section import bp as section_bp
    root_bp.register_blueprint(section_bp)

    from api.endpoints.v1.structure.unit import bp as unit_bp
    root_bp.register_blueprint(unit_bp)

    from api.endpoints.v1.accounting.accounting import bp as accounting_bp
    root_bp.register_blueprint(accounting_bp)

    from api.endpoints.v1.accounting.db_tables import bp as db_tables_bp
    root_bp.register_blueprint(db_tables_bp)

    from api.endpoints.v1.planning.schedule import bp as schedule_bp
    root_bp.register_blueprint(schedule_bp)

    app.register_blueprint(root_bp)


def create_db_schema(db, schema_name=CONFIG.DB.SCHEMA_NAME):
    db.engine.execute(f'CREATE SCHEMA IF NOT EXISTS {schema_name};')


def create_app(config_classes=[CONFIG, INTERACTION_CONFIG]):
    app = Flask(__name__)
    [app.config.from_object(config_class) for config_class in config_classes]
    db.init_app(app)
    migrate.init_app(app, db)
    register_blueprints(app)
    register_di_containers()
    spec.register(app)
    app.app_context().push()

    create_db_schema(db)

    return app
