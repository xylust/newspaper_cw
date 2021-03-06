from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=10)
    created = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Article(models.Model):
    # The title of the Article
    title = models.CharField(max_length=255)
    # The author of the Article
    author = models.CharField(max_length=255)
    # The headline of the article
    headline = models.TextField(max_length=400)
    # The actual article content
    content = models.TextField()
    # Article image URL
    article_img = models.CharField(max_length=255)
    # Publication date
    pub_date = models.DateTimeField('publication date')
    # The category of the article
    category = models.CharField(max_length=255)
    # Tags
    tags = models.CharField(max_length=255)
    # Likes
    likes = models.IntegerField()
    # Article objects are named by their title

    def __str__(self):
        return self.title


class Comment (models.Model):
    # FK User
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # FK Article
    article = models.ForeignKey('Article')
    # User comment
    content = models.TextField()

    def __str__(self):
        return self.content


class Like(models.Model):
    profile = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    liked_date = models.DateField(auto_now_add=True)
    liked = models.BooleanField()

    def __str__(self):
        return self.liked
