"""Visualization script for Piper environment using Rerun."""

import argparse

import gymnasium as gym

import piper_sim.envs  # noqa: F401 - Register environments


def main():
    """Main function to visualize the Piper environment."""
    parser = argparse.ArgumentParser(
        description="Visualize Piper environment with Rerun"
    )
    parser.add_argument(
        "--task",
        type=str,
        default="Isaac-Piper-Basic-Play-v0",
        help="Task name to visualize",
    )
    parser.add_argument(
        "--num_envs", type=int, default=1, help="Number of environments to create"
    )
    parser.add_argument(
        "--num_steps", type=int, default=1000, help="Number of steps to run"
    )
    args = parser.parse_args()

    print(f"Creating environment: {args.task}")

    # Create the environment
    env = gym.make(
        args.task,
        render_mode="human",  # Use Rerun for visualization
    )

    print("Environment created successfully!")
    print(f"Observation space: {env.observation_space}")
    print(f"Action space: {env.action_space}")

    # Reset the environment
    obs, _info = env.reset()
    print(f"Initial observation shape: {obs.shape}")

    # Run simulation steps
    print(f"\nRunning {args.num_steps} steps...")
    print("Press Ctrl+C to stop\n")

    try:
        for step in range(args.num_steps):
            # Sample random action
            action = env.action_space.sample()

            # Step the environment
            obs, reward, terminated, truncated, info = env.step(action)

            # Check for episode end
            if terminated or truncated:
                print(f"Episode ended at step {step}")
                obs, info = env.reset()

            # Print progress every 100 steps
            if step % 100 == 0:
                print(f"Step {step}/{args.num_steps}")

    except KeyboardInterrupt:
        print("\nVisualization stopped by user")

    finally:
        # Close the environment
        env.close()
        print("Environment closed")


if __name__ == "__main__":
    main()
