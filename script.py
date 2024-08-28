import asyncio
import json

from api.bootstrap import BootstrapContainer
from api.config import settings
from api.resources.schemas.about import AboutCreateSchema
from api.resources.schemas.education import EducationCreateSchema
from api.resources.schemas.experience import ExperienceCreateSchema
from api.resources.schemas.user import UserCreateSchema

settings = settings.from_env("default")
bootstrap = BootstrapContainer.from_settings(settings)

paths = [("experiences", bootstrap.experience_service, ExperienceCreateSchema),
         ("education", bootstrap.education_service, EducationCreateSchema),
         ("about", bootstrap.about_service, AboutCreateSchema)]


def get_payload(filepath):
    return json.load(open(f"tests/data/{filepath}.json", encoding='utf-8'))


async def save_user():
    user = UserCreateSchema(**get_payload("user"))
    return await bootstrap.user_service.save(user)


async def async_run(path, service, schema, user):
    payload = get_payload(path)
    for element in payload:
        element["user"] = user.id
        await service.save(schema(**element))


print("Starting script...\n")

loop = asyncio.get_event_loop()
user = loop.run_until_complete(save_user())
print(f"USER ID: {user.id}\n")

for path, service, schema in paths:
    loop.run_until_complete(async_run(path, service, schema, user))
loop.close()

print("Script finished!")
