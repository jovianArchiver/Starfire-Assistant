# Calculates the GPV for a given population.
def calculate_gpv(pu, hi, rei, iu, tl):
    multiplier_hi = {'Benign': 1.0, 'Harsh': 1.0, 'Hostile': 1.0, 'Desolate': 0.7, 'Extreme': 0.6}
    multiplier_rei = {'V.Poor': 0.5, 'Poor': 0.75, 'Normal': 1.0, 'Rich': 1.25, 'V.Rich': 1.5}
    multiplier_tl = {'pre-ind': 0.3, 'ind1': 0.6, 'ind2': 0.9, 'ht1': 1.1, 'ht2': 1.2, 'ht3': 1.3, 'ht4': 1.4,
                     'ht5': 1.5, 'ht6': 1.6, 'ht7': 1.7, 'ht8': 1.8, 'ht9': 1.9, 'ht10': 2.0, 'ht11': 2.1, 'ht12': 2.2,
                     'ht13': 2.3, 'ht14': 2.4, 'ht15': 2.5, 'ht16': 2.6, 'ht17': 2.7, 'ht18': 2.8, 'ht19': 2.9}

    result = (pu * multiplier_hi[hi] * multiplier_rei[rei] + iu) * multiplier_tl[tl]
    return result


# Returns the discovered status for a system, to be appended to the localization list for the civilization
def generate_star_discovery_dict(star):
    output = []
    planets = star['planets']

    for n in range(0, len(planets)):
        output.append({'name': False, 'explored': False, 'population': False, 'moons': []})

        if not planets[n]['moons']:
            output[n]['moons'] = False
        else:
            for m in range(0, len(output[n]['moons'])):
                output[n]['moons'].append({'name': False, 'explored': False, 'population': False})

    return output


# Returns the habitability value of a certain planet for a certain civilization
def calculate_hab(planet, hi):
    if planet['type'] == 'T':
        difference = abs(planet['hi'] - hi)

        if difference <= 2:
            return 'Benign'
        else:
            return 'Harsh'
    elif planet['type'] == 'ST':
        return 'Hostile'

    elif planet['type'] == 'O2':
        return 'Desolate'

    else:
        return 'Extreme'


# Returns the dictionary of a non-existent population
def generate_empty_population(pu, planet, hi, iu=0):
    population = {'pu': pu, 'iu': iu, 'hab': calculate_hab(planet, hi), 'gpv': 0}

    return population


