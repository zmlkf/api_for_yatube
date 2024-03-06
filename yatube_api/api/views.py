from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, pagination, permissions, viewsets

from posts.models import Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с постами.
    Реализует методы CRUD для модели Post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer):
        """
        Создает новый пост с указанием текущего пользователя в качестве автора.
        """
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для просмотра групп.
    Позволяет только чтение групп для всех пользователей
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с комментариями к постам.
    Реализует методы CRUD для модели Comment
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_post(self):
        """
        Получает объект поста по его идентификатору из URL.
        """
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        """
        Получает все комментарии для конкретного поста.
        """
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """
        Создает новый комментарий к посту
        с указанием текущего пользователя в качестве автора.
        """
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """
    Вьюсет для работы с подписчиками.
    Позволяет просматривать подписки пользователя.
    При создании новой подписки автоматически
    устанавливает текущего пользователя как подписчика.
    """
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """
        Получает список подписок текущего пользователя.
        """
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """
        Создает новую подписку от имени текущего пользователя.
        """
        serializer.save(user=self.request.user)
