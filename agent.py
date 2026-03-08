import random
import numpy as np

class Agent:
    def __init__(self):
        self.n_games=0
        self.epsilon=1.0
        self.epsilon_min=0.01
        self.epsilon_decay = 0.98
        self.gamma=0.6
        self.alpha=0.01
        self.q_table={}


    def get_state(self, game):
        head=game.head

        point_l = [head[0] - 10, head[1]]
        point_r = [head[0] + 10, head[1]]
        point_u = [head[0], head[1] - 10]
        point_d = [head[0], head[1] + 10]

        dir_l = game.direction == 'LEFT'
        dir_r = game.direction == 'RIGHT'
        dir_u = game.direction == 'UP'
        dir_d = game.direction == 'DOWN'

        state=[
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),

            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),

            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),


            dir_l, dir_r, dir_u, dir_d,

            game.food[0] < game.head[0],
            game.food[0] > game.head[0],
            game.food[1] < game.head[1],
            game.food[1] > game.head[1]
            ]
        return tuple(np.array(state, dtype=int))

    def get_action(self, state):
        final_move=[0,0,0]

        if random.random() < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            if state not in self.q_table:
                self.q_table[state] = [0.0, 0.0, 0.0]
            move = np.argmax(self.q_table[state])
            final_move[move] = 1

        return final_move


    def train_short_memory(self, state, action, reward, next_state, done):
        if state not in self.q_table:
            self.q_table[state]=[0.0, 0.0, 0.0]
        if next_state not in self.q_table:
            self.q_table[next_state]=[0.0, 0.0, 0.0]

        action_idx=np.argmax(action)

        old_q=self.q_table[state][action_idx]
        next_max=np.max(self.q_table[next_state])

        if done:
            target=reward
        else:
            target=reward+self.gamma*next_max
        self.q_table[state][action_idx] = old_q + self.alpha * (target - old_q)

