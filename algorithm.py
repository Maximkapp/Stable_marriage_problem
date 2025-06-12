def gale_shapley(men_preferences, women_preferences):
    n = len(men_preferences)
    free_men = list(men_preferences.keys())
    engaged = {}
    women_partners = {woman: None for woman in women_preferences}

    women_rankings = {
        woman: {man: rank for rank, man in enumerate(prefs)}
        for woman, prefs in women_preferences.items()
    }

    while free_men:
        man = free_men.pop(0)
        for woman in men_preferences[man]:
            current = women_partners[woman]
            if current is None:
                engaged[man] = woman
                women_partners[woman] = man
                break
            elif women_rankings[woman][man] < women_rankings[woman][current]:
                free_men.append(current)
                engaged.pop(current)
                engaged[man] = woman
                women_partners[woman] = man
                break
    return engaged
