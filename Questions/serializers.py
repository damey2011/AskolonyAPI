from rest_framework import serializers

from Account.serializers import RetrieveUpdateDeleteUserSerializer
from Questions.models import Question


class QuestionCreateSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    last_updated_by = RetrieveUpdateDeleteUserSerializer(required=False)

    class Meta:
        model = Question
        fields = (
            'id',
            'title',
            'author',
            'body',
            'followings',
            'answers',
            'views',
            'created',
            'updated',
            'last_updated_by',
            'slug',
            'is_anonymous'
        )
        extra_kwargs = {
            "author": {
                "required": False
            },
            "last_updated_by": {
                "required": False
            },
        }

    def get_author(self, obj):
        if obj.is_anonymous:
            return "Anonymous"
        return RetrieveUpdateDeleteUserSerializer(obj.author).data


class QuestionRetrieveUpdateDeleteSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    last_updated_by = RetrieveUpdateDeleteUserSerializer()

    class Meta:
        model = Question
        fields = (
            'id',
            'title',
            'author',
            'body',
            'followings',
            'answers',
            'views',
            'created',
            'updated',
            'last_updated_by',
            'slug',
            'is_anonymous'
        )
        extra_kwargs = {
            "author": {
                "required": False
            },
            "last_updated_by": {
                "required": False
            },
        }

    def get_author(self, obj):
        if obj.is_anonymous:
            return "Anonymous"
        return RetrieveUpdateDeleteUserSerializer(obj.author).data
