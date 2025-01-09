import numpy as np
import random


class QLearningSolver:
    def __init__(
        self,
        itMax=10000,
        stepsMax=100,
        startLR=0.5,
        minLR=0.1,
        startEps=0.5,
        minEps=0.05,
        decayEps=0.01,
        gamma=0.9,
        decayFactor=0.001,
        expInterval=50,
        expItMax=5,
    ):
        self.itMax = itMax
        self.stepsMax = stepsMax
        self.startLR = startLR
        self.minLR = minLR
        self.startEps = startEps
        self.minEps = minEps
        self.decayEps = decayEps
        self.gamma = gamma
        self.decayFactor = decayFactor
        self.expInterval = expInterval
        self.expItMax = expItMax

    def solve(self, env):
        QTable = np.zeros((env.observation_space.n, env.action_space.n))
        expRate = self.startEps
        learningRate = self.startLR
        rewards = []
        expRewards = []
        for i in range(self.itMax):
            state, _ = env.reset()
            rewardSum = 0
            isExp = i % self.expInterval < self.expItMax
            for _ in range(self.stepsMax):
                if random.uniform(0, 1) < expRate and not isExp:
                    action = env.action_space.sample()
                else:
                    action = np.argmax(QTable[state])

                nextState, reward, isFinished, _, _ = env.step(action)
                rewardSum += reward
                QTable[state][action] = QTable[state][action] + learningRate * (
                    reward
                    + self.gamma * np.max(QTable[nextState] - QTable[state][action])
                )
                state = nextState

                if isFinished:
                    break
            if isExp:
                expRewards.append(rewardSum)
            else:
                expRate = max(self.minEps, self.startEps * np.exp(-self.decayEps * i))
            learningRate = max(self.minLR, learningRate * self.decayFactor)
            rewards.append(rewardSum)

        return QTable, rewards, expRewards
