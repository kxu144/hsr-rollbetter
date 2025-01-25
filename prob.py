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

def p(relic, target_stats: list):
    """
    target_stats is a list of desirable stats used to determine how well relics roll
    """

    main_stat = format_stat(relic['main_stat'])
    main_stat_prob = MAIN_STAT_PROBABILITIES[relic['type']][main_stat]

    subs = {}
    for sub in relic['sub_stats']:
        subs[format_stat(sub)] = sub['value']

    pass

def format_stat(stat):
    """
    stat has "name", "value" keys, return the name formatted with %
    """
    name = stat['name']
    if name in ['HP', 'ATK', 'DEF'] and stat['value'].endswith('%'):
        name += '%'
    return name


MAIN_STAT_PROBABILITIES = {
    'HEAD': {'HP': 1.0},
    'HAND': {'ATK': 1.0},
    'BODY': {'HP%': 0.2, 'ATK%': 0.2, 'DEF%': 0.2, 'Effect Hit Rate': 0.1, 'Outgoing Healing Boost': 0.1, 'CRIT Rate': 0.1, 'CRIT DMG': 0.1},
    'FOOT': {'HP%': 0.28, 'ATK%': 0.3, 'DEF%': 0.3, 'SPD': 0.12},
    'ORB': {'HP%': 0.12, 'ATK%': 0.13, 'DEF%': 0.12, 'Physical DMG Boost': 0.09, 'Fire DMG Boost': 0.09, 'Ice DMG Boost': 0.09, 'Wind DMG Boost': 0.09, 'Lightning DMG Boost': 0.09, 'Quantum DMG Boost': 0.09, 'Imaginary DMG Boost': 0.09},
    'ROPE': {'HP%': 0.26, 'ATK%': 0.27, 'DEF%': 0.24, 'Break Effect': 0.16, 'Energy Regeneration Rate': 0.05},
}