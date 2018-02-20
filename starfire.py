import random, math, os, json



# Used for generating bearings. Returns an integer.
def generate_bearing():
    return random.randint(1, 12)

# Used for generating facings. Returns an integer.
def generate_facing():
    return random.randint(1,6)

# Generates the type of solar system. Returns a string.
def generate_type_system():
    x = random.randint(2,100)

    if x == 1:
        systemtype = 'Black Hole'
    elif x >= 2 and x <= 10:
        systemtype = 'Starless Nexus'
    elif x >= 11 and x <= 45:
        systemtype = 'Binary Star System'
    else:
        systemtype = 'Unary Star System'

    return systemtype

# Generates the type of star. Returns a string.
def generate_type_star():
    x = random.randint(1,100)
    if x <= 5:
        startype = 'Blue Giant'
    elif x > 5 and x <= 16:
        startype = 'White Star'
    elif x > 16 and x <= 41:
        startype = 'Yellow Star'
    elif x > 41 and x <= 66:
        startype = 'Orange Star'
    elif x > 66 and x <= 85:
        startype = 'Red Star'
    elif x > 85 and x <= 95:
        startype = 'Red Dwarf'
    elif x > 95 and x <= 98:
        startype = 'White Dwarf'
    else:
        startype = 'Red Giant'

    return startype

# Generates the mass of a planet. Returns a string.
def generate_type_mass():
    roll = random.randint(1, 20)

    if roll <= 5:
        mass = 'M1'
    elif roll > 5 and roll <= 17:
        mass = 'M2'
    else:
        mass = 'M3'

    return mass

# Generates the type of a planet for a given star and distance. Returns [type, mass, tidally locked].
def generate_type_planet(star, orbit):
    table = {'White Star':[10, 18, 25, 130, 8], 'Yellow Star':[6, 12, 16, 83, 4], 'Orange Star':[3, 5, 9, 38, 3], 'Red Star':[3, 4, 5, 18, 3], 'Red Dwarf':[0, 0, 3, 11, 2]}
    mass = generate_type_mass()

    if orbit <= table[star][2]:
        if orbit < table[star][0]:
            if mass == 'M1':
                planet_type = '01'
            else:
                planet_type = 'V'
        if orbit >= table[star][0] and orbit <= table[star][1]:
            if mass == 'M1':
                planet_type = 'O2'
            elif mass == 'M2':
                planet_type = 'T'
            else:
                planet_type = 'ST'
        if orbit > table[star][1]:
            planet_type = 'O2'
    elif orbit > table[star][2] and orbit <= table[star][3]:
        planet_type = 'G'
        mass = None
    elif orbit > table[star][3]:
        planet_type = 'I'
        mass = None

    planetclass = [planet_type, mass, False]
    if orbit <= table[star][4]:
        planetclass[2] = True

    return planetclass

# Generates the type of a moon. Returns a string.
def generate_type_moon(planet):
    if planet == 'I':
        return 'O1'
    else:
        return 'O2'

# Generates the distance for binary stars. Returns an integer.
def generate_distance_binary():
    x = random.randint(1,4)
    z = random.randint(1,100)

    if x == 1:
        y = 50
    elif x == 2:
        y = 150
    else:
        y = 250

    y += z
    return z

# Generates the REI for a given planet. Returns an integer.
def generate_rei(planet):
    roll = random.randint(1,10)

    if planet == '02':
        roll += 3
    elif planet == 'O1':
        roll += 5
    elif planet in ['V', 'G', 'I']:
        return None

    if roll == 1:
        rei = 'V.Poor'
    elif roll in [2, 3]:
        rei = 'Poor'
    elif roll in [4, 5, 6, 7]:
        rei = 'Normal'
    elif roll in [8, 9]:
        rei = 'Rich'
    else:
        rei = 'V.Rich'

    return rei

# Generates the orbits of the planets for a given star. Returns a list.
def generate_orbits_planets(star, binary = None):
    orbits=[]
    orbits.append(random.randint(1,8))
    orbits.append(random.randint(orbits[0]+2,10))
    difference = orbits[1]-orbits[0]

    if binary != None:
        maxdist = binary
    else:
        if star == 'White Star' or star == 'Yellow Star':
            maxdist = 300
        elif star == 'Orange Star':
            maxdist = 250
        else:
            maxdist = 200

    while orbits[-1] < maxdist:
        orbits.append(orbits[-1]+difference*pow(2, len(orbits)-2))

    del orbits[-1]
    return orbits

