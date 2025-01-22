from fastapi import APIRouter, status
from fastapi_restful.cbv import cbv

from src.bot.models.user import UserOrm
from src.server.schemas.user_schema import UserSchema
from src.server.services.user_service import UserService

router = APIRouter(
    prefix='/api/v1/user',
    tags=['user']
)


@cbv(router)
class UserController:
    def __init__(self):
        self.user_service = UserService()

    @router.post("/create", status_code=status.HTTP_201_CREATED, operation_id="create_user_post")
    async def create_user(self, user: UserSchema) -> UserSchema:
        user_orm: UserOrm = user.to_orm()
        return await self.user_service.create_user(user_orm)

    @router.get("/{user_id}", status_code=status.HTTP_200_OK, operation_id="retrieve_user_get")
    async def get_user(self, user_id: int) -> UserSchema:
        return await self.user_service.get_user(user_id)

    @router.put("/{user_id}", status_code=status.HTTP_200_OK, operation_id="update_user_put")
    async def update_user(self, user_id: int, user: UserSchema) -> UserSchema:
        user_orm: UserOrm = user.to_orm()
        return await self.user_service.update_user(user_id, user_orm)

    @router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, operation_id="delete_user_delete")
    async def delete_order(self, user_id: int):
        await self.user_service.delete_user(user_id)
