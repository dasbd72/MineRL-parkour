# MinerRL Parkour Spec

A Minecraft RL parkour training environment for MineRL.

## Usage

### parkour_env
Import

```python
from parkour_env import parkour_env
env = parkour_env()
```

### PKWB

Import gym and the spec.
```python
import gym
from parkour_wb_specs import PKWB
```

Register the environment.
```python
abs_PK = PKWB(resolution=(64,64), map="bridge", manual_reset=False)
abs_PK.register()
env = gym.make("PKWB-v0")
```

## API

### maps

* "bridge": A straight bridge
* "bridge_turn_left": A bridge that needs to turn left then turn right.
* "bridge_turn_right": A bridge that needs to turn right then turn left.
* "bridge_lift": A bridge that requires to jump up two steps.
* "bridge_hole": A straight bridge with a hole.
* "bridge_turn_left_hole"
* "bridge_turn_right_hole"

### parkour_env

* resolution: (int, int)
* map: str
* debug: bool
  * Enables debug mode (runs extremely faster without launching minecraft)

### PKWB

* resolution: (int, int)
* map: str
* manual_reset: bool
  * Enabling manual reset teleports the agent to the original point once it falls out of map.
  * Not compatible with
    * action_space.sample()
    * env.render()
    * and some other functions