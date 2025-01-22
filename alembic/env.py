import asyncio
import re
from logging.config import fileConfig
from pathlib import Path
from typing import Iterable

from alembic.operations import MigrationScript
from alembic.runtime.migration import MigrationContext
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from src.bot.models.base import Base
from src.bot.utils.postgres_settings import get_pg_settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", get_pg_settings().async_url)
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


# noinspection PyUnusedLocal
def process_revision_directives(
    context: MigrationContext,
    revision: str | Iterable[str | None] | None,
    directives: list[MigrationScript]
) -> None:
    script_directory = context.script
    head_revision_id = script_directory.get_current_head()
    revision_num = 1

    if head_revision_id:
        head_revision_obj = script_directory.get_revision(head_revision_id)
        head_revision_prefix, head_revision_name = (
            Path(head_revision_obj.path).name.split('_', 1)
        )
        head_revision_num = re.findall(r"^(\d+)", head_revision_prefix)
        head_revision_num = (
            int(head_revision_num[0]) if head_revision_num else 0
        )
        revision_num = head_revision_num + 1

    revision_num_str = f"{revision_num:03}"

    slug_arg = context.config.cmd_opts.message
    slug = re.sub(r'\W+', '_', slug_arg) if slug_arg else revision

    file_template = f"{revision_num_str}_{slug}"

    script_directory.file_template = file_template


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        process_revision_directives=process_revision_directives
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        process_revision_directives=process_revision_directives
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
