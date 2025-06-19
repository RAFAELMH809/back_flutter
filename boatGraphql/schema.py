import graphene
import graphql_jwt
import graphene

import links.schema
import users.schema
import reactions.schema
import comments.schema
class Query(users.schema.Query,
            links.schema.Query,
            reactions.schema.Query,
            comments.schema.CommentQuery,
            graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation,
     links.schema.Mutation,
     reactions.schema.Mutation,
     comments.schema.Mutation,
     graphene.ObjectType):
    delete_link = links.schema.DeleteLink.Field()
    create_comment = comments.schema.CreateComment.Field()
    delete_comment = comments.schema.DeleteComment.Field()
    create_reaction = reactions.schema.CreateReaction.Field()
    create_boat_link_reaction = reactions.schema.CreateBoatLinkReaction.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

