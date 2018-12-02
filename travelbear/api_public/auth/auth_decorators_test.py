from cryptography.hazmat.primitives.asymmetric.rsa import generate_private_key
from cryptography.hazmat.backends import default_backend
from django.http import HttpResponse
from django.test import RequestFactory
import jwt
import pytest

from db_layer.user import get_or_create_user
from .auth_decorators import require_jwt_auth


test_private_key = generate_private_key(65537, 2048, default_backend())
test_public_key = test_private_key.public_key()


def make_jwt_token(sub="test-sub", valid=True):
    payload = {"sub": sub}
    algorithm = "RS256"
    if not valid:
        return jwt.encode(
            payload, test_private_key, algorithm=algorithm, headers={"exp": 1000}
        )  # exp in past
    return jwt.encode(payload, test_private_key, algorithm=algorithm)


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def create_user():
    def _create_user(external_id):
        user, _ = get_or_create_user(external_id=external_id)
        return user

    return _create_user


@require_jwt_auth(public_key=test_public_key)
def protected_endpoint(request, expected_user=None):
    assert request.user == expected_user
    return HttpResponse()


@pytest.mark.parametrize(
    "authorization",
    ("", "foo", "Bearer: foo", f"Bearer: {make_jwt_token(valid=False)}"),
)
def test_require_jwt_auth_not_authenticated(request_factory, authorization):
    request = request_factory.get("/", HTTP_AUTHORIZATION=authorization)
    response = protected_endpoint(request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_require_jwt_auth_authenticated(request_factory, create_user):
    user = create_user(external_id="test-sub")
    token = make_jwt_token(sub="test-sub")
    authorization = f"Bearer: {token.decode()}"

    request = request_factory.get("/", HTTP_AUTHORIZATION=authorization)
    result = protected_endpoint(request, expected_user=user)
    assert result.status_code == 200
