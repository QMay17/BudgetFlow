from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from src.utils.password_utils import hash_password
import uuid

class User(Base):
    __table__name = 'users'

    id = Column(Integer, primary_key = True)
    username = Column(String, unique = True, nullable = False)
    first_name = Column(String, nullable = False)
    last_name = Column(String, nullable = False)
    email = Column(String, unique = True, nullable = False)
    phone_number = Column(String)
    password_hash = Column(String)
    email_verified = Column(Boolean, default = False)
    verification_token = Column(String)

    @classmethod
    def create_user(cls, session, username, first_name, last_name, email, phone_number):
        """Create a new user with email verification token"""
        
        verification_token = str(uuid.uuid4())

        new_user = cls(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone_number = phone_number,
            email_verified = False,
            verification_token = verification_token
        )

        session.add(new_user)
        session.commit()

        return new_user, verification_token

