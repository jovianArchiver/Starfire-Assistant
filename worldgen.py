import math
import random
import config

systems = config.save['systems']


# Used for generating bearings. Returns an integer.
def generate_bearing():
    return random.randint(1, 12)


# Used for generating facings. Returns an integer.
def generate_facing():
    return random.randint(1, 6)


# Generates the type of solar system. Returns a string.
def generate_system_type():
    x = random.randint(2, 100)

    if x == 1:
        systemtype = 'Black Hole'
    elif 2 <= x <= 10:
        systemtype = 'Starless Nexus'
    elif 11 <= x <= 45:
        systemtype = 'Binary Star System'
    else:
        systemtype = 'Unary Star System'

    return systemtype


# Generates the type of star. Returns a string.
def generate_star_type():
    x = random.randint(1, 100)
    if x <= 5:
        startype = 'Blue Giant'
    elif 5 < x <= 16:
        startype = 'White Star'
    elif 16 < x <= 41:
        startype = 'Yellow Star'
    elif 41 < x <= 66:
        startype = 'Orange Star'
    elif 66 < x <= 85:
        startype = 'Red Star'
    elif 85 < x <= 95:
        startype = 'Red Dwarf'
    elif 95 < x <= 98:
        startype = 'White Dwarf'
    else:
        startype = 'Red Giant'

    return startype


# Generates the mass of a planet. Returns a string.
def generate_mass():
    roll = random.randint(1, 20)

    if roll <= 5:
        mass = 'M1'
    elif 5 < roll <= 17:
        mass = 'M2'
    else:
        mass = 'M3'

    return mass


# Generates the type of a planet for a given star and distance. Returns [type, mass, tidally locked].
def generate_planet_type(star, orbit):
    table = {'White Star': [10, 18, 25, 130, 8],
             'Yellow Star': [6, 12, 16, 83, 4],
             'Orange Star': [3, 5, 9, 38, 3],
             'Red Star': [3, 4, 5, 18, 3],
             'Red Dwarf': [0, 0, 3, 11, 2]}

    mass = generate_mass()

    if orbit <= table[star][2]:
        if orbit < table[star][0]:
            if mass == 'M1':
                planet_type = '01'
            else:
                planet_type = 'V'
        if table[star][0] <= orbit <= table[star][1]:
            if mass == 'M1':
                planet_type = 'O2'
            elif mass == 'M2':
                planet_type = 'T'
            else:
                planet_type = 'ST'
        if orbit > table[star][1]:
            planet_type = 'O2'
    elif table[star][2] < orbit <= table[star][3]:
        planet_type = 'G'
        mass = False
    elif orbit > table[star][3]:
        planet_type = 'I'
        mass = False

    # noinspection PyUnboundLocalVariable
    planet_class = [planet_type, mass, False]
    if orbit <= table[star][4]:
        planet_class[2] = True

    return planet_class


# Generates the type of a moon. Returns a string.
def generate_moon_type(planet):
    if planet == 'I':
        return 'O1'
    else:
        return 'O2'


# Generates the distance for binary stars. Returns an integer.
def generate_binary_distance():
    x = random.randint(1, 4)
    z = random.randint(1, 100)

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
    roll = random.randint(1, 10)

    if planet == '02':
        roll += 3
    elif planet == 'O1':
        roll += 5
    elif planet in ['V', 'G', 'I']:
        return False

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
# noinspection PyListCreation,PyListCreation
def generate_orbits_planets(star, binary=False):
    orbits = []
    orbits.append(random.randint(1, 8))
    orbits.append(random.randint(orbits[0] + 2, 10))
    difference = orbits[1] - orbits[0]

    if binary:
        max_dist = binary
    else:
        if star == 'White Star' or star == 'Yellow Star':
            max_dist = 300
        elif star == 'Orange Star':
            max_dist = 250
        else:
            max_dist = 200

    while orbits[-1] < max_dist:
        orbits.append(orbits[-1] + difference * pow(2, len(orbits) - 2))

    del orbits[-1]
    return orbits


# Generates the orbits of the moons for a given planet. Returns a list.
# noinspection PyUnboundLocalVariable
def generate_orbits_moons(planet, number):
    orbits = []

    while len(orbits) < number:
        if planet == 'G':
            x = random.randint(1, 10)

        elif planet == 'I':
            x = random.randint(1, 10) / 2.0
            x = math.ceil(x)

        elif planet in ['O2', 'T', 'ST']:
            x = int(random.randint(1, 10) / 2)
            if x == 0:
                x = 1

        if x not in orbits:
            orbits.append(x)

    orbits.sort()
    return orbits


