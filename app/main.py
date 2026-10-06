from datetime import datetime, timezone

from fastapi import Depends, FastAPI
from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import Quote

app = FastAPI(title="Pelican Pricing")


class QuoteIn(BaseModel):
    product: str = Field(min_length=1, max_length=120)
    amount_cents: int = Field(ge=0)
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    expires_at: datetime

    @field_validator("expires_at")
    @classmethod
    def to_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)


class QuoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product: str
    amount_cents: int
    currency: str
    expires_at: datetime
    created_at: datetime

    # SQLite keeps no offset; every timestamp stored is UTC
    @field_serializer("expires_at", "created_at")
    def as_utc(self, value: datetime) -> datetime:
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


@app.get("/health")
def health() -> dict[str, bool]:
    return {"ok": True}


@app.get("/quotes", response_model=list[QuoteOut])
def list_quotes(session: Session = Depends(get_session)) -> list[Quote]:
    return list(session.scalars(select(Quote).order_by(Quote.id)))


@app.post("/quotes", response_model=QuoteOut, status_code=201)
def create_quote(payload: QuoteIn, session: Session = Depends(get_session)) -> Quote:
    quote = Quote(**payload.model_dump())
    session.add(quote)
    session.commit()
    session.refresh(quote)
    return quote
