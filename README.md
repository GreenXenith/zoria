# Zoria
Real-time 2.5D RPG Dungeon Crawler using PyGame  

## Usage
`python3 zoria.py`

## Controls
| Key     | Action    |
| ------- | --------- |
| `WASD`  | Movement  |
| `SPACE` | Attack    |
| `SHIFT` | Use stair |

## Premise
Each level contains a key and a locked hatch. Collect the key in order to unlock the passage to the next level (`SHIFT` to unlock).  
Slimes do minimal damage, but more spawn on each level. They can drop health or XP. More XP = more damage dealt per hit. Coins are currently useless.  
The levels are infinite and persistent. The only limit is your RAM. World resets on death.  

## Known Bugs
* Window resizing is mostly broken on Linux. This is a bug in SDL2. Using the maximize button _should_ work most of the time.
* Slimes get stuck in corners. Probably due to the raycaster hitting the corner at the start (rounding issue?).
* Walls occasionally render improperly. Usually occurs when two rooms are close to each other diagonally.
