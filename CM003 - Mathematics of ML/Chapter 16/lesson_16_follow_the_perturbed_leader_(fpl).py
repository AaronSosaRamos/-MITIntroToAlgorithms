# -*- coding: utf-8 -*-
"""Lesson 16 - Follow the perturbed leader (FPL).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kiCFxmtl5tCssYc7lpFZFBdgMv6t_JiW

# FOLLOW THE PERTURBED LEADER (FPL)
"""

import random
import math

class FollowThePerturbedLeader:
    def __init__(self, num_actions, eta):
        self.num_actions = num_actions  # Number of actions (arms)
        self.eta = eta  # Exploration parameter

        # Initialize weights for each action
        self.weights = [1.0] * num_actions

    def choose_action(self):
        # Perturb weights with random noise
        perturbed_weights = [w + self.eta * random.random() for w in self.weights]

        # Choose action with the highest perturbed weight
        chosen_action = max(range(self.num_actions), key=lambda i: perturbed_weights[i])

        return chosen_action

    def update(self, action, reward):
        # Update weights based on received reward
        total_weight = sum(self.weights)
        normalized_rewards = [reward * (w / total_weight) for w in self.weights]

        for i in range(self.num_actions):
            self.weights[i] *= math.exp(normalized_rewards[i] / self.num_actions)

if __name__ == "__main__":
    # Example usage for a two-armed bandit
    num_actions = 2
    eta = 1.0  # Exploration parameter

    fpl = FollowThePerturbedLeader(num_actions, eta)

    # Simulation of bandit game
    num_steps = 1000
    rewards = []

    for _ in range(num_steps):
        action = fpl.choose_action()

        # Simulate reward (0 or 1 for simplicity)
        reward = random.randint(0, 1)

        # Update FPL algorithm with the observed reward
        fpl.update(action, reward)

        # Collect reward for plotting or analysis
        rewards.append(reward)

    # Print final weights (optional)
    print("Final weights:", fpl.weights)

"""#Exponential Weights Algorithm (Exp3)

The Exponential Weights Algorithm (Exp3) is a well-known algorithm for multi-armed bandit problems, providing a good balance between exploration and exploitation.
"""

import random
import math

class Exp3:
    def __init__(self, num_actions, gamma):
        self.num_actions = num_actions
        self.gamma = gamma  # Exploration parameter

        self.weights = [1.0] * num_actions

    def choose_action(self):
        total_weight = sum(self.weights)
        probabilities = [((1 - self.gamma) * (w / total_weight)) + (self.gamma / self.num_actions) for w in self.weights]

        chosen_action = random.choices(range(self.num_actions), probabilities)[0]
        return chosen_action

    def update(self, action, reward):
        total_weight = sum(self.weights)
        estimated_reward = reward / max(1e-5, ((1 - self.gamma) * (self.weights[action] / total_weight)) + (self.gamma / self.num_actions))
        self.weights[action] *= math.exp(self.gamma * estimated_reward / self.num_actions)

if __name__ == "__main__":
    num_actions = 2
    gamma = 0.1

    exp3 = Exp3(num_actions, gamma)

    num_steps = 1000
    rewards = []

    for _ in range(num_steps):
        action = exp3.choose_action()
        reward = random.randint(0, 1)
        exp3.update(action, reward)
        rewards.append(reward)

    print("Final weights:", exp3.weights)

"""#Softmax Exploration

Softmax Exploration is another technique used in bandit problems that utilizes a softmax function to convert action values into probabities.
"""

import random
import math

class SoftmaxExplorer:
    def __init__(self, num_actions, tau):
        self.num_actions = num_actions
        self.tau = tau  # Temperature parameter

        self.action_values = [0.0] * num_actions

    def choose_action(self):
        # Apply a stable softmax calculation using logarithmic transformation
        log_values = [value / self.tau for value in self.action_values]
        max_log_value = max(log_values)

        # Compute softmax probabilities in log space to prevent overflow
        exp_values = [math.exp(log_value - max_log_value) for log_value in log_values]
        total_exp = sum(exp_values)
        probabilities = [value / total_exp for value in exp_values]

        # Choose action using the computed probabilities
        chosen_action = random.choices(range(self.num_actions), probabilities)[0]
        return chosen_action

    def update(self, action, reward):
        # Simple update: increment the value of the chosen action by the reward received
        self.action_values[action] += reward

if __name__ == "__main__":
    num_actions = 2
    tau = 0.5

    softmax_explorer = SoftmaxExplorer(num_actions, tau)

    num_steps = 1000
    rewards = []

    for _ in range(num_steps):
        action = softmax_explorer.choose_action()
        reward = random.randint(0, 1)
        softmax_explorer.update(action, reward)
        rewards.append(reward)

    print("Final action values:", softmax_explorer.action_values)

"""#UCB1 Algorithm

The Upper Confidence Bound (UCB1) algorithm is used for exploration-exploitation trade-off by selecting actions based on upper confidence bounds of their estimated rewards.
"""

import random
import math

class UCB1:
    def __init__(self, num_actions):
        self.num_actions = num_actions
        self.action_counts = [0] * num_actions
        self.action_values = [0.0] * num_actions
        self.timestep = 0

    def choose_action(self):
        if 0 in self.action_counts:
            return self.action_counts.index(0)  # Choose unexplored action

        ucb_values = [value + math.sqrt(2 * math.log(self.timestep) / count) for value, count in zip(self.action_values, self.action_counts)]
        chosen_action = ucb_values.index(max(ucb_values))
        return chosen_action

    def update(self, action, reward):
        self.timestep += 1
        self.action_counts[action] += 1
        self.action_values[action] += (reward - self.action_values[action]) / self.action_counts[action]

if __name__ == "__main__":
    num_actions = 2

    ucb1 = UCB1(num_actions)

    num_steps = 1000
    rewards = []

    for _ in range(num_steps):
        action = ucb1.choose_action()
        reward = random.randint(0, 1)
        ucb1.update(action, reward)
        rewards.append(reward)

    print("Final action values:", ucb1.action_values)