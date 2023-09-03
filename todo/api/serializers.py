from rest_framework import serializers

from main.models import Category, Task


class CategorySerializer(serializers.ModelSerializer):
    """ Category serializer. """

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
        )


class TaskReadSerializer(serializers.ModelSerializer):
    """ Task serializer for reading. """

    category = CategorySerializer()
    file = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'created_at',
            'due_date',
            'category',
        )

    def get_file(self, obj):
        if obj.file:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.file.url)
        return None


class TaskCreateSerializer(serializers.ModelSerializer):
    """ Task serializer for creation. """

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
    )
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'due_date',
            'user',
            'category',
            'file',
        )

    def to_representation(self, instance):
        return TaskReadSerializer(instance).data
