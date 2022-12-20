from enum import Enum
import gym
from gym import spaces
from parkour_wb_specs import PKWB, PKWB_MAP
import random
from typing import Tuple, Dict, Any
import numpy as np
import xml.etree.ElementTree as ET

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


def parse_map(mapstr: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    tree = ET.fromstring("<Data>" + mapstr + "</Data>")
    x1s, x2s, y1s, y2s, z1s, z2s, types = [], [], [], [], [], [], []
    for ele in tree:
        print(ele.attrib)
        x1s.append(int(ele.get('x1')))
        x2s.append(int(ele.get('x2')))
        y1s.append(int(ele.get('y1')))
        y2s.append(int(ele.get('y2')))
        z1s.append(int(ele.get('z1')))
        z2s.append(int(ele.get('z2')))
        types.append(ele.get('type'))
    xmin, xmax = min(x1s + x2s) - 1, max(x1s + x2s) + 1
    ymin, ymax = min(y1s + y2s) + 1, max(y1s + y2s) + 1
    zmin, zmax = min(z1s + z2s) - 1, max(z1s + z2s) + 1
    xdim = xmax - xmin + 1
    ydim = ymax - ymin + 3
    zdim = zmax - zmin + 1

    destination = np.array([0, 2, 0], dtype=np.int32)
    offset = np.array([-xmin, -ymin, -zmin], dtype=np.int32)
    grid = np.zeros((xdim, ydim, zdim), dtype=np.int32)

    for x1, x2, y1, y2, z1, z2, type in zip(x1s, x2s, y1s, y2s, z1s, z2s, types):
        reward = 0
        if type == 'gold_block':
            reward = 100
            destination = np.array([x1, y1 + 1, z1], dtype=np.int32)
        elif type == 'obsidian':
            reward = 1
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        if y1 > y2:
            y1, y2 = y2, y1

        grid[x1-xmin:x2-xmin+1, y1-ymin+1:y2-ymin+2, z1-zmin:z2-zmin+1] = reward

    return (destination, grid, offset)


class parkour_env(gym.Env):
    def __init__(self, resolution=(64, 64), map="bridge", debug=False, fast=False, action_set=3, isYawDelta=False) -> None:
        super().__init__()
        self.version = '0.3.0'

        if map in PKWB_MAP.keys():
            self.map = map
        else:
            self.map = "bridge"
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
        self.destination, self.grid, self.offset = parse_map(PKWB_MAP[self.map])

        self.yaw = 0
        self.t = 0
        self.walked_block = np.zeros_like(self.grid, dtype=np.bool8)
        self.walked_cnt = 0

    def step(self, action: _ActionType) -> Tuple[_ObservationType, float, bool, Dict[str, Any], bool]:
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
            pos_offset = np.array(pos, dtype=np.int32) + self.offset
            pos_available = np.all((pos_offset < self.grid.shape) & (pos_offset >= np.zeros_like(pos_offset)))

            success = False
            if self.fast:
                if done:
                    # Environment end
                    self.env_alive = False
                elif reward >= 100:
                    done = True
                    success = True
                elif not pos_available:
                    done = True
                    reward -= 100

                if done and self.env_alive:
                    self.teleport((0, 2, 0), (0, 0))
            else:
                # Environment end
                if reward >= 100:
                    done = True
                    success = True
                if not pos_available:
                    done = True
                    reward -= 100

            dis = np.linalg.norm(pos - self.destination)  # Absolute distance to target
            if pos_available and self.walked_block[tuple(pos_offset)] == False:
                self.walked_cnt += 1
                self.walked_block[tuple(pos_offset)] = True
                # reward += np.linalg.norm(self.destination) - dis
                reward += self.grid[tuple(pos_offset)] * (np.linalg.norm(self.destination) - dis)

            # reward += (np.linalg.norm(self.destination) - dis + self.walked_cnt) / 2
            reward -= 0.01 * self.t

            return (obs, reward, done, info, success)

        else:
            # Random step result
            return self.random_step()

    def reset(self) -> _ObservationType:
        self.yaw = 0
        self.t = 0
        self.walked_block = np.zeros_like(self.grid, dtype=np.bool8)
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
        return np.array([obs['location_stats']['xpos'], obs['location_stats']['ypos'], obs['location_stats']['zpos']], dtype=np.float32)

    def teleport(self, pos=(0, 2, 0), rot=(0, 0)) -> Tuple[_ObservationType, float, bool, Dict[str, Any], bool]:
        if not self.debug:
            if self.fast:
                self.env.set_next_chat_message(f'/tp @a {pos[0]} {pos[1]} {pos[2]} {rot[0]} {rot[1]}')
                self.env.step({})
                self.env.step({})
            return self.env.step({})
        return self.random_step()

    def random_step(self) -> Tuple[_ObservationType, float, bool, Dict[str, Any], bool]:
        obs = self.env.observation_space.sample()
        obs['location_stats']['ypos'] = 2
        obs['location_stats']['xpos'] = random.random() * 5
        obs['location_stats']['zpos'] = random.random() * 5
        reward = 0
        done = np.random.choice(np.arange(0, 2), p=[0.99, 0.01])
        info = {}
        success = 0
        return (obs, reward, done, info, success)
