from maps.maps import Map_blueprint

the_map = Map_blueprint(
    name='start',
    file='start.map',
    fields_resolution={
        "1": "path",
        "2": "grass",
        "3": "mountain"
    },
    fields_enemy_probability={
        "2": {"None": 0.0, "Goblin": 0.2, "Goblin Goblin": 0.1, "Ork": 0.05, "Ork Goblin": 0.01}
    },
    drop_rate={
        "Goblin": {
            "Drink": 0.4,
            "Water": 0.4,
            "Longsword": 0.2
        },
        "Ork": {
            "Drink": 0.2,
            "Water": 0.3,
            "Longsword": 0.5
        }
    },
    start=[3, 2],
    sight_range=3
)
