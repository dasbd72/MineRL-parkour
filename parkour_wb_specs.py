from minerl.herobraine.env_specs.simple_embodiment import SimpleEmbodimentEnvSpec
from minerl.herobraine.hero.handler import Handler
import minerl.herobraine.hero.handlers as handlers
from typing import List

PKWB_DOC = """
In PKWB, player parkours.
"""

PKWB_LENGTH = 1000000
PKWB_MAP = {
    "bridge": (0, 1, 5),
    "bridge_turn_left": (4, 1, 9), 
    "bridge_turn_right": (-4, 1, 9), 
    "bridge_lift": (0, 3, 7), 
    "bridge_hole": (0, 1, 9), 
    "bridge_turn_left_hole": (4, 1, 10), 
    "bridge_turn_right_hole": (-4, 1, 10),
    "bridge_hybrid": (0, 3, 16)
}

class PKWB(SimpleEmbodimentEnvSpec):
    def __init__(self, resolution=(64,64), map="bridge", manual_reset=False, *args, **kwargs):
        """
        map types
        bridge: a bridge
        bridge_turn: a bridge that needs to turn twice
        """
        if 'name' not in kwargs:
            kwargs['name'] = 'PKWB-v0'
        
        self.manual_reset = manual_reset
        self.map = map
        self.maps = {
            "bridge": [
                handlers.DrawingDecorator("""
                    <DrawCuboid x1="0" y1="1" z1="0" x2="0" y2="1" z2="4" type="obsidian"/>
                    <DrawCuboid x1="0" y1="1" z1="5" x2="0" y2="1" z2="5" type="gold_block"/>
                """)
            ], 
            "bridge_turn_left": [
                handlers.DrawingDecorator("""
                    <DrawCuboid x1="0" y1="1" z1="0" x2="0" y2="1" z2="4" type="obsidian"/>
                    <DrawCuboid x1="0" y1="1" z1="4" x2="4" y2="1" z2="4" type="obsidian"/>
                    <DrawCuboid x1="4" y1="1" z1="4" x2="4" y2="1" z2="8" type="obsidian"/>
                    <DrawCuboid x1="4" y1="1" z1="9" x2="4" y2="1" z2="9" type="gold_block"/>
                """)
            ],
            "bridge_turn_right": [
                handlers.DrawingDecorator("""
                    <DrawCuboid x1="0" y1="1" z1="0" x2="0" y2="1" z2="4" type="obsidian"/>
                    <DrawCuboid x1="0" y1="1" z1="4" x2="-4" y2="1" z2="4" type="obsidian"/>
                    <DrawCuboid x1="-4" y1="1" z1="4" x2="-4" y2="1" z2="8" type="obsidian"/>
                    <DrawCuboid x1="-4" y1="1" z1="9" x2="-4" y2="1" z2="9" type="gold_block"/>
                """)
            ],
            "bridge_lift": [
                handlers.DrawingDecorator("""
                    <DrawCuboid x1="0" y1="1" z1="0" x2="0" y2="1" z2="3" type="obsidian"/>
                    <DrawCuboid x1="0" y1="2" z1="4" x2="0" y2="2" z2="4" type="obsidian"/>
                    <DrawCuboid x1="0" y1="3" z1="5" x2="0" y2="3" z2="6" type="obsidian"/>
                    <DrawCuboid x1="0" y1="3" z1="7" x2="0" y2="3" z2="7" type="gold_block"/>
                """)
            ], 
            "bridge_hole": [
                handlers.DrawingDecorator("""
                    <DrawCuboid x1="0" y1="1" z1="0" x2="0" y2="1" z2="3" type="obsidian"/>
                    <DrawCuboid x1="0" y1="1" z1="5" x2="0" y2="1" z2="8" type="obsidian"/>
                    <DrawCuboid x1="0" y1="1" z1="9" x2="0" y2="1" z2="9" type="gold_block"/>
                """)
            ],
            "bridge_turn_left_hole": [
                handlers.DrawingDecorator("""
                    <DrawCuboid x1="4" y1="1" z1="10" x2="4" y2="1" z2="10" type="gold_block"/>
                    <DrawCuboid x1="0" y1="1" z1="0" x2="0" y2="1" z2="2" type="obsidian"/>
                    <DrawCuboid x1="0" y1="1" z1="4" x2="0" y2="1" z2="5" type="obsidian"/>
                    <DrawCuboid x1="0" y1="1" z1="5" x2="4" y2="1" z2="5" type="obsidian"/>
                    <DrawCuboid x1="4" y1="1" z1="5" x2="4" y2="1" z2="8" type="obsidian"/>
                """)
            ],
            "bridge_turn_right_hole": [
                handlers.DrawingDecorator("""
                    <DrawCuboid x1="-4" y1="1" z1="10" x2="-4" y2="1" z2="10" type="gold_block"/>
                    <DrawCuboid x1="0" y1="1" z1="0" x2="0" y2="1" z2="2" type="obsidian"/>
                    <DrawCuboid x1="0" y1="1" z1="4" x2="0" y2="1" z2="5" type="obsidian"/>
                    <DrawCuboid x1="0" y1="1" z1="5" x2="-4" y2="1" z2="5" type="obsidian"/>
                    <DrawCuboid x1="-4" y1="1" z1="5" x2="-4" y2="1" z2="8" type="obsidian"/>
                """)
            ], "bridge_hybrid": [
                handlers.DrawingDecorator("""
                    <DrawCuboid x1="0" y1="1" z1="0" x2="0" y2="1" z2="3" type="obsidian"/>
                    <DrawCuboid x1="0" y1="1" z1="5" x2="0" y2="1" z2="6" type="obsidian"/>
                    <DrawCuboid x1="0" y1="1" z1="6" x2="5" y2="1" z2="6" type="obsidian"/>
                    <DrawCuboid x1="5" y1="1" z1="6" x2="5" y2="1" z2="7" type="obsidian"/>
                    <DrawCuboid x1="5" y1="1" z1="9" x2="5" y2="1" z2="10" type="obsidian"/>
                    <DrawCuboid x1="5" y1="2" z1="10" x2="5" y2="2" z2="11" type="obsidian"/>
                    <DrawCuboid x1="5" y1="3" z1="11" x2="5" y2="3" z2="13" type="obsidian"/>
                    <DrawCuboid x1="5" y1="3" z1="13" x2="0" y2="3" z2="13" type="obsidian"/>
                    <DrawCuboid x1="0" y1="3" z1="13" x2="0" y2="3" z2="14" type="obsidian"/>
                    <DrawCuboid x1="0" y1="3" z1="16" x2="0" y2="3" z2="16" type="gold_block"/>
                """)
            ]
        }

        super().__init__(*args,
                    max_episode_steps=PKWB_LENGTH,
                    reward_threshold=100.0, 
                    resolution=resolution,
                    **kwargs)

    def create_server_world_generators(self) -> List[Handler]:
        if self.manual_reset:
            return [handlers.FlatWorldGenerator(generatorString="1;0;1")] + self.maps[self.map]
        else:
            return [handlers.FlatWorldGenerator(generatorString="1;0;1")] + self.maps[self.map]

    def create_agent_start(self) -> List[Handler]:
        return [
            handlers.AgentStartPlacement(0, 2, 0, 0, 0)
        ]

    def create_rewardables(self) -> List[Handler]:
        return [
            # reward the agent for touching a gold block (but only once)
            handlers.RewardForTouchingBlockType([
                {'type':'gold_block', 'behaviour':'onceOnly', 'reward':'100'}
            ]),
            # also reward on mission end
            handlers.RewardForMissionEnd(100)
        ]

    def create_agent_handlers(self) -> List[Handler]:
        return [
            # make the agent quit
            handlers.AgentQuitFromTouchingBlockType([
                'glass'
            ])
        ]

    def create_actionables(self) -> List[Handler]:
        if self.manual_reset:
            return super().create_actionables() + [
                handlers.ChatAction()
            ]
        else:
            return super().create_actionables()

    def create_observables(self) -> List[Handler]:
        return super().create_observables() + [
            handlers.ObservationFromCurrentLocation()
        ]

    def create_server_initial_conditions(self) -> List[Handler]:
        return [
            # Sets time to morning and stops passing of time
            handlers.TimeInitialCondition(False, 6000)
        ]

    # see API reference for use cases of these first two functions
    def create_server_quit_producers(self):
        return []

    def create_server_decorators(self) -> List[Handler]:
        return []

    # the episode can terminate when this is True
    def determine_success_from_rewards(self, rewards: list) -> bool:
        return sum(rewards) >= self.reward_threshold

    def is_from_folder(self, folder: str) -> bool:
        return folder == 'pkwb'

    def get_docstring(self):
        return PKWB_DOC