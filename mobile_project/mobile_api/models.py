from mobile_api.utils import photo_path
from django.db import models


#User
class User(models.Model):
    id = models.AutoField(primary_key=True,
                          null=False,
                          editable=False,
                          unique=True)
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)

    def __str__(self):
        return str(self.full_name)


#Category
class Category(models.Model):
    id = models.AutoField(primary_key=True,
                          null=False,
                          editable=False,
                          unique=True)
    name = models.CharField(max_length=50, null=False, default='')
    image_id = models.CharField(max_length=255, null=False, default='')

    def __str__(self):
        return self.name


class Image(models.Model):
    id = models.AutoField(primary_key=True,
                          null=False,
                          editable=False,
                          unique=True)
    image = models.ImageField(upload_to=photo_path)

    def __str__(self):
        return "ok"


#Food
class Food(models.Model):
    id = models.AutoField(primary_key=True,
                          null=False,
                          editable=False,
                          unique=True)
    name = models.CharField(max_length=50)
    clorie = models.IntegerField(null=True)
    potion = models.IntegerField(null=True)
    level = models.IntegerField(null=True)
    star_level = models.IntegerField(null=True)
    prepare = models.TextField()
    youtube_url = models.CharField(max_length=500, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cover_image = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


#UserFavoriteFood
class UserFavoriteFood(models.Model):
    id = models.AutoField(primary_key=True,
                          null=False,
                          editable=False,
                          unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return 'model'


#Review
class Review(models.Model):
    id = models.AutoField(primary_key=True,
                          null=False,
                          editable=False,
                          unique=True)
    content = models.TextField()
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return 'model'


#Ingredient
class Ingredient(models.Model):
    id = models.AutoField(primary_key=True,
                          null=False,
                          editable=False,
                          unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


#FoodIngredient
class FoodIngredient(models.Model):
    id = models.AutoField(primary_key=True,
                          null=False,
                          editable=False,
                          unique=True)
    quantity = models.CharField(max_length=50)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True)
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   null=True)

    def __str__(self):
        return 'model'
