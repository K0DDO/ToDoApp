from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import CategoryORM


class CategoryRepository:
    """Ключевые операции с таблицей category в БД"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> Sequence[CategoryORM]:
        """Получить все записи category"""
        return self.db.scalars(select(CategoryORM)).all()

    def get_by_id(self, category_id: str) -> CategoryORM | None:
        """Получить запись category по id"""
        return self.db.get(CategoryORM, category_id)

    def create(self, name: str) -> CategoryORM:
        """Создать запись category"""
        category = CategoryORM(name=name)
        self.db.add(category)
        return category

    def delete(self, category: CategoryORM) -> None:
        """Удалить запись category"""
        self.db.delete(category)
