from src.bot.models.user import UserOrm
from src.bot.repositories.user import UserRepository


class UserService:
    def __init__(self):
        self.user_repo: UserRepository = UserRepository()

    async def create_user(self, user: UserOrm) -> UserOrm:
        return await self.user_repo.save(user)

    async def get_user(self, user_id: int) -> UserOrm:
        return await self.user_repo.get_by_id(user_id)

    async def update_user(self, user_id: int, updated_user: UserOrm):
        user: UserOrm = await self.user_repo.get_by_id(user_id)
        for field, value in updated_user.dict(exclude_unset=True).items():
            setattr(user, field, value)
        return await self.user_repo.save(user)

    async def delete_user(self, user_id: int):
        return await self.user_repo.delete_by_id(user_id)
