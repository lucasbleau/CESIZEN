from api.serializers import UtilisateurSerializer
from api.models import Utilisateur


def test_utilisateur_serializer_output():
    u = Utilisateur(username="bob", email="bob@ex.com", role="utilisateur", is_superuser=True)
    serializer = UtilisateurSerializer(u)
    data = serializer.data

    assert data["username"] == "bob"
    assert data["email"] == "bob@ex.com"
    assert data["role"] == "utilisateur"
    assert data["is_superuser"] is True
