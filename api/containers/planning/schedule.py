from dependency_injector import containers, providers

from api.services.planning.schedule import ScheduleService


class ServiceContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['...endpoints.v1.planning.schedule'])
    service = providers.Factory(ScheduleService)
