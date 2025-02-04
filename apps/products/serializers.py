from rest_framework import serializers
from .models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image",
            "created_date",
            "updated_date",
        ]  # Include fields you want to expose

    def validate(self, attrs):
        # Get the product instance from the context
        product = self.context.get("product")
        if product and product.images.count() >= 5:
            raise serializers.ValidationError(
                "A product can only have a maximum of 5 images."
            )
        return attrs
    
    def validate_image(self, value):
        max_size = 2 * 1024 * 1024  # 2MB in bytes
        if value.size > max_size:
            raise serializers.ValidationError("Image size must be less than 2MB.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)  # Allow multiple images

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "price",
            "description",
            "created_date",
            "updated_date",
            "images",
        ]
    
    def validate(self, attrs):
        request = self.context.get("request")
        product = self.context.get("product")

        if product and product.images.count() >= 5:
            raise serializers.ValidationError("A product can only have up to 5 images.")
        
        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        images_data = request.FILES.getlist("images")  # Get uploaded images

        product = Product.objects.create(**validated_data)  # Create product first
        if len(images_data) > 5:  # Validate image count
            raise serializers.ValidationError({"error": "You can upload up to 5 images only."})

        # Create ProductImage instances
        for image in images_data:
            ProductImage.objects.create(product=product, image=image)

        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop("images", [])  # Extract image data
        instance = super().update(instance, validated_data)  # Update product fields

        if images_data:
            if instance.images.count() + len(images_data) > 5:
                raise serializers.ValidationError(
                    {"error": "You can upload up to 5 images only."}
                )

            for image_data in images_data:
                ProductImage.objects.create(product=instance, **image_data)

        return instance
