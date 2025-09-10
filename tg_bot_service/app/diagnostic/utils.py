from app.db.db_helper import get_async_session
from app.user.repositories import UserRepository


async def get_user_id_by_tg_id(
    user_tg_id,
) -> int:
    async with get_async_session() as session:
        user_repo = UserRepository(session)
    user = await user_repo.get_or_create(user_tg_id)
    user_id = user.id
    return user_id
