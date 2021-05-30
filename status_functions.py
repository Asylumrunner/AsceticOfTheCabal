import tcod as libtcod
from game_constants import fluids, npcs
from components.fluid import Fluid
from render_functions import RenderOrder
from game_states import AIStates
from entity import Entity

def bleed(affected_entity, entities, game_map):
    if not any ([entity for entity in game_map.get_tile(affected_entity.x, affected_entity.y).get_entities() if entity.has_component('Fluid')]):
        fluid_data = fluids[npcs[affected_entity.name]['blood'] if affected_entity.name in npcs else "blood"]
        fluid_components = {
            "Fluid": Fluid(fluid_data['conductive'], fluid_data['statuses'], fluid_data['time'])
        }
        entities.insert_entity(Entity(affected_entity.x, affected_entity.y, libtcod.CHAR_BLOCK1, fluid_data['color'], fluid_data['name'], False, RenderOrder.LIQUID, affected_entity.log, AIStates.INANIMATE, fluid_components))

def poison(affected_entity, entities, game_map):
    print("Hell yeah bruv you've been poisoned")

def sleep(affected_entity, entities, game_map):
    print("Shit man you NAPPIN")

status_mapping = {
    'bleeding': bleed,
    'poisoned': poison,
    'asleep': sleep
}
