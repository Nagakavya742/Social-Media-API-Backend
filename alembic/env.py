# from logging.config import fileConfig
# from dotenv import load_dotenv
# load_dotenv()

# from sqlalchemy import engine_from_config
# from sqlalchemy import pool

# from alembic import context
# from app.models import Base      #giving access to all those sqlalchemy models
# from app.config import settings    #access to setting object and override all teh table models into it

# # this is the Alembic Config object, which provides
# # access to the values within the .ini file in use.
# config = context.config
# print(
#     settings.database_username,
#     settings.database_password,
#     settings.database_hostname,
#     settings.database_port
# )

# config.set_main_option(
#     "sqlalchemy.url",f'postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}')

# # Interpret the config file for Python logging.
# # This line sets up loggers basically.
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# # add your model's MetaData object here
# # for 'autogenerate' support
# # from myapp import mymodel
# # target_metadata = mymodel.Base.metadata
# target_metadata = Base.metadata

# # other values from the config, defined by the needs of env.py,
# # can be acquired:
# # my_important_option = config.get_main_option("my_important_option")
# # ... etc.


# def run_migrations_offline() -> None:
#     """Run migrations in 'offline' mode.

#     This configures the context with just a URL
#     and not an Engine, though an Engine is acceptable
#     here as well.  By skipping the Engine creation
#     we don't even need a DBAPI to be available.

#     Calls to context.execute() here emit the given string to the
#     script output.

#     """
#     url = config.get_main_option("sqlalchemy.url")
#     context.configure(
#         url=url,
#         target_metadata=target_metadata,
#         literal_binds=True,
#         dialect_opts={"paramstyle": "named"},
#     )

#     with context.begin_transaction():
#         context.run_migrations()


# def run_migrations_online() -> None:
#     """Run migrations in 'online' mode.

#     In this scenario we need to create an Engine
#     and associate a connection with the context.

#     """
#     connectable = engine_from_config(
#         config.get_section(config.config_ini_section, {}),
#         prefix="sqlalchemy.",
#         poolclass=pool.NullPool,
#     )

#     with connectable.connect() as connection:
#         context.configure(
#             connection=connection, target_metadata=target_metadata
#         )

#         with context.begin_transaction():
#             context.run_migrations()


# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     run_migrations_online()


#code from chatgpt that access advanced forms

from logging.config import fileConfig

from dotenv import load_dotenv       #getting .env causes troubles so instead of this dotenv replaces and works well
from sqlalchemy import engine_from_config, pool, create_engine
from sqlalchemy.engine import URL
from alembic import context

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()

from app.config import settings
from app.models import Base

# -------------------------------------------------
# Alembic Config
# -------------------------------------------------
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata
target_metadata = Base.metadata

# -------------------------------------------------
# Database URL (SAFE)
# -------------------------------------------------
database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=settings.database_port,
    database=settings.database_name,
)

# -------------------------------------------------
# Offline migrations
# -------------------------------------------------
def run_migrations_offline() -> None:
    context.configure(
        url=database_url.render_as_string(hide_password=False),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# -------------------------------------------------
# Online migrations (NO configparser involved)
# -------------------------------------------------
def run_migrations_online() -> None:
    connectable = create_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# -------------------------------------------------
# Entry point
# -------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
