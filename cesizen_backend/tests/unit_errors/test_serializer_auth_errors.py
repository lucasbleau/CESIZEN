import pytest
from api.serializers import ConnexionSerializer, InscriptionSerializer

def test_connexion_serializer_requis():

    ser = ConnexionSerializer(data={"email": "x@y.com"})
    assert not ser.is_valid()
    assert "password" in ser.errors

def test_inscription_serializer_mdp_incohérents():
    """
    Les deux mots de passe doivent correspondre.
    """
    ser = InscriptionSerializer(
        data={
            "email": "z@y.com",
            "username": "z",
            "password1": "abc",
            "password2": "def",
        }
    )
    assert not ser.is_valid()
    assert ser.errors["non_field_errors"]
