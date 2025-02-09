from itertools import permutations, product
import math

def p(relic, target_stats: dict):
    """
    target_stats is a list of desirable stats used to determine how well relics roll
    returns probability of relic main stat, probability of getting substats to roll at least the current score, and 
    SUBSTAT_VALUE, a dict mapping substat combinations to substat probabilities.

    need to multiply main_stat_prob to substat_prob and SUBSTAT_VALUE.
    """

    main_stat = format_stat(relic['main_stat'])
    main_stat_prob = MAIN_STAT_PROBABILITIES[relic['type']][main_stat]

    sub_dict = {}
    for sub in relic['sub_stats']:
        sub_dict[format_stat(sub)] = float(sub['value'].strip('%'))

    roll_score = sum(sub_dict[s] / SUBSTAT_MAX_ROLL[s] * target_stats[s] for s in target_stats if s in sub_dict)
    substat_prob, SUBSTAT_VALUE = prob_substat(main_stat, list(sub_dict.keys()), target_stats, roll_score)
    
    return main_stat_prob, substat_prob, SUBSTAT_VALUE

def prob_substat(main_stat, subs, target_stats, target_score, prob_4liner=0.2):
    """
    finds probability of rolling a piece equal or better than the current subs
    """
    pool = [k for k in SUBSTAT_WEIGHTS if k != main_stat]
    all_permutations = permutations(pool, 4)
    
    weight = sum(SUBSTAT_WEIGHTS.values()) - SUBSTAT_WEIGHTS.get(main_stat, 0)
    substat_score = sum(target_stats.get(s, 0) for s in subs)

    total_prob = 0
    SUBSTAT_VALUE = {}
    for a, b, c, d in all_permutations:
        sub_score = [target_stats.get(e, 0) for e in (a, b, c, d)]
        unrolled_score = sum(sub_score)
        if substat_score > unrolled_score:
            continue
        
        substat_prob = SUBSTAT_WEIGHTS[a] * SUBSTAT_WEIGHTS[b] * SUBSTAT_WEIGHTS[c] * SUBSTAT_WEIGHTS[d]
        substat_prob /= weight * (weight - SUBSTAT_WEIGHTS[a]) * (weight - SUBSTAT_WEIGHTS[a] - SUBSTAT_WEIGHTS[b]) * (weight - SUBSTAT_WEIGHTS[a] - SUBSTAT_WEIGHTS[b] - SUBSTAT_WEIGHTS[c])

        if target_score:
            roll_prob = 0
            for aw, bw, cw, dw in distributions(4):
                if target_score - unrolled_score > aw * sub_score[0] + bw * sub_score[1] + cw * sub_score[2] + dw * sub_score[3]:
                    continue
                dist_weight = math.factorial(4) / (4**4 * math.factorial(aw) * math.factorial(bw) * math.factorial(cw) * math.factorial(dw))
                roll_prob += dist_weight * (1 - prob_4liner)
            for aw, bw, cw, dw in distributions(5):
                if target_score - unrolled_score > aw * sub_score[0] + bw * sub_score[1] + cw * sub_score[2] + dw * sub_score[3]:
                    continue
                dist_weight = math.factorial(5) / (4**5 * math.factorial(aw) * math.factorial(bw) * math.factorial(cw) * math.factorial(dw))
                roll_prob += dist_weight * prob_4liner
        else:
            roll_prob = 1

        comb_prob = substat_prob * roll_prob
        SUBSTAT_VALUE[frozenset((a, b, c, d))] = comb_prob

        total_prob += comb_prob
    
    return total_prob, SUBSTAT_VALUE

def distributions(total, size=4):
    for comb in product(range(total + 1), repeat=size):
        if sum(comb) == total:
            yield comb

def format_stat(stat):
    """
    stat has "name", "value" keys, return the name formatted with %
    """
    name = stat['name']
    if name in ['HP', 'ATK', 'DEF'] and stat['value'].endswith('%'):
        name += '%'
    return name

SUBSTAT_WEIGHTS = {
    'HP': 10,
    'ATK': 10,
    'DEF': 10,
    'HP%': 10,
    'ATK%': 10,
    'DEF%': 10,
    'SPD': 4,
    'CRIT Rate': 6,
    'CRIT DMG': 6,
    'Effect Hit Rate': 8,
    'Effect RES': 8,
    'Break Effect': 8
}

SUBSTAT_MAX_ROLL = {
    'HP': 42,
    'ATK': 21,
    'DEF': 21,
    'HP%': 4.3,
    'ATK%': 4.3,
    'DEF%': 5.4,
    'SPD': 2.6,
    'CRIT Rate': 3.2,
    'CRIT DMG': 6.4,
    'Effect Hit Rate': 4.3,
    'Effect RES': 4.3,
    'Break Effect': 6.4
}

MAIN_STAT_PROBABILITIES = {
    'HEAD': {'HP': 1.0},
    'HAND': {'ATK': 1.0},
    'BODY': {'HP%': 0.2, 'ATK%': 0.2, 'DEF%': 0.2, 'Effect Hit Rate': 0.1, 'Outgoing Healing Boost': 0.1, 'CRIT Rate': 0.1, 'CRIT DMG': 0.1},
    'FOOT': {'HP%': 0.28, 'ATK%': 0.3, 'DEF%': 0.3, 'SPD': 0.12},
    'ORB': {'HP%': 0.12, 'ATK%': 0.13, 'DEF%': 0.12, 'Physical DMG Boost': 0.09, 'Fire DMG Boost': 0.09, 'Ice DMG Boost': 0.09, 'Wind DMG Boost': 0.09, 'Lightning DMG Boost': 0.09, 'Quantum DMG Boost': 0.09, 'Imaginary DMG Boost': 0.09},
    'ROPE': {'HP%': 0.26, 'ATK%': 0.27, 'DEF%': 0.24, 'Break Effect': 0.16, 'Energy Regeneration Rate': 0.05},
}




if __name__ == '__main__':
    # debug
    prob, d = prob_substat('CRIT DMG', ['SPD'], {'SPD': 1,}, 6.9/2.6)
    print(prob)