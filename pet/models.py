from django.conf import settings
from django.db import models
from cloudinary.models import CloudinaryField
from pet.validators import validate_file_size


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.TextField()
    breed = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="pet")
    availability_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

    def mark_available(self):
        """Sets the pet's status to available."""
        if not self.availability_status:
            self.availability_status = True
            self.save()

    def mark_unavailable(self):
        """Sets the pet's status to unavailable."""
        if self.availability_status:
            self.availability_status = False
            self.save()


class PetImage(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField('image', validators=[validate_file_size])

    def __str__(self):
        return f"Image for {self.pet.name}"


class Review(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comments = models.TextField()
    date = models.DateField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["pet", "user"], name="unique_pet_user_review"
            )
        ]

    def __str__(self):
        return f"Review by {self.user.email} for {self.pet.name}"
