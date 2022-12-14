from enum import Enum
import gym
from gym import spaces
from parkour_wb_specs import PKWB, PKWB_MAP
import random
from typing import Tuple, Dict, Any
import numpy as np

ACTION = Enum('Actions', ['forward', 'jump', 'sprint', 'camera_left', 'camera_right', 'camera_down', 'camera_up'])
_ActionType = int
_ObservationType = map

class parkour_env(gym.Env):
    def __init__(self, resolution=(64, 64), map="bridge", debug=False, fast=False) -> None:
        super().__init__()
        if map in PKWB_MAP.keys():
            self.map = map
        else:
            self.map = PKWB_MAP.keys()[0]
        self.debug = debug
        self.image_shape = resolution + (3,)
        self.fast = fast

        env_name = 'PKWB_%04d-v0' % (random.randint(0, 9999))
        abs_PK = PKWB(name=env_name, resolution=resolution, map=self.map, manual_reset=self.fast)
        abs_PK.register()
        self.env = gym.make(env_name)
        self.n_actions = len(ACTION)
        self.action_space = spaces.Discrete(self.n_actions)
        self.observation_space = self.env.observation_space
        self.destination = np.array(PKWB_MAP[self.map])
        
        self.yaw = 0
        self.t = 0

    def step(self, action: _ActionType) -> Tuple[_ObservationType, float, bool, Dict[str, Any]]:
        action_int = action + 1
        action_space = {
            'forward': 0,
            'jump': 0,
            'sprint': 0,
            'camera': [0, 0]
        }

        if action_int == ACTION.forward.value:
            action_space['forward'] = 1
        elif action_int == ACTION.jump.value:
            action_space['jump'] = 1
        elif action_int == ACTION.sprint.value:
            action_space['forward'] = 1
            action_space['sprint'] = 1
        elif action_int == ACTION.camera_left.value:
            action_space['camera'][1] = 10
        elif action_int == ACTION.camera_right.value:
            action_space['camera'][1] = 10
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
            done = np.random.choice(np.arange(0, 2), p=[0.99, 0.01])
            info = {}
        self.t += 1
        pos = self.extract_pos(obs)

        if (reward <= 0 and done) or pos[1] < 2:
            reward -= 50

        if pos[1] < 2:
            if self.fast:
                self.env.set_next_chat_message("/tp @a 0 2 0")
            else:
                done = True

        dis = np.linalg.norm(pos - self.destination)
        reward -= dis
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
        if not self.debug and not self.fast:
            return self.env.render(mode)
        else:
            return

    def close(self) -> None:
        if not self.debug:
            self.env.close()
            return
        else:
            return
    
    def extract_pos(self, obs) -> np.ndarray:
        return np.array([obs['location_stats']['xpos'], obs['location_stats']['ypos'], obs['location_stats']['zpos']])