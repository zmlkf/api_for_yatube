from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, pagination, permissions, viewsets

from posts.models import Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """
    Viewset for working with posts.
    Implements CRUD methods for the Post model.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsAuthorOrReadOnly, permissions.IsAuthenticatedOrReadOnly)
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer):
        """
        Creates a new post with the current user as the author.
        """
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for viewing groups.
    Allows only reading groups for all users.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    Viewset for working with comments on posts.
    Implements CRUD methods for the Comment model.
    """
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorOrReadOnly, permissions.IsAuthenticatedOrReadOnly)

    def get_post(self):
        """
        Gets the post object by its ID from the URL.
        """
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        """
        Gets all comments for a specific post.
        """
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """
        Creates a new comment on the post
        with the current user as the author.
        """
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """
    Viewset for working with followers.
    Allows viewing user subscriptions.
    When creating a new subscription, automatically
    sets the current user as the follower.
    """
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """
        Gets the list of subscriptions for the current user.
        """
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """
        Creates a new subscription on behalf of the current user.
        """
        serializer.save(user=self.request.user)
