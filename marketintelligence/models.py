from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import insert, select, update
engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:8291/marketintelligence", echo=True)

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class Base(DeclarativeBase):
    pass

class SecretsOrm(Base):
    __tablename__ = "secrets"
 
    id: Mapped[str] = mapped_column(primary_key=True)
    secret_data: Mapped[str] = mapped_column()
    password: Mapped[str | None] = mapped_column()
    is_viewed: Mapped[bool] 


async def reveal_secret_data(
        sess: AsyncSession,
        secret_id: str,
        hashed_password: str | None,
) -> str:
    query = select(SecretsOrm).filter_by(id=secret_id, is_viewed=False).with_for_update()
    result = await sess.execute(query)
    record = result.scalar_one_or_none()
    if record is None:
        raise ValueError("Secret not found or already viewed")
    update_viewed_status_stmt = update(SecretsOrm).filter_by(id=secret_id).values(is_viewed=True)
    await sess.execute(update_viewed_status_stmt)
    await sess.commit()

    return record.secret_data



async def add_secret_record(
        sess: AsyncSession,
        secret_id: str,
        secret_data: str,
        hashed_password: str | None,
):
    stmt = insert(SecretsOrm).values(
        id=secret_id,
        secret_data=secret_data,
        password=hashed_password,
        is_viewed=False
    )
    await sess.execute(stmt)
    await sess.commit()