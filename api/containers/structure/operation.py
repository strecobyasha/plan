from dependency_injector import containers, providers

from api.services.structure.operation import OperationService


class ServiceContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['...endpoints.v1.structure.operation'])
    service = providers.Factory(OperationService)
