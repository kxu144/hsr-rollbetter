from itertools import permutations

def p(relic, target_stats: dict):
    """
    target_stats is a list of desirable stats used to determine how well relics roll
    """

    main_stat = format_stat(relic['main_stat'])
    main_stat_prob = MAIN_STAT_PROBABILITIES[relic['type']][main_stat]

    sub_dict = {}
    for sub in relic['sub_stats']:
        sub_dict[format_stat(sub)] = sub['value']

    substat_prob = prob_substat(main_stat, list(sub_dict.keys()), target_stats)
        
    pass

def prob_substat(main_stat, subs, target_stats):
    """
    finds probability of rolling a piece equal or better than the current subs
    """
    pool = [k for k in SUBSTAT_WEIGHTS if k != main_stat]
    all_permutations = permutations(pool, 4)
    
    weight = sum(SUBSTAT_WEIGHTS.values()) - SUBSTAT_WEIGHTS.get(main_stat, 0)
    score = sum(target_stats.get(s, 0) for s in subs)

    total_prob = 0
    for a, b, c, d in all_permutations:
        if score > target_stats.get(a, 0) + target_stats.get(b, 0) + target_stats.get(c, 0) + target_stats.get(d, 0):
            continue
        prob = SUBSTAT_WEIGHTS[a] * SUBSTAT_WEIGHTS[b] * SUBSTAT_WEIGHTS[c] * SUBSTAT_WEIGHTS[d]
        prob /= weight * (weight - SUBSTAT_WEIGHTS[a]) * (weight - SUBSTAT_WEIGHTS[a] - SUBSTAT_WEIGHTS[b]) * (weight - SUBSTAT_WEIGHTS[a] - SUBSTAT_WEIGHTS[b] - SUBSTAT_WEIGHTS[c])
        total_prob += prob
    
    return total_prob

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
    prob = prob_substat('HP', ['CRIT Rate', 'ATK', 'CRIT DMG', 'DEF'], {'CRIT Rate': 100, 'CRIT DMG': 100, 'ATK%': 10, 'ATK': 1})
    print(prob)