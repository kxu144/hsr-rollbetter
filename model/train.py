import gymnasium as gym
import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.common.evaluation import evaluate_policy

# Import your custom environment
from relic import RelicEnv  # Make sure this file is correct

tensorboard_log_dir = "./logs/dqn_relic_env"

# Create environment
env = RelicEnv()

# Define the DQN model
model = DQN(
    "MlpPolicy",     # Multi-Layer Perceptron policy for continuous state space
    env,             
    learning_rate=1e-3,  
    buffer_size=10000,  
    batch_size=64,  
    gamma=0.99,  # Discount factor
    exploration_fraction=0.2,  
    exploration_final_eps=0.05,  
    target_update_interval=500,  
    train_freq=4,  
    gradient_steps=1,  
    verbose=1,  
    tensorboard_log=tensorboard_log_dir
)

# Train the model
for epoch in range(10):
    model.learn(total_timesteps=100_000, reset_num_timesteps=False, progress_bar=True)

# Save the trained model
model.save("relic_dqn_agent")