# Generates the number of moons for a given planet. Returns an integer.
def generate_number_moons(planet, mass):
    roll = random.randint(1, 100)

    if planet not in ['G', 'I']:
        if planet == 'V' or mass == 'M1':
            return False
        elif mass == 'M2':
            roll += -10

    elif planet == 'G':
        roll += 50
    elif planet == 'I':
        roll += 35

    if roll < 56:
        return 1
    elif 56 <= roll < 86:
        return 2
    elif 86 <= roll < 106:
        return 3
    elif 106 <= roll < 127:
        return 4
    elif roll >= 127:
        return 5


# Generates the moons that orbit a given planet. Returns a list.
def generate_list_moons(planet, mass):
    number = generate_number_moons(planet, mass)
    if not number:
        return False

    moon_orbits = generate_orbits_moons(planet, number)
    moon_type = generate_moon_type(planet)
    moon_list = []

    for moon in moon_orbits:
        moon_list.append(
            {'orbit': moon,
             'bearing': generate_facing(),
             'type': moon_type,
             'rei': generate_rei(moon_type)})

    return moon_list


# Generates the planets that orbit a given star. If distance_binary is an integer,
#  creates the planets as orbiting a component in a binary, given the distance. Returns a dictionary.
def generate_list_planets(star, binary=False):
    if star in ['Blue Giant', 'White Dwarf', 'Red Giant']:
        return False

    planets = []

    planet_orbits = generate_orbits_planets(star, binary)

    for planet in range(0, len(planet_orbits)):
        planet_class = generate_planet_type(star, planet_orbits[planet])
        planet_type = planet_class[0]
        planet_mass = planet_class[1]

        if binary != False and planet_orbits[planet] >= binary / 3:
            planets.append(
                {'orbit': planet_orbits[planet],
                 'bearing': 'N/A',
                 'type': 'AS',
                 'hi': False,
                 'rei': generate_rei('O2'),
                 'tide_lock': False,
                 'moons': False})
        else:
            planets.append(
                {'orbit': planet_orbits[planet],
                 'bearing': generate_bearing(),
                 'type': planet_type, 'hi': False,
                 'rei': generate_rei(planet_type),
                 'tide_lock': False,
                 'moons': generate_list_moons(planet_type, planet_mass)})

        if planet_class == 'T':
            planets[planet]['hi'] = random.randint(1, 10)

    for planet in range(len(planets) - 1, 1, -1):
        if planets[planet]['type'] == 'G' and random.randint(1, 10) < 7:
            planets[planet - 1] = {'orbit': planet_orbits[planet - 1],
                                   'bearing': 'N/A',
                                   'type': 'AS',
                                   'hi': False,
                                   'rei': generate_rei('O2'),
                                   'tide_lock': False,
                                   'moons': False}

    return planets


# Generates an entire solar system, given a name or id. Returns a dictionary.
def generate_solar_system():
    system = {'systemtype': generate_system_type(),
              'primary': False,
              'binary': False,
              'distance': False}

    if system['systemtype'] == 'Binary Star System':
        startype = generate_star_type()
        system['distance'] = generate_binary_distance()

        system["binary"] = {'startype': startype,
                            'planets': generate_list_planets(startype, system['distance'])}

    else:
        del system['binary']

    if system['systemtype'] in ['Unary Star System', 'Binary Star System']:
        startype = generate_star_type()

        system['primary'] = {'startype': startype,
                             'planets': generate_list_planets(startype, system['distance'])}

        if system['systemtype'] == 'Unary Star System':
            del system['distance']

    else:
        del system['primary']

    return system


# Truncates a name to a certain length, adding an ellipsis at the end.
def truncate_name(name, short=-2, length=config.name_length):
    if len(name) > length - short:
        return name[:15] + '...'

    else:
        return name


# noinspection PyListCreation
def print_system_primary(number, name, star, binary=False):
    line = []

    line.append(' ' * (4 - len(str(number))) + str(number) + ' ')  # ID

    line.append(name)

    if binary:
        line.append('-A')

    line.append(' ' * (config.name_length - len(name) - 2 * binary) + ' ')
    line.append(star)

    print(''.join(line))


