import httpx


class HabitServiceClient:

    def __init__(self, base_url) -> None:
        self.client = httpx.AsyncClient(base_url=base_url)

    async def get_habits(self):
        print('Начало отправки')
        r = await self.client.get('')
        print('Реквест отправлен')
        r.raise_for_status()
        return r.json()


habit_client = HabitServiceClient('http://localhost:8000/api/v1/habits')
