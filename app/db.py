from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


DB_URL = "sqlite+aiosqlite:///app.db"
engine = create_async_engine(DB_URL, echo=True)
NewSession = async_sessionmaker(engine, expire_on_commit=False)
