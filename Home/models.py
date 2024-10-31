from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from decimal import Decimal


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=500, unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            while Category.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{get_random_string(length=5)}'
            self.slug = slug
        super().save(*args, **kwargs)
    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    banner = models.ImageField(upload_to='Media/Products')  # Primary image for home page
    title = models.TextField()
    descriptions = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    sales_count = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=500, unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            while Product.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{get_random_string(length=5)}'
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    stock = models.PositiveIntegerField(default=0)  # Track the stock of each variant

    def __str__(self):
        return f"{self.product.title} - {self.color}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Media/Products/Images')

    def __str__(self):
        return f"Image for {self.product.title}"

class Blog(models.Model):
    banner = models.ImageField(upload_to='media/blogs', height_field=None, width_field=None, max_length=None, default='0')
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    author = models.CharField(max_length=100)
    categories = models.CharField(max_length=200)
    comments_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

class ProductType(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    full_name = models.CharField(max_length=255)
    cell_number = models.CharField(max_length=15)
    address = models.TextField()
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    shipping = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('100.00'))
    total = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    order_items = models.ManyToManyField('OrderItem', blank=True)

    def __str__(self):
        return f"Order {self.id} by {self.full_name}"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def total_price(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"Quantity {self.quantity} | {self.product}"