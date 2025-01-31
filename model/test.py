from stable_baselines3 import DQN

# Load the trained model
model = DQN.load("relic_dqn_agent")  # Adjust path if necessary

import gymnasium as gym
from relic import RelicEnv  # Replace with your actual environment

# Create the test environment
env = RelicEnv()

# Run the agent for a few episodes and visualize the behavior
for episode in range(5):  # Run 5 episodes
    obs, _ = env.reset()
    done = False
    total_reward = 0
    while not done:
        #env.render()
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, done, _, _info = env.step(action)
        total_reward += reward
    print(f"Episode {episode + 1} finished with total reward: {total_reward}")
    print(env.kept_pieces)

