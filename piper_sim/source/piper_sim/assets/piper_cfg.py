"""Configuration for Piper arm."""

import os

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets import ArticulationCfg


# TODO: dynamic path
ASSETS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "..",
    "..",
    "..",
    "assets",
)
PIPER_USD_PATH = os.path.join(ASSETS_DIR, "piper_usd", "piper.usd")

PROPS_DIR = os.path.join(ASSETS_DIR, "Props")


def get_props_usd_path(prop_name: str) -> str:
    """Get the path to a prop USD file."""
    possible_paths = [
        os.path.join(PROPS_DIR, f"{prop_name}.usd"),
        os.path.join(PROPS_DIR, prop_name, f"{prop_name}.usd"),
        os.path.join(PROPS_DIR, prop_name.lower(), f"{prop_name.lower()}.usd"),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    # let it fail here, catching it later with proper errors
    return possible_paths[0]


##
# Robot Configuration
##

PIPER_ARM_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=PIPER_USD_PATH,
        activate_contact_sensors=True,
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.8),  # on top of table
        rot=(1.0, 0.0, 0.0, 0.0),  # Identity rotation
        joint_pos={
            # TODO: adjust based on actual USD
            "joint1": 0.0,
            "joint2": 0.0,
            "joint3": 0.0,
            "joint4": 0.0,
            "joint5": 0.0,
            "joint6": 0.0,
        },
    ),
    actuators={
        "arm": ImplicitActuatorCfg(
            joint_names_expr=["joint.*"],
            effort_limit=100.0,
            velocity_limit=10.0,
            stiffness=100.0,
            damping=10.0,
            armature=0.01,
        ),
    },
)

##
# Props Configuration
##


def get_table_cfg():
    """Get table configuration as a rigid object."""
    from isaaclab.assets import RigidObjectCfg

    return RigidObjectCfg(
        prim_path="{ENV_REGEX_NS}/Table",
        spawn=sim_utils.CuboidCfg(
            size=(1.0, 0.6, 0.05),
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
                disable_gravity=False,
                linear_damping=0.0,
                angular_damping=0.0,
            ),
            mass_props=sim_utils.MassPropertiesCfg(mass=10.0),
            collision_props=sim_utils.CollisionPropertiesCfg(
                collision_enabled=True,
            ),
            visual_material=sim_utils.PreviewSurfaceCfg(
                diffuse_color=(0.4, 0.25, 0.1),
            ),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(
            pos=(0.0, 0.0, 0.775),
        ),
    )


def get_shelf_cfg():
    """Get shelf configuration as a rigid object."""
    from isaaclab.assets import RigidObjectCfg

    return RigidObjectCfg(
        prim_path="{ENV_REGEX_NS}/Shelf",
        spawn=sim_utils.CuboidCfg(
            size=(1.0, 0.4, 0.05),
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
                disable_gravity=False,
            ),
            mass_props=sim_utils.MassPropertiesCfg(mass=5.0),
            collision_props=sim_utils.CollisionPropertiesCfg(
                collision_enabled=True,
            ),
            visual_material=sim_utils.PreviewSurfaceCfg(
                diffuse_color=(0.7, 0.7, 0.7),
            ),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(
            pos=(0.0, -0.5, 1.5),
        ),
    )


def get_box_cfg():
    """Get box configuration."""
    from isaaclab.assets import RigidObjectCfg

    return RigidObjectCfg(
        prim_path="{ENV_REGEX_NS}/Box",
        spawn=sim_utils.UsdFileCfg(
            usd_path=get_props_usd_path("Box"),
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
                disable_gravity=False,
            ),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(
            pos=(0.0, 0.0, 0.825),
        ),
    )


def get_container_cfg():
    """Get container configuration."""
    from isaaclab.assets import RigidObjectCfg

    return RigidObjectCfg(
        prim_path="{ENV_REGEX_NS}/Container",
        spawn=sim_utils.UsdFileCfg(
            usd_path=get_props_usd_path("Container"),
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
                disable_gravity=False,
            ),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(
            pos=(0.0, 0.0, 0.825),
        ),
    )


AVAILABLE_PROPS = {
    "Box": get_box_cfg,
    "Container": get_container_cfg,
}


def get_random_prop_cfg(seed: int | None = None):
    """Get a random prop configuration."""
    import random

    if seed is not None:
        random.seed(seed)

    prop_name = random.choice(list(AVAILABLE_PROPS.keys()))
    return AVAILABLE_PROPS[prop_name]()
