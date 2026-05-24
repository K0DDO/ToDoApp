from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate


class CategoryNotFoundError(Exception):
    pass


class CategoryService:
    """Ключевые операции с категориями, включая бизнес-логику, валидацию и прочее"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = CategoryRepository(db)

    def list_categories(self) -> list[CategoryRead]:
        categories = self.repository.get_all()
        return [CategoryRead.model_validate(category) for category in categories]

    def create_category(self, payload: CategoryCreate) -> CategoryRead:
        category = self.repository.create(name=payload.name)
        self.db.commit()
        return CategoryRead.model_validate(category)

    def update_category(
        self, category_id: str, payload: CategoryUpdate
    ) -> CategoryRead:
        category = self.repository.get_by_id(category_id)
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена",
            )

        if payload.name is not None:
            category.name = payload.name

        self.db.commit()
        return CategoryRead.model_validate(category)

    def delete_category(self, category_id: str) -> None:
        category = self.repository.get_by_id(category_id)
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена",
            )

        self.repository.delete(category)
        self.db.commit()
