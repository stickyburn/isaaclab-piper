"""Visualize Piper using Rerun."""

import argparse

import gymnasium as gym

import piper_sim.envs  # noqa: F401 - Register environments


def main():
    """Visualize Piper using Rerun."""
    parser = argparse.ArgumentParser(description="Visualize Piper environment with Rerun")
    parser.add_argument(
        "--task",
        type=str,
        default="Isaac-Piper-Basic-Play-v0",
        help="Task to visualize",
    )
    parser.add_argument("--num_envs", type=int, default=1, help="Number of environments")
    parser.add_argument("--num_steps", type=int, default=1000, help="Number of steps to run")
    args = parser.parse_args()

    print(f"Creating environment: {args.task}")

    env = gym.make(
        args.task,
        render_mode="human",
    )

    print("Environment created!")
    print(f"Observation space: {env.observation_space}")
    print(f"Action space: {env.action_space}")

    obs, _info = env.reset()
    print(f"Initial observation shape: {obs.shape}")

    print(f"\nRunning {args.num_steps} steps...")
    print("Press Ctrl+C to stop\n")

    try:
        for step in range(args.num_steps):
            action = env.action_space.sample()

            obs, _reward, terminated, truncated, _info = env.step(action)

            if terminated or truncated:
                print(f"Episode ended at step {step}")
                obs, _info = env.reset()

            if step % 100 == 0:
                print(f"Step {step}/{args.num_steps}")

    except KeyboardInterrupt:
        print("\nVisualization stopped by user")

    finally:
        env.close()
        print("Environment closed")


if __name__ == "__main__":
    main()
