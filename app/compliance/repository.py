
from typing import List
from app.compliance.models import Compliance
from app.utils.data_manager import load_json


class ComplianceRepository:
    def __init__(self, data_file='compliance.json'):
        self.data_file = data_file
        self.compliance_records = self._load_compliance()

    def _load_compliance(self) -> List[Compliance]:
        compliance_data_list = load_json(self.data_file)
        compliance_records = []
        for compliance_data in compliance_data_list:
            compliance = Compliance(
                regulation=compliance_data.get('regulation'),
                status=compliance_data.get('status'),
                last_checked=compliance_data.get('last_checked')
            )
            compliance_records.append(compliance)
        return compliance_records

    def get_all(self) -> List[Compliance]:
        return self.compliance_records

    def get_by_regulation(self, regulation_name: str):
        for record in self.compliance_records:
            if record.regulation == regulation_name:
                return record
        return None