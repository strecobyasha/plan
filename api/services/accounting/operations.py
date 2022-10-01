import uuid
from datetime import date
from http import HTTPStatus

from api.errors.accounting.accounting import AccountingErrors
from api.maps.accounting.accounting import OperationCompletingMap
from api.models.accounting_models import OperationsHistory
from api.models.associations import OperationProduct
from api.models.base import db
from api.models.models import Operation, Product
from api.utils.system import json_abort


class OperationsAccountingService:
    error = AccountingErrors
    main_model = Operation
    history_model = OperationsHistory
    balance_model = OperationProduct
    map = OperationCompletingMap

    def record(self, operation_id: uuid, product_id: uuid, completion_date: date) -> None:
        # Accounting for the completing of operations.
        operation = self.main_model.query.get(operation_id)
        if not operation:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, self.error.NOT_EXISTS)
        if not Product.query.get(product_id):
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, self.error.PRODUCT_NOT_EXISTS)

        map_data = self.map(**{
            'operation_id': operation_id,
            'product_id': product_id,
            'completion_date': completion_date,
        })
        element = self.history_model(**map_data.dict())
        element.insert_and_commit()

    def change_balance(self, operation_id: uuid, product_id: uuid) -> dict:
        # Operations balance changing.
        oper_prod = self.balance_model.query.filter_by(
            operation_id=operation_id,
            product_id=product_id,
        ).first()

        if oper_prod.is_completed:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, self.error.ALREADY_COMPLETED)

        oper_prod.is_completed = True

        db.session.commit()

        return {
            'section_id': oper_prod.operation.section_id,
            'parts': oper_prod.operation.parts,
            'units': oper_prod.operation.units,
        }
