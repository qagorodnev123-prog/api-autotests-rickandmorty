from pydantic import BaseModel


class NotFoundErrorSchema(BaseModel):
    """
    Модель для описания ошибки
    """
    error: str