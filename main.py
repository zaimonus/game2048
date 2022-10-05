from game2048 import Field, Directions

f = Field()
f.start()
directions = ['w', 'a', 's', 'd']

while not f.game_over():
    print(f.field)
    while (direction := input('>>>')) not in directions:
        print(f'{direction} is not a valid direction. Use on of {directions}')
    match direction:
        case 'w':
            f.action(Directions.UP)
        case 'a':
            f.action(Directions.LEFT)
        case 's':
            f.action(Directions.DOWN)
        case 'd':
            f.action(Directions.RIGHT)
    f.spawn_node()
