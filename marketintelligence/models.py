from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:8291/marketintelligence", echo=True)


class Base(DeclarativeBase):
    pass


class SecretsOrm(Base):
    __tablename__ = "secrets"
 
    id: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    secret_data: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str | None] = mapped_column(nullable=False)
    is_viewed: Mapped[bool] 