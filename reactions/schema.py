import graphene
from graphene_django.types import DjangoObjectType
from .models import Reaction, BoatLinkReaction
from users.schema import UserType
from django.contrib.auth import get_user_model


User = get_user_model()

class ReactionType(DjangoObjectType):
    class Meta:
        model = Reaction

class BoatLinkReactionType(DjangoObjectType):
    class Meta:
        model = BoatLinkReaction


class CreateReaction(graphene.Mutation):
    description = graphene.String(required=True)

    class Arguments:
        description = graphene.String(required=True)
    def mutate(self, info, description):
        description_upper = description.upper()
        if Reaction.objects.filter(description=description_upper).exists():
            raise Exception("Ya existe una reacción con esta descripción")

        reaction = Reaction(description=description_upper)
        reaction.save()

        return CreateReaction(description=reaction.description)


class CreateBoatLinkReaction(graphene.Mutation):
    reaction = graphene.Field(ReactionType)
    link_id = graphene.Int()
    user = graphene.Field(UserType)
    class Arguments:
        reaction_id = graphene.Int(required=True)
        link_id = graphene.Int(required=True)

    def mutate(self, info, reaction_id, link_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")

        # Validar que no exista ya la reacción
        if BoatLinkReaction.objects.filter(link_id=link_id, user=user).exists():
            raise Exception("Ya reaccionaste a este link")

        reaction = Reaction.objects.get(id=reaction_id)
        boat_link_reaction = BoatLinkReaction.objects.create(
            reaction=reaction,
            link_id=link_id,
            user=user
        )

        return CreateBoatLinkReaction(
            reaction=reaction,
            link_id=link_id,
            user=user
        )
    
class CreateOrToggleBoatLinkReaction(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    boat_link_reaction = graphene.Field(lambda: BoatLinkReactionType)

    class Arguments:
        reaction_id = graphene.Int(required=True)
        link_id = graphene.Int(required=True)

    def mutate(self, info, reaction_id, link_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")

        # Buscar reacción existente
        existing_reaction = BoatLinkReaction.objects.filter(link_id=link_id, user=user).first()

        # Reacción es la misma => eliminar
        if existing_reaction and existing_reaction.reaction_id == reaction_id:
            existing_reaction.delete()
            return CreateOrToggleBoatLinkReaction(
                success=True,
                message="Reacción eliminada",
                boat_link_reaction=None
            )

        # Reacción es distinta => actualizar
        if existing_reaction:
            existing_reaction.reaction_id = reaction_id
            existing_reaction.save()
            return CreateOrToggleBoatLinkReaction(
                success=True,
                message="Reacción actualizada",
                boat_link_reaction=existing_reaction
            )

        # No existe => crear nueva
        reaction = Reaction.objects.get(id=reaction_id)
        new_reaction = BoatLinkReaction.objects.create(
            reaction=reaction,
            link_id=link_id,
            user=user
        )

        return CreateOrToggleBoatLinkReaction(
            success=True,
            message="Reacción creada",
            boat_link_reaction=new_reaction
        )

class BoatLinkReactionQuery(graphene.ObjectType):
    allboatlink_reactions = graphene.List(BoatLinkReactionType)
    reactions_by_link = graphene.List(BoatLinkReactionType, link_id=graphene.Int(required=True))

    def resolve_allboatlink_reactions(self, info):
        return BoatLinkReaction.objects.select_related('reaction', 'link', 'user').all()

    def resolve_reactions_by_link(self, info, link_id):
        return BoatLinkReaction.objects.filter(link_id=link_id).select_related('reaction', 'user')
class ReactionQuery(graphene.ObjectType):
    all_reactions = graphene.List(ReactionType)

    def resolve_all_reactions(self, info):
        return Reaction.objects.all()

class Mutation(graphene.ObjectType):
    create_boat_link_reaction = CreateBoatLinkReaction.Field()
    create_or_toggle_boat_link_reaction = CreateOrToggleBoatLinkReaction.Field()
    create_Reaction = CreateReaction.Field()
    
class Query(BoatLinkReactionQuery,ReactionQuery, graphene.ObjectType):
    pass
