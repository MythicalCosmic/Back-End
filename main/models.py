from django.db import models
from django.contrib.auth.models import AbstractUser

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        DeletedProduct.objects.create(
            original_id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            quantity=self.quantity,
            category=self.category,
            photo=self.photo
        )
        super(Product, self).delete(*args, **kwargs)

class DeletedProduct(models.Model):
    original_id = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='deleted_images/')
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    role = models.CharField(max_length=50)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Updated related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'phone_number', 'address', 'role']

    def __str__(self):
        return self.username