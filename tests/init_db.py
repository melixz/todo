from app.models import Base
from app.database import engine


def create_tables():
    """Создание всех таблиц в базе данных."""
    Base.metadata.create_all(bind=engine)
    print("База данных инициализирована успешно!")


if __name__ == "__main__":
    create_tables()
