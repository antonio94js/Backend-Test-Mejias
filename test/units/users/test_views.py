import pytest
import json
from django.urls import reverse
from api.users.v1.views import UserSignUpViewSet
from api.users.models import User

@pytest.mark.urls('api.users.urls')
@pytest.mark.django_db
class TestUserSignUpViewSet:
    def test_create(self, rf, mocker, user_mock, regular_user):
        """
        Should return status code 201 and call create_user method through serializers
        """
        url = reverse('user-list')
        request = rf.post(url, content_type='application/json', data=json.dumps(user_mock))

        mocker.patch.object(User.objects, 'create_user', return_value=regular_user)
        response = UserSignUpViewSet.as_view({'post': 'create'})(request).render()

        content = json.loads(response.content)

        assert response.status_code == 201
        assert 'id' in content

        User.objects.create_user.assert_called_once()