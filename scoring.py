def calculate_scores(answers, category_names):
    scores = {}
    for i, category in enumerate(category_names):
        score = 0
        if answers[i * 2].startswith("A"):
            score += 1
        if answers[i * 2 + 1].startswith("A"):
            score += 1
        scores[category] = score
    return scores
