from fastapi import APIRouter

from api.data.mongo import MongoDatabase


async def check_database_status_connection(database: MongoDatabase) -> str:
    """Verify database connection status.

    Returns:
        str: Connection status.

    """
    pong = await database.ping()
    return "UP" if "ok" in pong and pong["ok"] == 1 else "DOWN"


def build_router(mongo_database: MongoDatabase) -> APIRouter:  # noqa: D103
    router = APIRouter()

    @router.get("")
    async def get_health():
        data = await get_health_complete()
        del data["details"]
        return data

    @router.get("/complete")
    async def get_health_complete():
        mongo = await check_database_status_connection(mongo_database)
        return {"status": mongo, "details": {"database": mongo}}

    return router
