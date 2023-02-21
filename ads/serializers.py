from rest_framework import serializers

from ads.models import Ad, Category


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Ad
        fields = ['id', 'name', 'author', 'price', 'description', 'is_published', 'image', 'category']