# Generates the orbits of the moons for a given planet. Returns a list.
def generate_orbits_moons(planet, number):
    orbits = []

    while len(orbits) < number:
        if planet == 'G':
            x = random.randint(1,10)

        elif planet == 'I':
            x = random.randint(1,10)/2.0
            x = math.ceil(x)

        elif planet in ['O2', 'T', 'ST']:
            x = int(random.randint(1,10)/2)
            if x == 0:
                x = 1

        if x not in orbits:
            orbits.append(x)

    orbits.sort()
    return orbits

# Generates the number of moons for a given planet. Returns an integer.
def generate_number_moons(planet, mass):
    roll = random.randint(1,100)

    if planet not in ['G', 'I']:
        if planet == 'V' or mass == 'M1':
            return None
        elif mass == 'M2':
            roll += -10

    elif planet == 'G':
        roll += 50
    elif planet == 'I':
        roll += 35

    if roll < 56:
        return 1
    elif roll >= 56 and roll < 86:
        return 2
    elif roll >= 86 and roll < 106:
        return 3
    elif roll >= 106 and roll < 127:
        return 4
    elif roll >= 127:
        return 5

# Generates the moons that orbit a given planet. Returns a list.
def generate_list_moons(planet, mass):
    number = generate_number_moons(planet, mass)
    if number == None:
        return None

    moon_orbits = generate_orbits_moons(planet, number)
    moon_type = generate_type_moon(planet)
    moon_list = []

    for moon in moon_orbits:
        moon_list.append({'orbit': moon, 'bearing': generate_facing(), 'type': moon_type, "rei": generate_rei(moon_type)})

    return moon_list

# Generates the planets that orbit a given star. If distance_binary is an integer, creates the planets as orbiting a component in a binary, given the distance. Returns a dictionary.
def generate_list_planets(star, binary = None):
    if star in ['Blue Giant', 'White Dwarf', 'Red Giant']:
        return None

    planets = []

    planet_orbits = generate_orbits_planets(star, binary)

    for planet in range(0, len(planet_orbits)):
        planet_class = generate_type_planet(star, planet_orbits[planet])
        planet_type = planet_class[0]
        planet_mass = planet_class[1]
        moon_list = generate_list_moons(planet_type, planet_mass)

        if binary != None and planet_orbits[planet] >= binary/3:
            planets.append({'orbit': planet_orbits[planet], 'bearing': 'N/A', 'type': 'AS', 'rei': generate_rei('O2'), 'tide_lock': False, 'moons': None})
        else:
            planets.append({'orbit': planet_orbits[planet], 'bearing': generate_bearing(), 'type': planet_type, 'rei': generate_rei(planet_type), 'tide_lock': False, 'moons': generate_list_moons(planet_type, planet_mass)})

    for p in range(len(planets)-1, 1, -1):
        if planets[p]['type'] == 'G' and random.randint(1, 10) < 7:
            planets[p-1] = {'orbit': planet_orbits[p-1], 'bearing': 'N/A', 'type': 'AS', 'rei': generate_rei('O2'), 'tide_lock': False, 'moons': None}

    return planets


# Generates an entire solar system, given a name or id. Returns a dictionary.
def generate_solar_system(number):
    system = {'systemtype': generate_type_system(), 'name': number, 'primary': None, 'binary': None, 'distance': None}

    if system['systemtype'] == 'Binary Star System':
        startype = generate_type_star()
        system['distance'] = generate_distance_binary()

        system['binary'] = {'startype': startype, 'planets': generate_list_planets(startype, system['distance'])}

    else:
        del system['binary']

    if system['systemtype'] in ['Unary Star System','Binary Star System']:
        startype = generate_type_star()

        system['primary'] = {'startype': startype, 'planets': generate_list_planets(startype, system['distance'])}

        del system['distance']
    else:
        del system['primary']

    return system

