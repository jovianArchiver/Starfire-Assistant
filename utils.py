# Prints out the star system in the format used by my Google drive sheets. Returns a string.
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

# Modified version of the solar system generation function that uses predetermined parameters instead of rng. 
def generate_solar_system_modified(star):
    system = {'systemtype': 'Unary Star System', 'name': star[0], 'primary': None, 'binary': None, 'distance': None}

    if system['systemtype'] == 'Binary Star System':
        startype = star
        system['distance'] = generate_distance_binary()

        system['binary'] = {'startype': startype, 'planets': generate_list_planets(startype, system['distance'])}

    else:
        del system['binary']

    if system['systemtype'] in ['Unary Star System', 'Binary Star System']:
        startype = star[1]

        system['primary'] = {'startype': startype, 'planets': generate_list_planets(startype, system['distance'])}

        del system['distance']
    else:
        del system['primary']

    return system

for star in [[28, 'Yellow Star'], [31, 'Orange Star'], [33, 'White Star'], [41, 'Red Star'], [43, 'Yellow Star'], [44, 'Orange Star'], [47, 'Orange Star'], [48, 'Yellow Star'], [49, 'Orange Star'], [55, 'Red Dwarf'], [57, 'Orange Star']]:
    print(dump_system(generate_solar_system_modified(star)))