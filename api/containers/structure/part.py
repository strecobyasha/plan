from dependency_injector import containers, providers

from api.services.structure.part import PartService


class ServiceContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['...endpoints.v1.structure.part'])
    service = providers.Factory(PartService)
