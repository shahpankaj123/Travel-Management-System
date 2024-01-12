from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, name, ph, password=None, password2=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            ph=ph
        )

        if password != password2:
            raise ValueError("Passwords donot match")
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, ph, password=None,**extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth, and password.
        """
        
        user = self.create_user(
            email=email,
            password=password,
            name=name,
            ph=ph,
        )
        user.is_superuser=True
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    tc = models.IntegerField(default=0)
    ph = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    is_customer_user = models.BooleanField(default=False)
    is_merchant = models.BooleanField(default=False)
    is_staff_member = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name', 'ph']

    def __str__(self):
        return self.email
    
    '''def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True'''
    
    '''def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True'''

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        if self.is_admin:
          return self.is_admin
        elif self.is_staff_member:
            return self.is_staff_member
        else:
            return self.is_merchant




