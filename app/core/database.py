import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Base para os modelos
Base = declarative_base()

# URL do banco de dados SQLite
DATABASE_URL = "sqlite+aiosqlite:///./chatbot.db"


# Modelo de mensagens
class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_phone = Column(String(50), index=True)
    user_message = Column(Text)
    bot_response = Column(Text)
    source = Column(String(50), default="api")  # api, whatsapp, etc
    created_at = Column(DateTime, default=datetime.utcnow)


# Engine do banco
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    future=True
)


# Função para inicializar o banco
async def init_db():
    """Cria as tabelas no banco de dados"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Banco de dados inicializado com sucesso")
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar banco: {e}")


# Função para pegar a sessão
async def get_db():
    """Dependency para injetar a sessão do banco"""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
