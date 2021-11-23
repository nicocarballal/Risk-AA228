import numpy as np

def compute_attack_successes(max_attackers, max_defenders):
    probs = np.zeros((max_attackers + 1, max_defenders + 1))
    for i in range(max_attackers + 1):
        for j in range(max_defenders + 1):
            probs[i][j] = compute_attack_successes_helper(i, j, probs)
    return probs

# assumes that both attacker and defender roll the maximum number of dice possible, which I believe is optimal
# https://web.stanford.edu/~guertin/risk.notes.html for roll probabilities
# https://riskodds.com/ for simulated win probabilities, they are close to matching
def compute_attack_successes_helper(num_attackers, num_defenders, probs):
    if probs[num_attackers][num_defenders] != 0:
        return probs[num_attackers][num_defenders]
    if num_attackers == 0 or num_attackers == 1:
        probs[num_attackers][num_defenders] = 0
    if num_defenders == 0:
        probs[num_attackers][num_defenders] = 1
    if num_attackers == 2 and num_defenders == 1:
        probs[num_attackers][num_defenders] = (5/12) * compute_attack_successes_helper(num_attackers, num_defenders - 1, probs) + (7/12) * compute_attack_successes_helper(num_attackers - 1, num_defenders, probs)
    if num_attackers == 3 and num_defenders == 1:
        probs[num_attackers][num_defenders] = (125/216) * compute_attack_successes_helper(num_attackers, num_defenders - 1, probs) + (91/216) * compute_attack_successes_helper(num_attackers - 1, num_defenders, probs)
    if num_attackers > 3 and num_defenders == 1:
        probs[num_attackers][num_defenders] = (95/144) * compute_attack_successes_helper(num_attackers, num_defenders - 1, probs) + (49/144) * compute_attack_successes_helper(num_attackers - 1, num_defenders, probs)
    if num_attackers == 2 and num_defenders > 1:
        probs[num_attackers][num_defenders] = (55/216) * compute_attack_successes_helper(num_attackers, num_defenders - 1, probs) + (161/216) * compute_attack_successes_helper(num_attackers - 1, num_defenders, probs)
    if num_attackers == 3 and num_defenders > 1:
        probs[num_attackers][num_defenders] = (295/1296) * compute_attack_successes_helper(num_attackers, num_defenders - 2, probs) + (35/108) * compute_attack_successes_helper(num_attackers - 1, num_defenders - 1, probs) + (581/1296) * compute_attack_successes_helper(num_attackers - 2, num_defenders, probs)
    if num_attackers > 3 and num_defenders > 1:
        probs[num_attackers][num_defenders] = (1445/3888) * compute_attack_successes_helper(num_attackers, num_defenders - 2, probs) + (2611/7776) * compute_attack_successes_helper(num_attackers - 1, num_defenders - 1, probs) + (2275/7776) * compute_attack_successes_helper(num_attackers - 2, num_defenders, probs)
    return probs[num_attackers][num_defenders]

if __name__ == '__main__':
    probs = compute_attack_successes(100, 100)
    np.savetxt('probs.out', probs, delimiter=',')


