from django.db import models
import uuid

#User
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    def __str__(self):
        return self.name


#Category
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


#Food
class Food(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    clorie = models.IntegerField()
    potion = models.IntegerField()
    level = models.IntegerField()
    star_level = models.IntegerField()
    prepare = models.TextField()
    youtube_url = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, null=True)
    def __str__(self):
        return self.name

#UserFavoriteFood
class UserFavoriteFood(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    food = models.ForeignKey(Food, on_delete = models.CASCADE, null=True)
    def __str__(self):
        return self.name

#Review
class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    food = models.ForeignKey(Food, on_delete = models.CASCADE, null=True)
    def __str__(self):
        return self.name


#Ingredient
class Ingredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


#FoodIngredient
class FoodIngredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantity = models.IntegerField()
    food = models.ForeignKey(Food, on_delete = models.CASCADE, null=True)
    ingredient = models.ForeignKey(Ingredient, on_delete = models.CASCADE, null=True)
    def __str__(self):
        return self.name
