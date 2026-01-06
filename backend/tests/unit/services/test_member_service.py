import pytest
from unittest.mock import MagicMock
from backend.services.member_service import MemberService
from backend.core.database import MemberModel
from backend.core.exceptions import ValidationError, ConflictError, EntityNotFoundError
from backend.core.messages import ErrorMessages
from backend.core.constants import Limits

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def member_service(mock_session):
    return MemberService(mock_session)

def test_create_member_success(member_service, mock_session):
    # Mock repo.get_by_email to return None (no existing member)
    member_service.repo.get_by_email = MagicMock(return_value=None)
    
    member = member_service.create_member(name="John Doe", email="john@example.com")
    
    assert member.name == "John Doe"
    assert member.email == "john@example.com"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

def test_create_member_invalid_name(member_service):
    with pytest.raises(ValidationError) as exc:
        member_service.create_member(name="", email="test@example.com")
    assert str(exc.value) == ErrorMessages.MEMBER_NAME_REQUIRED

def test_create_member_name_too_long(member_service):
    long_name = "a" * (Limits.MEMBER_NAME_MAX + 1)
    with pytest.raises(ValidationError) as exc:
        member_service.create_member(name=long_name, email="test@example.com")
    expected_msg = ErrorMessages.MEMBER_NAME_TOO_LONG.format(max=Limits.MEMBER_NAME_MAX)
    assert str(exc.value) == expected_msg

def test_create_member_invalid_email(member_service):
    with pytest.raises(ValidationError) as exc:
        member_service.create_member(name="John", email="invalid-email")
    assert str(exc.value) == ErrorMessages.MEMBER_EMAIL_INVALID

def test_create_member_conflict(member_service):
    existing_member = MemberModel(name="Existing", email="john@example.com")
    member_service.repo.get_by_email = MagicMock(return_value=existing_member)
    
    with pytest.raises(ConflictError) as exc:
        member_service.create_member(name="John Doe", email="john@example.com")
    assert str(exc.value) == ErrorMessages.MEMBER_EMAIL_EXISTS

def test_list_members(member_service):
    mock_items = [MemberModel(name="M1", email="m1@ex.com"), MemberModel(name="M2", email="m2@ex.com")]
    member_service.repo.paginated_list = MagicMock(return_value=(mock_items, 2))
    
    result = member_service.list_members(page=1, limit=10)
    
    assert len(result['members']) == 2
    assert result['total_count'] == 2
    assert result['total_pages'] == 1

def test_update_member_success(member_service, mock_session):
    existing_member = MemberModel(id="1", name="Old Name", email="old@ex.com")
    member_service.repo.get_by_id = MagicMock(return_value=existing_member)
    member_service.repo.get_by_email = MagicMock(return_value=None)
    
    updated = member_service.update_member("1", name="New Name", email="new@ex.com")
    
    assert updated.name == "New Name"
    assert updated.email == "new@ex.com"
    mock_session.commit.assert_called_once()

def test_update_member_not_found(member_service):
    member_service.repo.get_by_id = MagicMock(return_value=None)
    
    with pytest.raises(EntityNotFoundError) as exc:
        member_service.update_member("999", name="New Name")
    assert str(exc.value) == ErrorMessages.MEMBER_NOT_FOUND

def test_update_member_email_conflict(member_service):
    existing_member = MemberModel(id="1", name="M1", email="m1@ex.com")
    other_member = MemberModel(id="2", name="M2", email="m2@ex.com")
    
    member_service.repo.get_by_id = MagicMock(return_value=existing_member)
    member_service.repo.get_by_email = MagicMock(return_value=other_member)
    
    with pytest.raises(ConflictError) as exc:
        member_service.update_member("1", email="m2@ex.com")
    assert str(exc.value) == ErrorMessages.MEMBER_EMAIL_EXISTS
