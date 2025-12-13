from datetime import date
import httpx
from bot.services.errors import (
    BackendUnavailable,
    BackendBadResponse,
    NotFound,
    Conflict,
    ValidationError,
    BackendHTTPError,
)


class HabitServiceClient:

    def __init__(self, base_url) -> None:
        self.client = httpx.AsyncClient(base_url=base_url, timeout=5)

    async def _request(self, method: str, url: str, *, json: dict | None = None):
        try:
            r = await self.client.request(method, url, json=json)
        except httpx.RequestError as e:
            # таймауты, соединение, DNS, connection reset и т.п.
            raise BackendUnavailable() from e

        # Пробуем достать detail (если backend прислал JSON с detail)
        detail = None
        try:
            if r.headers.get("content-type", "").startswith("application/json"):
                payload = r.json()
                if isinstance(payload, dict):
                    detail = payload.get("detail")
        except Exception:
            # если JSON битый — не валим клиента, просто считаем detail неизвестным
            raise BackendBadResponse()

        if 200 <= r.status_code < 300:
            return r

        # Нормализация статусов
        if r.status_code == 404:
            raise NotFound(404, detail)
        if r.status_code in (409,):
            raise Conflict(r.status_code, detail)
        if r.status_code in (400, 422):
            raise ValidationError(r.status_code, detail)

        raise BackendHTTPError(r.status_code, detail)

    async def get_habits(self):
        r = await self._request('GET', 'habits/')
        return r.json()

    async def get_today_habits(self):
        r = await self._request('GET', 'habits/not_complete')
        return r.json()

    async def create_habit(self, data: dict):
        r = await self._request('POST', 'habits/', json=data)
        return r.json()

    async def delete_habit(self, habit_id: int):
        r = await self._request('DELETE', f'habits/{habit_id}')
        return r.json()

    async def edit_habit(self, habit_id: int, data: dict):
        r = await self._request('PATCH', f'habits/{habit_id}', json=data)
        return r.json()

    async def complete_habit(self, habit_id: int):
        day = date.today()
        r = await self._request('POST', f'habits/complete/{habit_id}', json={'date': day.isoformat()})
        return r.json()
