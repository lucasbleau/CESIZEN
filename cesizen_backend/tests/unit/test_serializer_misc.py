from api.serializers import MessageResponseSerializer, ErrorResponseSerializer


def test_message_response_serializer():
    serializer = MessageResponseSerializer(data={"detail": "All good!"})
    assert serializer.is_valid()
    assert serializer.validated_data["detail"] == "All good!"


def test_error_response_serializer():
    serializer = ErrorResponseSerializer(data={"error": "Something went wrong."})
    assert serializer.is_valid()
    assert serializer.validated_data["error"] == "Something went wrong."
