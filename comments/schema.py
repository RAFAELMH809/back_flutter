# comments/schema.py
import graphene
from graphene_django import DjangoObjectType
from .models import Comment
from users.schema import UserType
from links.models import Link
from links.schema import LinkType

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

# Mutation: crear comentario
class CreateComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        link_id = graphene.Int(required=True)
        description = graphene.String(required=True)

    def mutate(self, info, link_id, description):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Autenticación requerida")

        link = Link.objects.get(id=link_id)
        comment = Comment.objects.create(link=link, user=user, description=description)

        return CreateComment(comment=comment)

# Mutation: eliminar comentario
class DeleteComment(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        comment_id = graphene.Int(required=True)

    def mutate(self, info, comment_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Autenticación requerida")

        comment = Comment.objects.get(id=comment_id)
        if comment.user != user:
            raise Exception("No tienes permiso para eliminar este comentario")

        comment.delete()
        return DeleteComment(success=True)

# Queries
class CommentQuery(graphene.ObjectType):
    all_comments = graphene.List(CommentType)
    comments_by_link = graphene.List(CommentType, link_id=graphene.Int(required=True))

    def resolve_all_comments(self, info):
        return Comment.objects.select_related("user", "link").all()

    def resolve_comments_by_link(self, info, link_id):
        return Comment.objects.filter(link_id=link_id).select_related("user")
    
class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
    delete_comment = DeleteComment.Field()

