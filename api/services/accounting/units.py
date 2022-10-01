import uuid

from api.errors.accounting.accounting import AccountingErrors
from api.maps.accounting.accounting import ItemTransferMap
from api.models.accounting_models import UnitsTransferHistory
from api.models.associations import UnitAssociation, UnitSection
from api.models.base import db
from api.models.models import Unit
from api.services.accounting.base import BaseAccountingService


class UnitsAccountingService(BaseAccountingService):
    error = AccountingErrors
    main_model = Unit
    history_model = UnitsTransferHistory
    balance_model = UnitSection
    map = ItemTransferMap

    def change_balance(self, unit_id: uuid, section_id: uuid, quantity: int, role: str) -> list:
        # Unit balance changing.
        unit_parts = []
        unit_sec = self.balance_model.query.filter_by(
            unit_id=unit_id,
            section_id=section_id,
        ).first()
        if role == 'sender':
            unit_sec.balance = max(unit_sec.balance-quantity, 0)
            if unit_sec.order_num == 1:
                unit_parts = unit_sec.unit.parts
                for unit_child in unit_sec.unit.unit_children:
                    quantity_obj = UnitAssociation.query.filter_by(
                        unit_id=unit_id,
                        child_id=unit_child.id,
                    ).first()
                    self.change_balance(unit_child.id, section_id, -quantity * quantity_obj.quantity, 'producer')
        else:
            unit_sec.balance = unit_sec.balance + quantity

        db.session.commit()

        return unit_parts
