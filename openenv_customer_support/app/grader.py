def grade_easy(pred, gt):
    return 1.0 if pred["cpu"] == gt["cpu"] else 0.0


def grade_medium(pred, gt):
    cpu_score = 1 - abs(pred["cpu"] - gt["cpu"]) / 10
    mem_score = 1 - abs(pred["memory"] - gt["memory"]) / 20

    return max(0.0, min(1.0, 0.5 * cpu_score + 0.5 * mem_score))


def grade_hard(pred, gt):
    cpu_error = abs(pred["cpu"] - gt["cpu"])
    mem_error = abs(pred["memory"] - gt["memory"])

    score = 1 - (0.1 * cpu_error + 0.05 * mem_error)
    return max(0.0, min(1.0, score))