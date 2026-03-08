import matplotlib.pyplot as plt

plt.ion()

def plot(scores, mean_scores):
    plt.figure(1)
    plt.clf()

    plt.title('Entrenamiento en curso...')
    plt.xlabel('Número de Juegos')
    plt.ylabel('Puntuación')

    plt.plot(scores, label='Puntuación', color='tab:blue')
    plt.plot(mean_scores, label='Media', color='tab:orange')
    plt.ylim(ymin=0)

    if scores:
        plt.text(len(scores)-1, scores[-1], str(scores[-1]))
        plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))

    plt.legend()

    plt.draw()
    plt.pause(0.01)
