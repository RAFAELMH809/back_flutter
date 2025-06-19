import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType
from .models import Link
from users.schema import UserType

User = get_user_model()

class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()
# ...code
#1
class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        url = graphene.String()
        description = graphene.String()

    def mutate(self, info, url, description):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Autenticación requerida")

        link = Link(url=url, description=description, posted_by=user)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            posted_by=link.posted_by
        )



#4
class DeleteLink(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        link_id = graphene.Int(required=True)

    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Autenticación requerida")

        try:
            link = Link.objects.get(id=link_id)
        except Link.DoesNotExist:
            return DeleteLink(success=False, message="El link no existe")

        if link.posted_by != user:
            return DeleteLink(success=False, message="No tienes permiso para eliminar este link")

        link.delete()
        return DeleteLink(success=True, message="Link eliminado exitosamente")

class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    delete_link = DeleteLink.Field()

