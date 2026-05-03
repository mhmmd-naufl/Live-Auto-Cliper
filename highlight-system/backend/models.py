from sqlalchemy import Integer, String, Float, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from database import Base

class Configuration(Base):
    __tablename__ = "configurations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    obs_host: Mapped[str] = mapped_column(String(255), default="127.0.0.1")
    obs_port: Mapped[int] = mapped_column(Integer, default=4455)
    obs_password: Mapped[str] = mapped_column(String(255), default="")
    threshold_db: Mapped[float] = mapped_column(Float, default=-20.0)
    file_path: Mapped[str] = mapped_column(Text, default="")
    persistence_duration: Mapped[float] = mapped_column(Float, default=2.0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

class HighlightLog(Base):
    __tablename__ = "highlight_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    config_id: Mapped[int] = mapped_column(Integer, default=1)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    duration: Mapped[float] = mapped_column(Float, default=0.0)
    trigger_value: Mapped[float] = mapped_column(Float, default=0.0)
    filename: Mapped[str] = mapped_column(String(255), default="")
    status: Mapped[str] = mapped_column(String(50), default="SUCCESS")
    error_message: Mapped[str] = mapped_column(Text, default="")