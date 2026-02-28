from fastapi import Depends 
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.db.models import Review
from sqlmodel import select , desc, delete
from src.books.service import BookService
from src.auth.service import UserService
from .schemas import ReviewCreateModel
from src.errors import BookNotFound, UserNotFound, InsufficientPermission
from fastapi import status
import logging

book_service = BookService()
user_service = UserService()

class ReviewService:
    
    async def add_review_to_book(
        self,
        user_email: str,
        book_uid: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ):
        try:
            book = await book_service.get_book(book_uid=book_uid, session=session)
            user = await user_service.get_user_by_email(
                email=user_email, session=session
            )
            review_data_dict = review_data.model_dump()
            if not book:
                raise BookNotFound()

            if not user:
                raise UserNotFound()

            new_review = Review(**review_data_dict, user=user, book=book)

            session.add(new_review)

            await session.commit()

            return new_review

        except Exception as e:
            logging.exception(e)
            raise e
        
    async def get_review(self, review_uid: str, session: AsyncSession):
        statement = select(Review).where(Review.uid == review_uid)

        result = await session.exec(statement)

        return result.first()

    async def get_all_reviews(self, session: AsyncSession):
        statement = select(Review).order_by(desc(Review.created_at))

        result = await session.exec(statement)

        return result.all()

    async def delete_review_to_from_book(
        self, review_uid: str, user_email: str, session: AsyncSession
    ):
        user = await user_service.get_user_by_email(user_email, session)

        review = await self.get_review(review_uid, session)

        if not review or (review.user != user):
            raise InsufficientPermission()

        session.delete(review)

        await session.commit()