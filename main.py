from agent import Agent
from environment import SnakeGameAI
from helper import plot



def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()

    print("--- Iniciando Entrenamiento de Snake AI ---")

    while True:
        if agent.n_games==1000:
            agent.alpha=0.001

        state_old = agent.get_state(game)

        final_move = agent.get_action(state_old)

        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)


        if done:
            game.reset()
            agent.n_games += 1
            if agent.epsilon > agent.epsilon_min:
                agent.epsilon *= agent.epsilon_decay

            if score > record:
                record = score

            if agent.n_games%10==0:
                print(f'Juego: {agent.n_games} | Score: {score} | Récord: {record}')

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            if agent.n_games%10==0:
                plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()
