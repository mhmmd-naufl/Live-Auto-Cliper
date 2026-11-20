from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import text

DATABASE_URL = "sqlite+aiosqlite:///./highlight.db"

engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    from models import Configuration, HighlightLog
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Migrasi ringan: tambahkan kolom pre_roll jika belum ada (untuk DB lama)
    try:
        async with engine.begin() as conn:
            await conn.execute(
                text("ALTER TABLE configurations ADD COLUMN pre_roll FLOAT DEFAULT 5.0")
            )
    except Exception:
        pass
    try:
        async with engine.begin() as conn:
            await conn.execute(
                text("ALTER TABLE configurations ADD COLUMN cooldown_seconds FLOAT DEFAULT 8.0")
            )
    except Exception:
        # Kolom sudah ada atau tabel belum siap — abaikan
        pass