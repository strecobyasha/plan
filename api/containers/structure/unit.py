from dependency_injector import containers, providers

from api.services.structure.unit import UnitService


class ServiceContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['...endpoints.v1.structure.unit'])
    service = providers.Factory(UnitService)
