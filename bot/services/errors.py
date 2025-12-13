from aiogram.types import CallbackQuery, Message


class BackendError(Exception):
    """Базовая ошибка общения с backend-сервисом."""


class BackendUnavailable(BackendError):
    """Нет соединения / таймаут / DNS / backend упал."""


class BackendBadResponse(BackendError):
    """Backend вернул неожиданный ответ (невалидный JSON, странный формат)."""


class BackendHTTPError(BackendError):
    def __init__(self, status_code: int, detail: str | None = None):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {detail}")


class NotFound(BackendHTTPError):
    pass


class Conflict(BackendHTTPError):
    pass


class ValidationError(BackendHTTPError):
    pass


def format_backend_error(e: Exception) -> str:
    if isinstance(e, BackendUnavailable):
        return "🚧 Сервис привычек сейчас недоступен. Попробуй ещё раз через минуту."
    if isinstance(e, NotFound):
        return "🔎 Не нашёл такую привычку. Возможно, она была удалена."
    if isinstance(e, Conflict):
        return "⚠️ Сейчас это действие нельзя выполнить (конфликт состояния)."
    if isinstance(e, ValidationError):
        return "📝 Данные не прошли проверку. Проверь ввод и попробуй снова."
    if isinstance(e, BackendHTTPError):
        return "🚨 Ошибка сервиса привычек. Попробуй позже."
    return "😕 Что-то пошло не так. Попробуй позже."


async def reply_error(event: Message | CallbackQuery, text: str):
    if isinstance(event, CallbackQuery):
        await event.message.answer(text)
        await event.answer()
    else:
        await event.answer(text)
