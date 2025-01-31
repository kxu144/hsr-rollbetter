import gymnasium as gym
import numpy as np

class RelicEnv(gym.Env):

    def __init__(self, TOTAL_EXP=10):
        # Define action space: 0 = Trash, 1 = Upgrade
        self.action_space = gym.spaces.Discrete(2)

        # Observation space:
        # - 4 relic stats (0.0 to 1.0), -1.0 if empty stat
        # - Upgrade level (0 to 5)
        # - Exp used (unbounded, stored as float)
        # - Best kept score (float)
        self.observation_space = gym.spaces.Box(
            low=np.array([-1.0] * 4 + [0, 0.0, 0.0]),
            high=np.array([1.0] * 4 + [5, np.inf, np.inf]),
            dtype=np.float32
        )
        
        self.total_exp = TOTAL_EXP

    def reset(self, seed=None):
        if seed:
            np.random.seed(seed)

        self._get_relic(seed=seed)
        self.exp_left = self.total_exp
        self.best_score = 0.0
        
        self.kept_pieces = []
        
        return self._get_obs(), {'substats': self.substat_dict}
    
    def _get_relic(self, seed=None):
        p_norm = np.array(list(SUBSTAT_WEIGHTS.values()))
        p_norm = p_norm / sum(p_norm)
        if np.random.rand() < 0.2:
            relic_stats = np.random.choice(list(SUBSTAT_WEIGHTS.keys()), 4, p=p_norm, replace=False)
        else:
            relic_stats = np.random.choice(list(SUBSTAT_WEIGHTS.keys()), 3, p=p_norm, replace=False)
        self.substat_dict = {sub: 0 for sub in relic_stats}

        self.relic_scores = np.array([SUBSTAT_SCORES[sub] for sub in relic_stats])
        if len(self.relic_scores) == 3:
            self.relic_scores = np.append(self.relic_scores, -1.0)

        self.relic_level = 0

    def _get_obs(self):
        return np.array([
            *self.relic_scores,
            self.relic_level,
            self.exp_left,
            self.best_score
        ], dtype=np.float32)

    def step(self, action):
        done = False
        reward = 0

        if action == 0: #Trash relic
            reward = -0.01
            self.exp_left += RELIC_EXP_COST[self.relic_level] * 0.8
            self._get_relic()
        
        elif action == 1: #Upgrade relic
            if self.relic_level < 15:
                exp_cost = RELIC_EXP_COST[self.relic_level + 3] - RELIC_EXP_COST[self.relic_level]
                if self.exp_left >= exp_cost:
                    self.relic_level += 3
                    self.exp_left -= exp_cost

                    if len(self.substat_dict) == 4: #Upgrade stat
                        substat_ind = np.random.randint(sum(self.relic_scores >= 0.0))
                        substat_name = list(self.substat_dict.keys())[substat_ind]
                        assert self.relic_scores[substat_ind] >= 0.0
                        self.relic_scores[substat_ind] += SUBSTAT_SCORES[substat_name]
                        self.substat_dict[substat_name] += 1

                    else: #Add new substat
                        assert len(self.substat_dict) == 3
                        assert self.relic_scores[-1] == -1.0
                        new_weights = {k: v for k, v in SUBSTAT_WEIGHTS.items() if k not in self.substat_dict}
                        p_norm = np.array(list(new_weights.values()))
                        p_norm = p_norm / sum(p_norm)
                        new_stat = np.random.choice(list(new_weights.keys()), 1, p=p_norm)[0]
                        self.substat_dict[new_stat] = 0
                        self.relic_scores[-1] = SUBSTAT_SCORES[new_stat]

                else: #Cannot afford relic, illegal action
                    reward = -1
                    self.exp_left += RELIC_EXP_COST[self.relic_level] * 0.8
                    self._get_relic()
            
            else: #Keep relic
                assert self.relic_level == 15
                assert len(self.substat_dict) == 4
                assert sum(self.relic_scores >= 0.0) == 4

                relic_score = sum(self.relic_scores)
                if relic_score > self.best_score:
                    self.best_score = relic_score
                    self.kept_pieces.append(self.substat_dict)

                reward = np.exp(relic_score - self.best_score)
                self._get_relic()

        # end when cannot upgrade any
        if self.exp_left < RELIC_EXP_COST[3]:
            done = True

        return self._get_obs(), reward, done, False, {}
    
    def render(self):
        substat_dict = {str(k): v for k, v in self.substat_dict.items()}
        print(f'Level {self.relic_level} subs: {substat_dict}\nExp left: {self.exp_left} Best score: {self.best_score}')



SUBSTAT_SCORES = {
    'HP': 0,
    'ATK': 1/4,
    'DEF': 0,
    'HP%': 0,
    'ATK%': 2/3,
    'DEF%': 0,
    'SPD': 0,
    'CRIT Rate': 1,
    'CRIT DMG': 1,
    'Effect Hit Rate': 0,
    'Effect RES': 0,
    'Break Effect': 0
}

SUBSTAT_WEIGHTS = {
    'HP': 10,
    'ATK': 10,
    'DEF': 10,
    'HP%': 10,
    'ATK%': 10,
    'DEF%': 10,
    'SPD': 4,
    'CRIT Rate': 6,
    'CRIT DMG': 6,
    'Effect Hit Rate': 8,
    'Effect RES': 8,
    'Break Effect': 8
}

RELIC_EXP_COST = {
    0: 0,
    3: 2400 / 76000,
    6: 7500 / 76000,
    9: 17500 / 76000,
    12: 37000 / 76000,
    15: 76000 / 76000
}





if __name__ == '__main__':
    env = RelicEnv()
    ob, _ = env.reset()
    while True:
        env.render()
        ac = int(input())
        ob, reward, done, _, _ = env.step(ac)
        print(f'Reward: {reward}')
        if done:
            break

