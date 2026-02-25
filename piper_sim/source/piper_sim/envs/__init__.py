"""Environment registrations for Piper Sim."""

import gymnasium as gym

from .piper_env_cfg import PiperEnvCfg, PiperEnvCfg_PLAY


gym.register(
    id="Piper-Shelf-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": PiperEnvCfg,
    },
)

gym.register(
    id="Piper-Shelf-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": PiperEnvCfg_PLAY,
    },
)
