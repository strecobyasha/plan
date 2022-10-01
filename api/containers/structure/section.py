from dependency_injector import containers, providers

from api.services.structure.section import SectionService


class ServiceContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['...endpoints.v1.structure.section'])
    service = providers.Factory(SectionService)
