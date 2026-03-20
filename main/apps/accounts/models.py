from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email).lower()
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, password, **extra_fields)

    def freelancers(self):
        return self.filter(role="freelancer")

    def clients(self):
        return self.filter(role="client")
    
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("client", "Client"),
        ("freelancer", "Freelancer"),
    ]

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects=UserManager()

    @property
    def is_freelancer(self):
        return self.role == "freelancer"

    @property
    def is_client(self):
        return self.role == "client"

    def verify(self):
        self.is_verified = True
        self.save()

    def __str__(self):
        return f"{self.username} ({self.email})"
    
class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="freelancer_profile")
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    skills = models.CharField(max_length=500, blank=True)
    experience_years = models.PositiveIntegerField(default=0)

    def clean(self):
        if self.user.role != "freelancer":
            raise ValidationError("FreelancerProfile can only be created for users with role='freelancer'.")

    def __str__(self):
        return f"FreelancerProfile — {self.user.username}"


class ClientProfile(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile")
    company_name = models.CharField(max_length=200, blank=True)
    website      = models.URLField(blank=True)

    def clean(self):
        if self.user.role != "client":
            raise ValidationError("ClientProfile can only be created for users with role='client'.")

    def __str__(self):
        return f"ClientProfile — {self.user.username}"