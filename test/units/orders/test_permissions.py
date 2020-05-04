import pytest
from api.orders.permissions import IsRegularUser
from datetime import date, timedelta
from uuid import uuid4

class TestIsRegularUserPermission:

    permission = IsRegularUser()

    @pytest.mark.parametrize('user_type, result', [
        ('regular', True),
        ('super', False)
    ])
    def test_has_permission(self, mocker, regular_user, super_user, user_type, result):
        """
        Should return True if the authenticated user is regular, otherwise, False
        """
        # menu = create_menu(available_date=date)
        user = regular_user if user_type == 'regular' else super_user
        request = mocker.MagicMock(user=user)
        view = mocker.MagicMock()

        assert self.permission.has_permission(request, view) == result
