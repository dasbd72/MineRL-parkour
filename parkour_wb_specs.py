from minerl.herobraine.env_specs.simple_embodiment import SimpleEmbodimentEnvSpec
from minerl.herobraine.hero.handler import Handler
import minerl.herobraine.hero.handlers as handlers
from typing import List

PKWB_DOC = """
In PKWB, player parkours.
"""

PKWB_LENGTH = 1000000
PKWB_MAP = {
    "bridge":
        """
            <DrawCuboid x1="0" y1="1" z1="0" x2="0" y2="1" z2="4" type="obsidian"/>
            <DrawCuboid x1="0" y1="1" z1="5" x2="0" y2="1" z2="5" type="gold_block"/>
        """,
    "bridge_turn_left":
        """
            <DrawCuboid x1="0" y1="1" z1="0" x2="0" y2="1" z2="4" type="obsidian"/>
            <DrawCuboid x1="0" y1="1" z1="4" x2="4" y2="1" z2="4" type="obsidian"/>
            <DrawCuboid x1="4" y1="1" z1="4" x2="4" y2="1" z2="8" type="obsidian"/>
            <DrawCuboid x1="4" y1="1" z1="9" x2="4" y2="1" z2="9" type="gold_block"/>
        """,
    "bridge_turn_right":
        """
            <DrawCuboid x1="0" y1="1" z1="0" x2="0" y2="1" z2="4" type="obsidian"/>
            <DrawCuboid x1="0" y1="1" z1="4" x2="-4" y2="1" z2="4" type="obsidian"/>
            <DrawCuboid x1="-4" y1="1" z1="4" x2="-4" y2="1" z2="8" type="obsidian"/>
            <DrawCuboid x1="-4" y1="1" z1="9" x2="-4" y2="1" z2="9" type="gold_block"/>
        """,
    "bridge_lift":
        """
            <DrawCuboid x1="0" y1="1" z1="0" x2="0" y2="1" z2="3" type="obsidian"/>
            <DrawCuboid x1="0" y1="2" z1="4" x2="0" y2="2" z2="4" type="obsidian"/>
            <DrawCuboid x1="0" y1="3" z1="5" x2="0" y2="3" z2="6" type="obsidian"/>
            <DrawCuboid x1="0" y1="3" z1="7" x2="0" y2="3" z2="7" type="gold_block"/>
        """,
    "bridge_hole":
        """
            <DrawCuboid x1="0" y1="1" z1="0" x2="0" y2="1" z2="3" type="obsidian"/>
            <DrawCuboid x1="0" y1="1" z1="5" x2="0" y2="1" z2="8" type="obsidian"/>
            <DrawCuboid x1="0" y1="1" z1="9" x2="0" y2="1" z2="9" type="gold_block"/>
        """,
    "bridge_turn_left_hole":
        """
            <DrawCuboid x1="4" y1="1" z1="10" x2="4" y2="1" z2="10" type="gold_block"/>
            <DrawCuboid x1="0" y1="1" z1="0" x2="0" y2="1" z2="2" type="obsidian"/>
            <DrawCuboid x1="0" y1="1" z1="4" x2="0" y2="1" z2="5" type="obsidian"/>
            <DrawCuboid x1="0" y1="1" z1="5" x2="4" y2="1" z2="5" type="obsidian"/>
            <DrawCuboid x1="4" y1="1" z1="5" x2="4" y2="1" z2="8" type="obsidian"/>
        """,
    "bridge_turn_right_hole":
        """
            <DrawCuboid x1="-4" y1="1" z1="10" x2="-4" y2="1" z2="10" type="gold_block"/>
            <DrawCuboid x1="0" y1="1" z1="0" x2="0" y2="1" z2="2" type="obsidian"/>
            <DrawCuboid x1="0" y1="1" z1="4" x2="0" y2="1" z2="5" type="obsidian"/>
            <DrawCuboid x1="0" y1="1" z1="5" x2="-4" y2="1" z2="5" type="obsidian"/>
            <DrawCuboid x1="-4" y1="1" z1="5" x2="-4" y2="1" z2="8" type="obsidian"/>
        """,
    "bridge_hybrid":
        """
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
        """,
    "bridge_hybrid2":
        """
            <DrawCuboid x1="0" y1="1" z1="0" x2="0" y2="1" z2="3" type="obsidian"/>
            <DrawCuboid x1="0" y1="1" z1="5" x2="0" y2="1" z2="6" type="obsidian"/>
            <DrawCuboid x1="0" y1="1" z1="6" x2="5" y2="1" z2="6" type="obsidian"/>
            <DrawCuboid x1="5" y1="1" z1="6" x2="5" y2="1" z2="7" type="obsidian"/>
            <DrawCuboid x1="5" y1="1" z1="9" x2="5" y2="1" z2="10" type="obsidian"/>
            <DrawCuboid x1="5" y1="2" z1="10" x2="5" y2="2" z2="11" type="obsidian"/>
            <DrawCuboid x1="5" y1="3" z1="11" x2="5" y2="3" z2="13" type="obsidian"/>
            <DrawCuboid x1="5" y1="3" z1="13" x2="2" y2="3" z2="13" type="obsidian"/>
            <DrawCuboid x1="2" y1="3" z1="13" x2="2" y2="3" z2="10" type="obsidian"/>
            <DrawCuboid x1="2" y1="3" z1="10" x2="1" y2="3" z2="10" type="obsidian"/>
            <DrawCuboid x1="-1" y1="3" z1="10" x2="-1" y2="3" z2="13" type="obsidian"/>
            <DrawCuboid x1="-2" y1="3" z1="13" x2="-2" y2="3" z2="15" type="obsidian"/>
            <DrawCuboid x1="-2" y1="3" z1="16" x2="-2" y2="3" z2="16" type="gold_block"/>
        """,
    "bridge_debug":
        """
            <DrawCuboid x1="0" y1="1" z1="0" x2="0" y2="1" z2="0" type="obsidian"/>
            <DrawCuboid x1="0" y1="1" z1="1" x2="0" y2="1" z2="1" type="gold_block"/>
        """,
}


