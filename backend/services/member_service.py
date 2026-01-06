import re
from sqlalchemy.orm import Session
from backend.core.database import MemberRepository, MemberModel
from backend.core.exceptions import ValidationError, ConflictError, EntityNotFoundError
from backend.core.constants import Limits
from backend.core.messages import ErrorMessages
from backend.core.utils import build_paginated_response

class MemberService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = MemberRepository(session)

    def create_member(self, name: str, email: str) -> MemberModel:
        if not name or not name.strip():
            raise ValidationError(ErrorMessages.MEMBER_NAME_REQUIRED)
        if len(name) > Limits.MEMBER_NAME_MAX:
            raise ValidationError(ErrorMessages.MEMBER_NAME_TOO_LONG.format(max=Limits.MEMBER_NAME_MAX))
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError(ErrorMessages.MEMBER_EMAIL_INVALID)
        # Validation handled by Repository/DB Constraint
        # if self.repo.get_by_email(email): ...
            
        member = MemberModel(name=name, email=email)
        self.repo.add(member)
        self.session.flush()
        self.session.refresh(member)
        return member

    def list_members(self, page: int = 1, limit: int = 10) -> dict:
        items, total_count = self.repo.paginated_list(page, limit)
        return build_paginated_response(items, total_count, limit, "members")

    def update_member(self, member_id: str, name: str = None, email: str = None) -> MemberModel:
        member = self.repo.get_by_id(member_id)
        if not member:
            raise EntityNotFoundError(ErrorMessages.MEMBER_NOT_FOUND)
            
        if name is not None: member.name = name
        if email is not None:
            if email != member.email and self.repo.get_by_email(email):
                raise ConflictError(ErrorMessages.MEMBER_EMAIL_EXISTS)
            member.email = email
            
        self.session.flush()
        self.session.refresh(member)
        return member
