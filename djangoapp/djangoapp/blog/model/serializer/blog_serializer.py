from rest_framework import serializers

from blog.model.blog import Blog


class BlogSerializer(serializers.ModelSerializer):
    model = Blog
    fields = '__all__'
