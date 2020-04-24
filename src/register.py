from . import tiles

tiles.register_tile("map:cobble", {
    "textures": ["floor.png"],
})

tiles.register_tile("map:wall", {
    "textures": [
        "wall_0.png",
        "wall_1.png",
        "wall_2.png",
        "wall_3.png",
    ],
})

tiles.register_tile("map:wall_corner_inner", {
    "textures": [
        "wall_corner_inner_0.png",
        "wall_corner_inner_1.png",
        "wall_corner_inner_2.png",
        "wall_corner_inner_3.png",
    ],
})

tiles.register_tile("map:wall_corner_outer", {
    "textures": [
        "wall_corner_outer_0.png",
        "wall_corner_outer_1.png",
        "wall_corner_outer_2.png",
        "wall_corner_outer_3.png",
    ],
})

tiles.register_tile("loot:coins", {
    "textures": ["loot_gold.png"],
})

tiles.register_tile("loot:pile", {
    "textures": ["loot_pile.png"],
})
