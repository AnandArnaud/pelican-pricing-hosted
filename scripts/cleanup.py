"""Delete quotes whose expires_at is in the past."""

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import delete  # noqa: E402

from app.db import SessionLocal  # noqa: E402
from app.models import Quote  # noqa: E402


def main() -> None:
    now = datetime.now(timezone.utc)
    with SessionLocal() as session:
        result = session.execute(delete(Quote).where(Quote.expires_at < now))
        session.commit()
    print(f"removed {result.rowcount} expired quote(s)")


if __name__ == "__main__":
    main()
