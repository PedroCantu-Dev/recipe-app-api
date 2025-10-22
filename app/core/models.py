"""
Data base models
"""
from django.db import models  # noqa: F401
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
# Create your models here.

import uuid
from django.core.validators import RegexValidator, MinValueValidator, \
    MaxValueValidator
from django.utils.text import slugify


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class AllTypeFields(models.Model):
    # Campo UUID como clave primaria
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Identificador único universal"
    )  # SQL: UUID PRIMARY KEY

    # Campos de Texto
    title = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Título del registro"
    )  # SQL: VARCHAR(100) UNIQUE

    description = models.TextField(
        null=True,
        blank=True
    )  # SQL: TEXT NULL

    slug = models.SlugField(
        max_length=50,
        unique=True
    )  # SQL: VARCHAR(50) UNIQUE

    email = models.EmailField(
        unique=True
    )  # SQL: VARCHAR(254) UNIQUE

    url = models.URLField(
        max_length=200
    )  # SQL: VARCHAR(200)

    code = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex='^[A-Z]{2}$',
                message='Código debe ser en formato XX-000000'
            )
        ]
    )  # SQL: VARCHAR(10)

    # Campos Numéricos
    integer_num = models.IntegerField(
        default=0
    )  # SQL: INTEGER

    big_number = models.BigIntegerField()  # SQL: BIGINT

    decimal_num = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )  # SQL: DECIMAL(10,2)

    float_num = models.FloatField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )  # SQL: DOUBLE PRECISION

    positive_num = models.PositiveIntegerField()

    small_num = models.SmallIntegerField()  # SQL: SMALLINT

    # Campos Fecha/Hora
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # SQL: TIMESTAMP WITH TIME ZONE

    only_date = models.DateField()  # SQL: DATE

    only_time = models.TimeField()  # SQL: TIME

    duration = models.DurationField()  # SQL: INTERVAL

    # Campos Booleanos
    is_active = models.BooleanField(
        default=True
    )  # SQL: BOOLEAN

    is_optional = models.BooleanField(
        null=True,
        blank=True
    )  # SQL: BOOLEAN NULL

    # Campos Binarios
    binary_data = models.BinaryField(
        null=True,
        blank=True
    )  # SQL: BYTEA NULL

    file = models.FileField(
        upload_to='files/',
        null=True,
        blank=True
    )  # SQL: VARCHAR(100) NULL

    image = models.ImageField(
        upload_to='images/',
        null=True,
        blank=True
    )  # SQL: VARCHAR(100) NULL

    file_path = models.FilePathField(
        path="/path/to/files",
        null=True,
        blank=True
    )  # SQL: VARCHAR(100) NULL

    # Campos Especiales
    ip_address = models.GenericIPAddressField(
        protocol='both',
        unpack_ipv4=True
    )  # SQL: INET

    json_data = models.JSONField(
        default=dict
    )  # SQL: JSONB

    array_field = models.JSONField(
        default=list,
        null=True,
        blank=True
    )  # SQL: JSONB NULL

    mac_address = models.CharField(
        max_length=17,
        validators=[
            RegexValidator(
                regex='^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',
                message='Debe ser una dirección MAC válida'
            )
        ]
    )  # SQL: VARCHAR(17)

    # Campos con Choices
    STATUS_CHOICES = [
        ('AC', 'Active'),
        ('IN', 'Inactive'),
        ('PE', 'Pending')
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='AC'
    )  # SQL: VARCHAR(2)

    # Campos Indexados
    search_vector = models.CharField(
        max_length=255,
        db_index=True
    )  # SQL: VARCHAR(255) WITH INDEX

    hash_field = models.CharField(
        max_length=32,
        unique=True
    )  # SQL: CHAR(32) UNIQUE

    class Meta:
        db_table = 'all_type_fields'
        indexes = [
            models.Index(fields=['title', 'status']),
            models.Index(fields=['created_at']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(positive_num__gte=0),
                name='positive_num_non_negative'
            )
        ]

    def __str__(self):
        return f"{self.title} ({self.code})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
