from dependency_injector import containers, providers

from api.services.structure.product import ProductService


class ServiceContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['...endpoints.v1.structure.product'])
    service = providers.Factory(ProductService)
