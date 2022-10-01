import uuid
from http import HTTPStatus

from api.errors.structure.product import ProductErrors
from api.maps.structure.product import (ProductBriefMap, ProductFullMap,
                                        ProductGetOperationMap,
                                        ProductOperationMap,
                                        ProductSetOperationMap)
from api.models.associations import OperationProduct
from api.models.base import db
from api.models.models import Operation, Product
from api.services.structure.base import BaseService
from api.utils.system import json_abort


class ProductService(BaseService):
    error = ProductErrors
    model = Product
    map = ProductBriefMap

    def get_item(self, id: uuid) -> ProductFullMap:
        product = self.model.query.get(id)
        if not product:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, self.error.NOT_EXISTS)

        return ProductFullMap(
            **product.__dict__,
            **{
                'operations': [
                    ProductGetOperationMap(
                        operation_id=element.operation_id,
                        name=element.operation.name,
                        cycle_time=element.operation.cycle_time,
                        advance=element.operation.advance,
                        is_completed=OperationProduct.query.filter_by(
                            operation_id=element.operation_id,
                            product_id=id,
                        ).first().is_completed,
                    )
                    for element in product.operations
                ],
            }
        )

    def add_operations(self, product_id: uuid, operations: list[ProductSetOperationMap]) -> None:
        # Add operations, that the product contains.
        existing_product_operations = {
            str(item.operation_id): str(item.id)
            for item in OperationProduct.query.filter_by(product_id=product_id)
        }
        for operation in operations:
            map_data = ProductOperationMap(**{'product_id': product_id, **operation.dict()})
            if str(operation.operation_id) in existing_product_operations:
                OperationProduct.query.filter_by(
                    id=existing_product_operations.pop(str(operation.operation_id)),
                ).update(map_data.dict())
                db.session.commit()
            elif not Operation.query.get(operation.operation_id):
                json_abort(
                    HTTPStatus.UNPROCESSABLE_ENTITY, f'{operation.operation_id}: {self.error.OPERATION_NOT_EXISTS}',
                )
            else:
                element = OperationProduct(**map_data.dict())
                element.insert_and_commit()

        delete_query = OperationProduct.__table__.delete().where(
            OperationProduct.id.in_(existing_product_operations.values())
        )
        db.session.execute(delete_query)
        db.session.commit()
