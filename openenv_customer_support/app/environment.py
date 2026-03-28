import random
from openenv.core.env_server import Environment , Action , Observation

class GuessNumberEnv(Environment):
    def __init__(self):
        super().__init__()
        self.target = None
        self.steps = 0
        self.max_steps = 10

    # Reset environment
    def reset(self):
        self.target = random.randint(1, 100)
        self.steps = 0

        return Observation(
            observation="Game started! Guess number between 1-100",
            reward=0,
            done=False,
            info={}
        )

    # Step function
    def step(self, action: Action):
        guess = int(action.data)
        self.steps += 1

        if guess == self.target:
            return Observation(
                observation="Correct!",
                reward=10,
                done=True,
                info={"target": self.target}
            )

        elif self.steps >= self.max_steps:
            return Observation(
                observation=f"Game Over! Target was {self.target}",
                reward=-10,
                done=True,
                info={}
            )

        elif guess < self.target:
            return Observation(
                observation="Too low",
                reward=-1,
                done=False,
                info={}
            )

        else:
            return Observation(
                observation="Too high",
                reward=-1,
                done=False,
                info={}
            )

    # Optional: full state
    def state(self):
        return {
            "steps": self.steps,
            "max_steps": self.max_steps
        }