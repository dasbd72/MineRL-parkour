from enum import Enum
import gym
from gym import spaces
from parkour_wb_specs import PKWB
import random
from typing import Tuple, Dict, Any

ACTION = Enum('Actions', ['forward', 'jump', 'sprint', 'camera_left', 'camera_right', 'camera_down', 'camera_up'])
_ActionType = int
_ObservationType = map

class parkour_env(gym.Env):
    def __init__(self, resolution=(64, 64), map="bridge", debug=False) -> None:
        super().__init__()
        env_name = 'PKWB_%04d-v0' % (random.randint(0, 9999))
        abs_PK = PKWB(name=env_name, resolution=(64,64), map=map)
        abs_PK.register()

        self.map = map
        self.debug = debug
        self.image_shape = resolution + (3,)

        self.env = gym.make(env_name)
        self.n_actions = len(ACTION)
        self.action_space = spaces.Discrete(self.n_actions)
        self.observation_space = self.env.observation_space
        
        self.yaw = 0
        self.t = 0

    def step(self, action: _ActionType) -> Tuple[_ObservationType, float, bool, Dict[str, Any]]:
        action_int = action + 1
        action_space = self.env.action_space.noop()

        if action_int == ACTION.forward.value:
            action_space['forward'] = 1
        elif action_int == ACTION.jump.value:
            action_space['jump'] = 1
        elif action_int == ACTION.sprint.value:
            action_space['sprint'] = 1
        elif action_int == ACTION.camera_left.value:
            action_space['camera'][1] -= 30
        elif action_int == ACTION.camera_right.value:
            action_space['camera'][1] += 30
        elif action_int == ACTION.camera_down.value:
            action_space['camera'][0] = -30 - self.yaw
            self.yaw = -30
        elif action_int == ACTION.camera_up.value:
            action_space['camera'][0] = 30 - self.yaw
            self.yaw = 30

        if not self.debug:
            obs, reward, done, info = self.env.step(action_space)
        else:
            obs = self.env.observation_space.sample()
            obs['location_stats']['ypos'] = 2
            obs['location_stats']['xpos'] = random.random() * 5
            obs['location_stats']['zpos'] = random.random() * 5
            reward = 0
            done = False
            info = {}
        self.t += 1

        dead = False
        if (reward <= 0 and done) or obs['location_stats']['ypos'] < 2:
            reward -= 50
            dead = True
            done = True

        if not dead:
            dis = (obs['location_stats']['xpos'] ** 2 + obs['location_stats']['zpos'] ** 2 + obs['location_stats']['ypos'] ** 2) ** (1/2)
        else:
            dis = (obs['location_stats']['xpos'] ** 2 + obs['location_stats']['zpos'] ** 2) ** (1/2)
        reward += dis
        reward -= 0.001 * self.t

        return (obs, reward, done, info)

    def reset(self) -> _ObservationType:
        self.yaw = 0
        self.t = 0
        if not self.debug:
            return self.env.reset()
        else:
            return self.env.observation_space.sample()

    def render(self, mode='human') -> Any:
        if not self.debug:
            return self.env.render(mode)
        else:
            return

    def close(self) -> None:
        if not self.debug:
            self.env.close()
            return
        else:
            return