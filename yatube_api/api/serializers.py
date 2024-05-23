from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    Allows creating, updating, and viewing posts.
    Fields:
    - author: The author of the post (read-only).
    """
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for the Group model.
    Allows viewing information about groups.
    """

    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    Allows creating, updating, and viewing comments on posts.
    Fields:
    - author: The author of the comment (read-only).
    """

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    """
    Serializer for the Follow model.
    Allows creating and viewing user subscriptions.
    Fields:
    - user: The user subscribing (read-only).
    By default, this value will be automatically set to
    the current user sending the request to create the subscription.

    - following: The user being subscribed to.
    This field represents the user being subscribed to.
    The parameter queryset=User.objects.all() defines the set of users
    from which the client can choose to create the subscription.
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
        model = Follow
        fields = ('user', 'following')
        validators = (
            validators.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Subscription already exists.'
            ),
        )

    def validate_following(self, following):
        """
        Validation for the following field.
        Checks that the user is not trying to subscribe to themselves.
        """
        if self.context['request'].user == following:
            raise serializers.ValidationError(
                'Cannot subscribe to yourself!')
        return following
