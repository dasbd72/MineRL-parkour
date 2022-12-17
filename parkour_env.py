from enum import Enum
import gym
from gym import spaces
from parkour_wb_specs import PKWB, PKWB_MAP
import random
from typing import Tuple, Dict, Any
import numpy as np

ACTION = [
    # action_set = 0
    Enum('Actions', ['forward', 'camera_left', 'camera_right']),
    # action_set = 1
    Enum('Actions', ['forward', 'jump', 'camera_left', 'camera_right']),
    # action_set = 2
    Enum('Actions', ['forward', 'jump', 'camera_left', 'camera_right', 'camera_down', 'camera_up']),
    # action_set = 3
    Enum('Actions', ['forward', 'jump', 'forward_sprint', 'camera_left', 'camera_right', 'camera_down', 'camera_up']),
    # action_set = 4
    Enum('Actions', ['forward', 'forward_jump', 'forward_sprint', 'camera_left', 'camera_right']),
    # action_set = 5
    Enum('Actions', ['forward', 'forward_jump', 'forward_sprint', 'camera_left', 'camera_right', 'camera_down', 'camera_up']),
]
_ActionType = int
_ObservationType = map

class parkour_env(gym.Env):
    def __init__(self, resolution=(64, 64), map="bridge", debug=False, fast=False, action_set=3, isYawDelta=False) -> None:
        super().__init__()
        self.version = '0.2.6'

        if map in PKWB_MAP.keys():
            self.map = map
        else:
            self.map = PKWB_MAP.keys()[0]
        self.debug = debug
        self.image_shape = resolution + (3,)
        self.fast = fast
        self.action_set = action_set
        self.isYawDelta = isYawDelta

        env_name = 'PKWB_%04d-v0' % (random.randint(0, 9999))
        abs_PK = PKWB(name=env_name, resolution=resolution, map=self.map, manual_reset=self.fast)
        abs_PK.register()
        self.env = gym.make(env_name)
        self.env_alive = False
        self.n_actions = len(ACTION[self.action_set])
        self.action_space = spaces.Discrete(self.n_actions)
        self.observation_space = self.env.observation_space
        self.destination = np.array(PKWB_MAP[self.map])
        
        self.yaw = 0
        self.t = 0

        self.map_size = np.array([100, 100])
        self.walked_block = np.zeros(self.map_size*2, dtype=bool)
        self.walked_cnt = 0

    def step(self, action: _ActionType) -> Tuple[_ObservationType, float, bool, Dict[str, Any]]:
        if not self.debug:
            action_int = action + 1
            action_str = ACTION[self.action_set](action_int).name
            action_space = {
                'forward': 0,
                'jump': 0,
                'sprint': 0,
                'camera': np.array([0, 0])
            }

            if action_str == 'camera_left':
                action_space['camera'][1] = -10
            elif action_str == 'camera_right':
                action_space['camera'][1] = 10
            elif action_str == 'camera_down':
                if self.isYawDelta:
                    action_space['camera'][0] = -10
                    self.yaw = max(-90, self.yaw - 10)
                else:
                    action_space['camera'][0] = -30 - self.yaw
                    self.yaw = -30
            elif action_str == 'camera_up':
                if self.isYawDelta:
                    action_space['camera'][0] = 10
                    self.yaw = min(90, self.yaw + 10)
                else:
                    action_space['camera'][0] = 30 - self.yaw
                    self.yaw = 30
            elif action_str == 'forward_sprint':
                action_space['forward'] = 1
                action_space['sprint'] = 1
            elif action_str == 'forward_jump':
                action_space['forward'] = 1
                action_space['jump'] = 1
            else:
                # forward, jump or sprint
                action_space[action_str] = 1

            # One step forward
            obs, reward, done, info = self.env.step(action_space)
            self.t += 1
            pos = self.extract_pos(obs)

            if self.fast:
                if done:
                    # Environment end
                    self.env_alive = False
                elif reward >= 100:
                    done = True
                elif pos[1] < 2:
                    done = True
                    reward -= 100

                if done and self.env_alive:
                    self.teleport((0, 2, 0), (0, 0))
            else:
                # Environment end
                if reward >= 100:
                    done = True
                if pos[1] < 2:
                    done = True
                    reward -= 100

            dis = np.linalg.norm(pos - self.destination) # Absolute distance to target
            x = int(pos[0]) + self.map_size[0]
            z = int(pos[2]) + self.map_size[1]
            if self.walked_block[x][z] == False:
                self.walked_cnt += 1
                self.walked_block[x][z] = True
                reward += np.linalg.norm(self.destination) - dis
                
            # reward += (np.linalg.norm(self.destination) - dis + self.walked_cnt) / 2
            reward -= 0.01 * self.t

            return (obs, reward, done, info)

        else:
            # Random step result
            obs = self.env.observation_space.sample()
            obs['location_stats']['ypos'] = 2
            obs['location_stats']['xpos'] = random.random() * 5
            obs['location_stats']['zpos'] = random.random() * 5
            reward = 0
            done = np.random.choice(np.arange(0, 2), p=[0.99, 0.01])
            info = {}
            return (obs, reward, done, info)

    def reset(self) -> _ObservationType:
        self.yaw = 0
        self.t = 0
        self.walked_block = np.zeros(self.map_size*2, dtype=bool)
        self.walked_cnt = 0
        if not self.debug:
            if self.env_alive and self.fast:
                obs, _, _, _ = self.teleport((0, 2, 0), (0, 0))
                return obs
            else:
                if self.fast:
                    self.env_alive = True
                print('Resetting environment.')
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

    def teleport(self, pos=(0, 2, 0), rot=(0,0)) -> Tuple[_ObservationType, float, bool, Dict[str, Any]]:
        if not self.debug:
            if self.fast:
                self.env.set_next_chat_message(f'/tp @a {pos[0]} {pos[1]} {pos[2]} {rot[0]} {rot[1]}')
                self.env.step({})
                self.env.step({})
            return self.env.step({})
        return self.env.observation_space.sample()