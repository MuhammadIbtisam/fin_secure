from typing import Optional


class Compliance:
    def __init__(self, regulation: str, status: str, last_checked: Optional[str]):
        self.regulation = regulation
        self.status = status
        self.last_checked = last_checked