import graphene
from graphql_relay import from_global_id
from graphene import InputObjectType

from .models import Planet, People, Film
from .types import PlanetType, PeopleType, FilmType
from .utils import generic_model_mutation_process


class CreatePlanetMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=False)
        name = graphene.String(required=True)
        rotation_period = graphene.String(required=False)
        orbital_period = graphene.String(required=False)
        diameter = graphene.String(required=False)
        climate = graphene.String(required=False)
        gravity = graphene.String(required=False)
        terrain = graphene.String(required=False)
        surface_water = graphene.String(required=False)
        population = graphene.String(required=False)
    planet = graphene.Field(PlanetType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        raw_id = input.get('id', None)

        data = {'model': Planet, 'data': input}
        if raw_id:
            data['id'] = from_global_id(raw_id)[1]

        planet = generic_model_mutation_process(**data)
        return CreatePlanetMutation(planet=planet)


class CreatePeopleMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=False)
        name = graphene.String(required=True)
        mass = graphene.String(required=True)
        height = graphene.String(required=True)
        hair_color = graphene.String(required=True)
        skin_color = graphene.String(required=True)
        eye_color = graphene.String(required=True)
        birth_year = graphene.String(required=True)
        gender = graphene.String(required=False)
        home_world = graphene.GlobalID(parent_type=PlanetType, required=True)

    people = graphene.Field(PeopleType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        raw_id = input.get('id', None)

        data = {'model': People, 'data': input}
        if raw_id:
            data['id'] = from_global_id(raw_id)[1]

        people = generic_model_mutation_process(**data)
        return CreatePeopleMutation(people=people)


class UpdatePeopleInput(InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)
    height = graphene.String(required=False)
    mass = graphene.String(required=False)
    hairColor = graphene.String(required=False)
    skinColor = graphene.String(required=False)
    eyeColor = graphene.String(required=False)
    birthYear = graphene.String(required=False)
    gender = graphene.String(required=False)
    homeworld = graphene.ID(required=False)


class UpdatePeopleMutation(graphene.relay.ClientIDMutation):

    people = graphene.Field(PeopleType)

    class Arguments:
        input = UpdatePeopleInput(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        raw_id = input.get('id', None)
        data = {'model': People, 'data': input}
        if raw_id:
            data['id'] = from_global_id(raw_id)[1]
            People.objects.filter(pk=input.get('id')).update(**input)
            people = People.objects.filter(pk=input.get('id'))
            
        return CreatePeopleMutation(people=people)
