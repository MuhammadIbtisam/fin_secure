from typing import Optional, List
from app.compliance.repository import ComplianceRepository
from app.compliance.models import Compliance

class ComplianceService:
    def __init__(self, compliance_repository: ComplianceRepository):
        self.compliance_repository = compliance_repository

    def get_compliance_status(self, regulation_name: str) -> Optional[Compliance]:
        return self.compliance_repository.get_by_regulation(regulation_name)

    def track_regulatory_change(self, regulation_name: str, new_status: str):
        compliance_record = self.compliance_repository.get_by_regulation(regulation_name)
        if compliance_record:
            print(f"AUDIT LOG: Regulation '{regulation_name}' changed from '{compliance_record.status}' to '{new_status}'")
            compliance_record.status = new_status
        else:
            print(f"AUDIT LOG: New regulation '{regulation_name}' with status '{new_status}'")

    def get_all_regulations(self) -> List[Compliance]:
        return self.compliance_repository.get_all()