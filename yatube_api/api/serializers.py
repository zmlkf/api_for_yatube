from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Post.
    Позволяет создавать, обновлять и просматривать посты.
    Поля:
    - author: Автор поста (только чтение).
    """
    author = SlugRelatedField(slug_field='username', read_only=True)

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

    def validate_following(self, value):
        """
        Проверка поля following.
        Проверяет, что пользователь не пытается подписаться на самого себя.
        """
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!')
        return value

    def validate(self, data):
        """
        Проверяет, что комбинация значений полей user и following уникальна.
        """
        if Follow.objects.filter(
            user=self.context['request'].user,
            following=data['following']
        ).exists():
            raise serializers.ValidationError('Подписка уже существует.')

        return data
