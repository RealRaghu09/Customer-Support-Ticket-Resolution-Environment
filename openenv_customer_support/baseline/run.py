import os
import requests
import json
import google.generativeai as genai

BASE_URL = "http://localhost:8000"

api_key = os.getenv("HF_TOKEN")

if not api_key:
    raise ValueError("HF_TOKEN not set. Please configure environment variables.")

genai.configure(api_key=api_key)


def get_action(obs):
    prompt = f"""
You are a system optimizer.

Input:
{obs}

Task:
Predict CPU and memory needed.

Rules:
- low → cpu 2, mem 4
- medium → cpu 4, mem 8
- high → cpu 8, mem 16

Return ONLY JSON:
{{"cpu": int, "memory": int}}
"""

    try:
        response = model.generate_content(prompt)
        text = response.text

        # ---- safe parsing ----
        try:
            parsed = json.loads(text)
            return {
                "cpu": int(parsed.get("cpu", 4)),
                "memory": int(parsed.get("memory", 8))
            }
        except:
            return fallback(obs)

    except Exception as e:
        print("Gemini Error:", e)
        return fallback(obs)


def fallback(obs):
    obs = obs.lower()

    if "high" in obs:
        return {"cpu": 8, "memory": 16}
    elif "medium" in obs:
        return {"cpu": 4, "memory": 8}
    else:
        return {"cpu": 2, "memory": 4}


def run_episode():
    res = requests.post(f"{BASE_URL}/reset").json()
    obs = res["observation"]

    action = get_action(obs)

    step = requests.post(
        f"{BASE_URL}/step",
        json={"data": action}
    ).json()

    return step["reward"]


if __name__ == "__main__":
    scores = []

    for _ in range(10):
        scores.append(run_episode())

    print("Average Score:", sum(scores) / len(scores))