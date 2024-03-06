import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post, User


class Base64ImageField(serializers.ImageField):
    """
    Поле для обработки изображений в формате base64.
    При загрузке изображения в формате base64, данное поле
    декодирует изображение и сохраняет его как объект ContentFile.
    Аргументы:
    - data: Строка, представляющая изображение в формате base64.
    Возвращает объект ContentFile с декодированным изображением.
    """
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Post.
    Позволяет создавать, обновлять и просматривать посты.
    Поля:
    - author: Автор поста (только чтение).
    - image: Изображение поста в формате base64 (опционально).

    """
    author = SlugRelatedField(slug_field='username', read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = '__all__'
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Group.
    Позволяет просматривать информацию о группах.
    """

    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.
    Позволяет создавать, обновлять и просматривать комментарии к постам.
    Поля:
    - author: Автор комментария (только чтение).
    """

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Follow.
    Позволяет создавать и просматривать подписки пользователей.
    Поля:
    - user: Пользователь, который подписывается (только чтение).
    По умолчанию, это значение будет автоматически установлено на
    текущего пользователя, отправляющего запрос на создание подписки.

    - following: Пользователь, на которого подписываются.
    Это поле представляет пользователя, на которого создается подписка.
    Параметр queryset=User.objects.all() определяет набор пользователей,
    среди которых клиент может выбирать для создания подписки.
    """
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow

    def validate(self, data):
        """
        Проверка данных перед сохранением.
        Проверяет, что пользователь не пытается подписаться на самого себя.
        """
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!')
        return data
