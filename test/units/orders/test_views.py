import pytest
import json
from django.urls import reverse
from api.orders.v1.views import OrderViewSet
from api.orders.models import Order

@pytest.mark.urls('api.orders.urls')
@pytest.mark.django_db
class TestOrderViewSet:
    def test_create(self, auth_rf, mocker, regular_user, order_mock, create_order):
        """
        Should return status code 201 and call place_order method through serializers
        """
        url = reverse('order-list')
        order = create_order()
        request = auth_rf.post(regular_user, url, order_mock, format='json')

        mocker.patch.object(Order.objects, 'place_order', return_value=order)
        response = OrderViewSet.as_view({'post': 'create'})(request).render()

        content = json.loads(response.content)

        assert response.status_code == 201
        assert 'id' in content

        Order.objects.place_order.assert_called_once()

    def test_list(self, auth_rf, mocker, regular_user, create_order):
        """
        Should return status code 200 and filter the response by the appropriate user
        """
        create_order()
        url = reverse('order-list')
        request = auth_rf.get(regular_user, url, format='json')

        mocker.spy(Order.objects, 'filter')
        response = OrderViewSet.as_view({'get': 'list'})(request).render()

        content = json.loads(response.content)

        Order.objects.filter.assert_called_once_with(user=regular_user)
        assert response.status_code == 200
        assert len(content) == 1