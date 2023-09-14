from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Note:
    _id: str
    title: str
    date: datetime.today()
    content: str