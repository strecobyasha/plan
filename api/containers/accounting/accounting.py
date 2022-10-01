from dependency_injector import containers, providers

from api.services.accounting.operations import OperationsAccountingService
from api.services.accounting.parts import PartsAccountingService
from api.services.accounting.units import UnitsAccountingService


class ServiceContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['...endpoints.v1.accounting.accounting'])
    units_acc_service = providers.Factory(UnitsAccountingService)
    parts_acc_service = providers.Factory(PartsAccountingService)
    operations_acc_service = providers.Factory(OperationsAccountingService)
