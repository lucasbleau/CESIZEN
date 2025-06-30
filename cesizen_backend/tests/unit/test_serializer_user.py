import pytest
from django.contrib.auth import get_user_model
from api.serializers import UserSerializer

User = get_user_model()

@pytest.mark.django_db
def test_user_serializer_data():
    user = User.objects.create_user(
        username="alice",
        email="a@a.com",
        password="test123",
        first_name="Alice",
        last_name="Doe"
    )
    serializer = UserSerializer(user)
    data = serializer.data

    assert data["username"] == "alice"
    assert data["email"] == "a@a.com"
    assert data["first_name"] == "Alice"
    assert data["last_name"] == "Doe"
