import pytest
from rest_framework.exceptions import ValidationError
from api.orders.v1.serializers import OrderSerializer
from api.orders.models import Order
from uuid import uuid4

order_mock = {
    'additional_notes': 'test',
    'option_id': uuid4(),
}

@pytest.mark.django_db
class TestUserSignUpSerializer:

    def test_valid_incoming_data(self):
        """
        Should return True when the incoming data to be deserialized is valid
        """
        serializer = OrderSerializer(data=order_mock)

        assert serializer.is_valid()

    @pytest.mark.parametrize('input, context', [
        ({**order_mock, 'option_id': '123456'}, 'Invalid incoming data'),
        ({'additional_notes': 'test'}, 'Missing fields')
    ])
    def test_invalid_incoming_data(self, input, context):
        """
        Should raise a ValidationError when the incoming data to be deserialized is invalid
        """

        serializer = OrderSerializer(data=input)

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_valid_serialized(self, create_order):
        """
        Should return the respective serialized object
        """
        order = create_order()
        serializer = OrderSerializer(order)
        compare_attributes = ('id', 'additional_notes',
                              'created_at', 'updated_at', 'option', 'user')

        assert isinstance(serializer.data, dict)

        for prop in compare_attributes:
            # just makes sure that every attribute exist
            assert prop in serializer.data

    def test_create(self, mocker, create_order):
        """
        Should call place_order custom method instead of the predefined one (create)
        """
        order = create_order()
        serializer = OrderSerializer(data=order_mock)

        mocker.patch.object(Order.objects, 'place_order', return_value=order)
        mocker.spy(Order.objects, 'create')

        serializer.is_valid()
        serializer.save()

        Order.objects.place_order.assert_called_once()
        Order.objects.create.assert_not_called()
