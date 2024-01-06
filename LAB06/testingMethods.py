import gymnasium
import numpy as np
import matplotlib.pyplot as plt
from time import sleep


def getTaxiEnv(isRendering=False):
    if isRendering:
        return gymnasium.make("Taxi-v3", render_mode="human")
    return gymnasium.make("Taxi-v3")


def play(env, QTable, movLimit):
    for _ in range(100):
        state, _ = env.reset()
        for _ in range(movLimit):
            action = np.argmax(QTable[state])
            nextState, _, isFinished, _, _ = env.step(action)
            state = nextState
            sleep(0.5)
            if isFinished:
                break
    env.close()


def getMedianFromIntervals(rewards, interval):
    return [
        np.median(rewards[i : i + interval]) for i in range(0, len(rewards), interval)
    ]


def plt_rewards(
    rewards, xlabel, ylabel, title, scatterSize=2, isTrendAdded=True, isConnected=False
):
    x, y = zip(*enumerate(rewards, start=1))
    plt.scatter(x, y, s=scatterSize)
    if isTrendAdded:
        coefficients = np.polyfit(np.log(x), y, 1)
        trendline = np.poly1d(coefficients)
        plt.plot(
            x,
            trendline(np.log(x)),
            label="Trendline",
            linestyle="--",
            c="red",
            linewidth=2,
            alpha=0.6,
        )
    if isConnected:
        plt.plot(
            x,
            y,
            linestyle="--",
            c="grey",
            linewidth=2,
            alpha=0.6,
        )

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


# env = gymnasium.make("Taxi-v3")
# solver = QLearningSolver()
# QTable, rewards = solver.solve(env)
# for reward in rewards:
#     print(reward)
# env = gymnasium.make("Taxi-v3", render_mode="human")
# play(env, QTable, 1000)
