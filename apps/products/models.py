import uuid
from django.db import models
from django.core.exceptions import ValidationError
from online_shop.settings import PRODUCTS_MAX_IMAGE_SIZE

def validate_image_size(image):
    print(f"in validate image size, image.size: {image.size}")
    if image.size > PRODUCTS_MAX_IMAGE_SIZE:
        raise ValidationError("Image size must be less than 2MB.")


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def image_count(self):
        return self.images.count()  # 'images' is the related_name in ProductImage

    def clean(self):
        if self.product and self.product.images.count() >= 5:
            raise ValidationError("A product can only have up to 5 images.")



class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to="product_images/",
        blank=True,
        default=None,
        null=True,
        validators=[validate_image_size],  # Add validator here
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.image:
            try:
                validate_image_size(self.image)
            except ValidationError as e:
                raise ValidationError({"image": e.messages})


    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)  # Ensure validation runs before saving
