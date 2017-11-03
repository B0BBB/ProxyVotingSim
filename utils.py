from itertools import combinations
from random import randint, uniform


# Kendell's Tao distance between vector v and u
def kendall_tau(v, u):
    pairs = combinations(v, 2)
    dist = 0
    for x, y in pairs:
        a = v.index(x) - v.index(y)
        b = u.index(x) - u.index(y)
        # if discordant (different signs)
        if a * b < 0:
            dist += 1
    return dist


# Borda voting rule, will give a score to each option according to its rank, and will return a final result
# In order to avoid ties, we've added uniform noise to each score
def borda_voting_rule(ballots, a):
    scores = {}
    for i in range(a):
        scores[i] = uniform(0, 0.01)
    for voter in ballots:
        for i in range(a):
            scores[voter.get_vote()[i]] += a - 1 - i
    return sorted(scores, key=scores.__getitem__, reverse=True)


# Boyer Moore majority vote algorithm, tie will be {0,1} randomly
# returns a single vector {0,1} of size k
def bm_majority_vote(ballots, k):
    result = []
    for i in range(k):
        m = None
        count = 0
        for agent in ballots:
            if count == 0:
                m = agent.get_vote()[i]
                count = 1
            elif m == agent.get_vote()[i]:
                count += 1
            else:
                count -= 1
        if count > 0:
            result.append(m)
        elif count < 0:
            result.append(abs(1 - m))
        else:
            result.append(randint(0, 1))
    return result
