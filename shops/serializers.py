from rest_framework import serializers
from shops.models import ShopImage


class ShopImageSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
         return ShopImage.objects.create(
            title = validated_data['title'],
            shop = validated_data['shop'],
            image = validated_data['image'],
        )

    class Meta:
        model = ShopImage
        fields = ('title', 'image', 'shop')
        shop = serializers.Field(source='shop.id')
