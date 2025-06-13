from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os
from app.utils import DATABASE_URL
sys.path.insert( os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models import Base
from app import models

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()