from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys
import logging

# Add the app directory to sys.path so Alembic can find the models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

# Import your Base and models
from app.db.database import Base
from app.db.models import investment
from app.db.models.pricing import PriceCandle


# this is the Alembic Config object, which provides access to values within the .ini file
config = context.config

# Interpret the config file for Python logging
fileConfig(config.config_file_name)

# Set the target metadata for 'autogenerate'
target_metadata = Base.metadata

# Get the database URL from the environment variable or fallback to default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/investment_db")

#print("Using SQLAlchemy URL:", str(config.get_main_option("sqlalchemy.url")))

logging.getLogger(__name__).info("Using SQLAlchemy URL: %s", config.get_main_option("sqlalchemy.url"))



def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        {
            'sqlalchemy.url': DATABASE_URL
        },
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # detect column type changes
        )

        with context.begin_transaction():
            context.run_migrations()

# Main execution
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