class PKWB(SimpleEmbodimentEnvSpec):
    def __init__(self, resolution=(64, 64), map="bridge", manual_reset=False, *args, **kwargs):
        """
        map types
        bridge: a bridge
        bridge_turn: a bridge that needs to turn twice
        """
        if 'name' not in kwargs:
            kwargs['name'] = 'PKWB-v0'

        self.manual_reset = manual_reset
        self.map = map

        super().__init__(*args,
                         max_episode_steps=PKWB_LENGTH,
                         reward_threshold=100.0,
                         resolution=resolution,
                         **kwargs)

    def create_server_world_generators(self) -> List[Handler]:
        if self.manual_reset:
            return [handlers.FlatWorldGenerator(generatorString="1;0;2")] + [handlers.DrawingDecorator(PKWB_MAP[self.map])]
        else:
            return [handlers.FlatWorldGenerator(generatorString="1;0;2")] + [handlers.DrawingDecorator(PKWB_MAP[self.map])]

    def create_agent_start(self) -> List[Handler]:
        return [
            handlers.AgentStartPlacement(0, 2, 0, 0, 0)
        ]

    def create_rewardables(self) -> List[Handler]:
        return [
            # reward the agent for touching a gold block (but only once)
            handlers.RewardForTouchingBlockType([
                {'type': 'gold_block', 'behaviour': 'constant', 'reward': '100'}
            ])
        ]

    def create_agent_handlers(self) -> List[Handler]:
        if self.manual_reset:
            return []
        else:
            return [
                # make the agent quit
                handlers.AgentQuitFromTouchingBlockType([
                    'gold_block'
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
            handlers.ObservationFromCurrentLocation(),
            handlers.CompassObservation(angle=True, distance=False)
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
