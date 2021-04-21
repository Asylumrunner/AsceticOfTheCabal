from enum import Enum

def inspect_entity(entity, depth=0):
    if depth > 5:
        return
    
    prefix = ('-' * depth)

    if hasattr(entity, 'name'):
        print(" ")
        print(prefix + entity.name)
        print(' ' * len(prefix) + '_' * len(entity.name))

    try:
        unpacked_object = vars(entity)
    except TypeError as e:
        unpacked_object = entity
    
    for key in unpacked_object:
        if not key.startswith("__"):
            if isinstance(unpacked_object[key], Enum):
                print(prefix + key + ': ' + str(unpacked_object[key]))
            elif key == 'owner':
                print (prefix + key + ': ' + str(unpacked_object[key]))
            elif hasattr(unpacked_object[key], '__dict__'):
                print(prefix + key + ':')
                inspect_entity(unpacked_object[key], depth+1)
            elif isinstance(unpacked_object[key], dict):
                print(prefix + key + ':')
                inspect_entity(unpacked_object[key], depth+1)
            else:
                print(prefix + key + ': ' + str(unpacked_object[key]))
