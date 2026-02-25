"""Piper environment cfg with Newton."""

import isaaclab.envs.mdp as mdp
import isaaclab.sim as sim_utils
from isaaclab.assets import ArticulationCfg, AssetBaseCfg, RigidObjectCfg
from isaaclab.envs import ManagerBasedRLEnvCfg
from isaaclab.envs.mdp.actions import JointPositionActionCfg
from isaaclab.managers import (
    EventTermCfg as EventTerm,
    ObservationGroupCfg as ObsGroup,
    ObservationTermCfg as ObsTerm,
    RewardTermCfg as RewTerm,
    SceneEntityCfg,
    TerminationTermCfg as DoneTerm,
)
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sim import SimulationCfg
from isaaclab.sim._impl.newton_manager_cfg import NewtonCfg
from isaaclab.sim._impl.solvers_cfg import MJWarpSolverCfg
from isaaclab.utils import configclass
from isaaclab.utils.noise import AdditiveUniformNoiseCfg as Unoise
from piper_sim.assets.piper_cfg import (
    PIPER_ARM_CFG,
    get_random_prop_cfg,
    get_shelf_cfg,
    get_table_cfg,
)


##
# Scene
##


@configclass
class PiperSceneCfg(InteractiveSceneCfg):
    """Configuration for shelving simulation."""

    ground = AssetBaseCfg(
        prim_path="/World/ground",
        spawn=sim_utils.GroundPlaneCfg(),
        init_state=AssetBaseCfg.InitialStateCfg(pos=(0.0, 0.0, -1.05)),
    )

    table = get_table_cfg()

    shelf = get_shelf_cfg()

    robot: ArticulationCfg = PIPER_ARM_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

    prop: RigidObjectCfg = get_random_prop_cfg()

    light = AssetBaseCfg(
        prim_path="/World/light",
        spawn=sim_utils.DomeLightCfg(color=(0.75, 0.75, 0.75), intensity=2500.0),
    )


##
# Actions
##


@configclass
class ActionsCfg:
    """Action specifications for joint position control."""

    # Joint position actions for all robot joints
    arm_action: JointPositionActionCfg = JointPositionActionCfg(
        asset_name="robot",
        joint_names=["joint.*"],
        scale=1.0,
        use_default_offset=True,
    )


##
# Observations
##


@configclass
class ObservationsCfg:
    """Observation specifications."""

    @configclass
    class PolicyCfg(ObsGroup):
        """Observations for policy group."""

        # Joint observations
        joint_pos = ObsTerm(func=mdp.joint_pos_rel, noise=Unoise(n_min=-0.01, n_max=0.01))
        joint_vel = ObsTerm(func=mdp.joint_vel_rel, noise=Unoise(n_min=-0.01, n_max=0.01))

        # Previous action
        actions = ObsTerm(func=mdp.last_action)

        def __post_init__(self):
            self.enable_corruption = True
            self.concatenate_terms = True

    # Observation groups
    policy: PolicyCfg = PolicyCfg()


##
# Events
##


@configclass
class EventsCfg:
    """Configuration for events."""

    reset_robot_joints = EventTerm(
        func=mdp.reset_joints_by_scale,
        mode="reset",
        params={
            "position_range": (0.5, 1.5),
            "velocity_range": (0.0, 0.0),
        },
    )


##
# Rewards
##


@configclass
class RewardsCfg:
    """Reward terms for the MDP."""

    # Action penalties
    action_rate = RewTerm(func=mdp.action_rate_l2, weight=-0.0001)
    joint_vel = RewTerm(
        func=mdp.joint_vel_l2,
        weight=-0.0001,
        params={"asset_cfg": SceneEntityCfg("robot")},
    )


##
# Terminations
##


@configclass
class TerminationsCfg:
    """Termination terms for the MDP."""

    time_out = DoneTerm(func=mdp.time_out, time_out=True)
    # Can add more termination conditions here


##
# Configuration
##


@configclass
class PiperEnvCfg(ManagerBasedRLEnvCfg):
    """Configuration for the Piper environment with Newton physics."""

    # for now just 1 env
    scene: PiperSceneCfg = PiperSceneCfg(num_envs=1, env_spacing=2.5)

    observations: ObservationsCfg = ObservationsCfg()
    actions: ActionsCfg = ActionsCfg()

    # MDP settings
    rewards: RewardsCfg = RewardsCfg()
    terminations: TerminationsCfg = TerminationsCfg()
    events: EventsCfg = EventsCfg()

    # attach newton warp
    sim: SimulationCfg = SimulationCfg(
        dt=1.0 / 60.0,
        render_interval=2,
        newton_cfg=NewtonCfg(
            solver_cfg=MJWarpSolverCfg(
                njmax=50,
                nconmax=30,
                ls_iterations=5,
                cone="pyramidal",
                impratio=1,
                ls_parallel=True,
                integrator="implicit",
            ),
            num_substeps=2,
            debug_mode=True,
            use_cuda_graph=True,
        ),
    )

    def __post_init__(self):
        """Post initialization."""
        self.decimation = 2
        self.episode_length_s = 20.0
        self.viewer.eye = (2.0, 2.0, 2.0)
        self.viewer.lookat = (0.0, 0.0, 0.8)


@configclass
class PiperEnvCfg_PLAY(PiperEnvCfg):
    """Configuration for playing/validation."""

    def __post_init__(self):
        """Post initialization."""
        super().__post_init__()

        self.scene.num_envs = 1
        self.scene.env_spacing = 2.5

        self.observations.policy.enable_corruption = False
