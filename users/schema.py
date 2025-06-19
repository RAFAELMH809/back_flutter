from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType

# Tipo GraphQL para el modelo User
class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

# Mutación para crear usuario
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)

# Query con users y me
class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    me = graphene.Field(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user

# Mutaciones disponibles
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