# Calculates the GPV for a given population.
def calculate_gpv(pu, hi, rei, iu, tl):
    multiplier_hi = {'Benign': 1.0, 'Harsh': 1.0, 'Hostile': 1.0, 'Desolate': 0.7, 'Extreme': 0.6}
    multiplier_rei = {'Very Poor': 0.5, 'Poor': 0.75, 'Normal': 1.0, 'Rich': 1.25, 'Very Rich': 1.5}
    multiplier_tl = {'pre-ind': 0.3, 'ind1': 0.6, 'ind2': 0.9, 'ht1': 1.1, 'ht2': 1.2, 'ht3': 1.3, 'ht4': 1.4, 'ht5': 1.5, 'ht6': 1.6, 'ht7': 1.7, 'ht8': 1.8, 'ht9': 1.9, 'ht10': 2.0, 'ht11': 2.1, 'ht12': 2.2, 'ht13': 2.3, 'ht14': 2.4, 'ht15': 2.5, 'ht16': 2.6, 'ht17': 2.7, 'ht18': 2.8, 'ht19': 2.9}

    result = (pu*multiplier_hi[hi]*multiplier_rei[rei]+iu)*multiplier_tl[tl]
    return result


def dump_system(system):
    print(system['name'])

    if system['systemtype'] in ['Unary Star System','Binary Star System']:
        print('Primary Component Type\t'+system['primary']['startype'])
    else:
        print('Primary Component Type\t'+system['systemtype'])

    if system['systemtype'] == 'Binary Star System':
        print('Binary Component Type\t'+system['binary']['startype'])
        print('Binary Component Dist\t'+system['distance'])

    if system['primary']['planets'] != None:
        for p in range(0, len(system['primary']['planets'])):
            planet = system['primary']['planets'][p]

            print('Planet '+ str(p+1)+ '\t\t'+ str(planet['orbit'])+ '\t'+ str(planet['bearing'])+ '\t'+ str(planet['type'])+ '\t\t\t\t\t'+ str(planet['rei']))
            
            if planet['moons'] != None:
                for m in range(0, len(planet['moons'])):
                    moon = planet['moons'][m]

                    print('\t'+ 'Moon '+ str(m+1)+ '\t'+ str(moon['orbit'])+ '\t'+ str(moon['bearing'])+ '\t'+ moon['type']+ '\t\t\t\t\t'+ moon['rei'])
    print('\t')

    if system['systemtype'] == 'Binary Star System':
        for p in range(0, len(system['binary']['planets'])):
            planet = system['binary']['planets'][p]

            print('Planet '+ str(p+1)+ '\t\t'+ str(planet['orbit'])+ '\t'+ str(planet['bearing'])+ '\t'+ str(planet['type'])+ '\t\t\t\t\t'+ str(planet['rei']))
            
            if planet['moons'] != None:
                for m in range(0, len(planet['moons'])):
                    moon = planet['moons'][m]

                    print('\t'+ 'Moon '+ str(m+1)+ '\t'+ str(moon['orbit'])+ '\t'+ str(moon['bearing'])+ '\t'+ moon['type']+ '\t\t\t\t\t'+ moon['rei'])


def shipyard(ship, tl, typ = 'ship'):
    with open('data\modules.json') as f:
        data = json.loads(f.read())

    ht_index = {'preind': 0.3, 'ind1': 0.6, 'ind2': 0.9, 'ht1': 1.1, 'ht2': 1.2, 'ht3': 1.3, 'ht4': 1.4, 'ht5': 1.5, 'ht6': 1.6, 'ht7': 1.7, 'ht8': 1.8, 'ht9': 1.9, 'ht10': 2.0, 'ht11': 2.1, 'ht12': 2.2, 'ht13': 2.3, 'ht14': 2.4, 'ht15': 2.5, 'ht16': 2.6, 'ht17': 2.7, 'ht18': 2.8, 'ht19': 2.9}
    ships = data['ships']
    carriers = data['carriers']
    bases = data['bases']
    modules = data['modules']

    if typ == 'base':
        sizes = carriers
    elif typ == 'carrier':
        sizes = carriers
    else:
        sizes = ships

    cost = 0
    hs = 0

    for module in ship:
        cost += modules[module]['cost']
        hs += modules[module]['space']

        if ht_index[modules[module]['tl']] > ht_index[tl]:
            print('Module '+ module +' is of a higher tech level than available.')

    for size in sizes:
        if hs >= sizes[size]['min'] and hs <= sizes[size]['max']:
            cost += math.ceil(hs) * sizes[size]['cost']

            if ht_index[sizes[size]['tl']] > ht_index[tl]:
                print('Ship size larger than allowed by tech level.')

            return [hs, size, cost]

    return [hs, cost]