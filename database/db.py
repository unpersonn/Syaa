from tortoise import Tortoise

TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["database.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}

async def init_db():
    """Initialize the database connection."""
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["database.models"]}
    )
    # In production, use migrations (aerich). For now, generate schema automatically.
    await Tortoise.generate_schemas()

async def close_db():
    """Close the database connection."""
    await Tortoise.close_connections()
