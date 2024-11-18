from rest_framework import serializers
from .models import Product, Review

class ProductSerializer (serializers.ModelSerializer):
    #used to get "class reviews" from "class serializer"
    review = serializers.SerializerMethodField(method_name="get_reviews", read_only=True)

    class Meta:
        model  = Product
        fields = "__all__"

    def get_reviews(self,obj):
        #obj refers to product by default
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews,many=True)
        return serializer.data


class ReviewSerializer (serializers.ModelSerializer):
    class Meta:
        model  = Review
        fields = "__all__"