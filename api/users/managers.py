from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, **extra_fields):
        """
        Create and save a Normal User with the given email and password. (The ones who can place orders)
        """
        if not email or not first_name or not last_name:
            raise ValueError('You are missing some required fields.')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        """
        Create and save a super user with the given email and password (This will be the Nora's User).
        """
        super_user_fields = {
            **extra_fields,
            'is_staff': True,
            'is_superuser': True,
        }

        return self.create_user(email, first_name, last_name, password, **super_user_fields)
