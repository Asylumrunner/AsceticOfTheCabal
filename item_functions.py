import tcod as libtcod
from game_messages import Message 

def heal(*args, **kwargs):
    print(args)
    print(kwargs)
    entity = args[0]
    amount = kwargs.get('amount')

    if entity.fighter.hp < entity.fighter.max_hp:
        entity.fighter.hp = min(entity.fighter.max_hp, entity.fighter.hp + amount)
    if entity.log:
        entity.log.add_message(Message('Healed {0} damage'.format(amount), libtcod.white))

item_fuction_dict = {
    "heal": heal
}