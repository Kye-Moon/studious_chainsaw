from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel


class ProductHuntMention(BaseModel):
    PK: str  # Primary Key - external system id of the mention
    SK: str  # Sort Key - the source and type of the mention in the format: SOURCE#TYPE
    createAt: str
    body: str
    source: str
    username: str
    userDescription: Optional[str]
    profileImageUrl: Optional[str]
