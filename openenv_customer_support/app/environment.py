import random
from openenv.core.env_server import Environment, Observation, Action


class ResourceEnv(Environment):
    def __init__(self):
        super().__init__()
        self.steps = 0
        self.max_steps = 1
        self.task = None

    def reset(self):
        self.steps = 0

        users = random.randint(50, 500)
        load = random.choice(["low", "medium", "high"])

        # Ground truth logic
        if load == "low":
            cpu, mem = 2, 4
        elif load == "medium":
            cpu, mem = 4, 8
        else:
            cpu, mem = 8, 16

        self.task = {
            "users": users,
            "load": load,
            "target_cpu": cpu,
            "target_mem": mem,
        }

        obs = f"Users: {users}, Load: {load}"

        return Observation(
            observation=obs,
            reward=0.0,
            done=False,
            info={}
        )

    def step(self, action: Action):
        self.steps += 1

        pred_cpu = int(action.data.get("cpu", 0))
        pred_mem = int(action.data.get("memory", 0))

        gt_cpu = self.task["target_cpu"]
        gt_mem = self.task["target_mem"]

        # ---- reward design (IMPORTANT) ----
        cpu_error = abs(pred_cpu - gt_cpu)
        mem_error = abs(pred_mem - gt_mem)

        score = 1.0 - (0.1 * cpu_error + 0.05 * mem_error)
        score = max(0.0, min(1.0, score))

        return Observation(
            observation="Evaluation complete",
            reward=score,
            done=True,
            info={
                "target_cpu": gt_cpu,
                "target_mem": gt_mem
            }
        )

    def state(self):
        return {
            "steps": self.steps
        }