# noinspection PyListCreation
def print_system_binary(name, star):
    line = []

    line.append(' ' * 5)
    line.append(name + '-B')
    line.append(' ' * (config.name_length - 2 - len(name)) + ' ')
    line.append(star)

    print(''.join(line))


# noinspection PyListCreation
def print_system_special(name, systemtype):
    line = []

    line.append(' ' * (4 - len(str(name))) + str(name) + ' ')
    line.append(name)
    line.append(' ' * (config.name_length - len(name)) + ' ')
    line.append(systemtype)

    print(''.join(line))


# noinspection PyListCreation
def print_body(name, orbit, bearing, body_type, rei, pop=False, moon=False):
    # Name                 Orbit  B Type REI      PU     IU     GPV
    line = []

    line.append(' ' * moon)
    line.append(name)
    line.append(' ' * (config.name_length - len(name) - moon) + ' ')
    line.append(' ' * (3 - len(str(orbit))) + str(orbit) + 'LM ')

    if not bearing:
        line.append(' - ')
    else:
        line.append(' ' * (2 - len(str(bearing))) + str(bearing) + ' ')

    line.append(' ' * (3 - len(body_type)) + body_type + '  ')

    if not rei:
        line.append(' -  ')
    else:
        rei_table = {'V.Poor': 'V.P', 'Poor': ' P ', 'Normal': ' N ', 'Rich': ' R ', 'V.Rich': 'V.R'}
        line.append(rei_table[rei] + ' ')

    if pop:
        line.append(' ' * (4 - len(str(pop['pu']))) + str(pop['pu']) + 'PU ')
        line.append(' ' * (4 - len(str(pop['iu']))) + str(pop['iu']) + 'IU ')
        line.append(' ' * (5 - len(str(pop['gpv']))) + str(pop['gpv']) + 'MC')

    print(''.join(line))


# noinspection PyShadowingNames
def print_systems_list(systems, npr, override=False):
    print('  ID Name                 Type')

    for n in range(0, len(systems)):
        if npr['systems'][n] != False or override == True:
            name = truncate_name(npr['systems'][n]['system_name'])

            if systems[n]['systemtype'] == 'Binary Star System':
                print_system_primary(n, name, systems[n]['primary']['startype'], True)
                print_system_binary(name, systems[n]['binary']['startype'])

            elif systems[n]['systemtype'] == 'Unary Star System':
                print_system_primary(n, name, systems[n]['primary']['startype'])

            else:
                # noinspection PyTypeChecker
                print_system_special(n, systems[n]['systemtype'])


def print_planets_list(name, planets, npr, primary='primary'):
    for n in range(0, len(planets)):
        planet = planets[n]

        if not npr[n]['name']:
            planet_name = name + '-' + str(n + 1)
        else:
            planet_name = truncate_name(npr[n]['name'])

        print_body(planet_name, planet['orbit'], planet['bearing'], planet['type'], planet['rei'], npr[n]['population'])
        moons = planets[n]['moons']

        if 'moons' in planets[n] and moons != False:
            for m in range(0, len(moons)):
                moon = moons[m]

                if not npr[n]['moons'][m]['name']:
                    moon_name = truncate_name(planet_name + '-' + str(m + 1))
                else:
                    moon_name = truncate_name(npr[primary]['planets'][n]['moons'][m])

                print_body(moon_name, moon['orbit'], moon['bearing'], moon['type'], moon['rei'],
                           npr[n]['moons'][m]['population'], moon=True)


def print_system(n, system, npr):
    if not npr['system_name']:
        name = str(n)
    else:
        name = truncate_name(npr['system_name'])

    if system['systemtype'] in ['Unary Star System', 'Binary Star System']:
        print_system_primary(n, name, systems[n]['primary']['startype'], system['systemtype'] == 'Binary Star System')
        print('\nName                 Orbit  B Type REI     PU     IU     GPV')
        print_planets_list(name, system['primary']['planets'], npr['primary']['planets'])

        if system['systemtype'] == 'Binary Star System':
            print_system_binary(name, systems[n]['binary']['startype'])
            print('\nName                 Orbit  B Type REI     PU     IU     GPV')
            print_planets_list(name, system['binary']['planets'], npr['binary']['planets'], 'binary')
