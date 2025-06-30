from api.serializers import ConnexionSerializer, InscriptionSerializer


def test_connexion_serializer_valid():
    data = {"email": "test@example.com", "password": "MyPwd123!"}
    serializer = ConnexionSerializer(data=data)
    assert serializer.is_valid()


def test_inscription_serializer_valid():
    data = {
        "email": "test@example.com",
        "username": "newuser",
        "password1": "SecretPwd!",
        "password2": "SecretPwd!",
    }
    serializer = InscriptionSerializer(data=data)
    assert serializer.is_valid()
