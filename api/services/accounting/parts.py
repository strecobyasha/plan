import uuid

from api.errors.accounting.accounting import AccountingErrors
from api.maps.accounting.accounting import ItemTransferMap
from api.models.accounting_models import PartsTransferHistory
from api.models.associations import PartSection
from api.models.base import db
from api.models.models import Part
from api.services.accounting.base import BaseAccountingService


class PartsAccountingService(BaseAccountingService):
    error = AccountingErrors
    main_model = Part
    history_model = PartsTransferHistory
    balance_model = PartSection
    map = ItemTransferMap

    def change_balance(self, part_id: uuid, section_id: uuid, quantity: int, role: str) -> None:
        # Parts balance changing.
        part_sec = self.balance_model.query.filter_by(
            part_id=part_id,
            section_id=section_id,
        ).first()

        if role == 'sender':
            part_sec.balance = max(part_sec.balance - quantity, 0)
        else:
            part_sec.balance = part_sec.balance + quantity

        db.session.commit()
