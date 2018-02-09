import random, math, os, json

# Used for calculating bearings on anything besides moons. The only thing justifying its existance is that
# it's easier to see what is being done rather than just having the random.
def bodybearing():
    return random.randint(1, 12)


# Used for calculating bearings on moons. Same explanation as before.
def moonbearing():
    return random.randint(1,6)


# Gives type of system. Yes, it's a clusterfuck. If you can do it a bit better without sacrificing readability
# relative to the rulebook, fell free to do it.
# If h is False, it won't gen black holes. Same for n and starless nexi. I haven't actually those options yet so I don't know
# if it serves any actual purpose, but hey, maybe it'll get used at some point.
def systemtype(h=True,n=True):
    if h == False and n == False:
        x = random.randint(11,100) 
    elif h == False and n == True:
        x = random.randint(2,100)
    elif h == True and n == False:
        x = random.randint(11,101)
        if x == 101:
            x = 1
    elif h == True and n == True:
        x = random.randint(1,100)
    else:
        return null

    if x == 1:
        type = 'Black Hole'
    elif x >= 2 and x <= 10:
        type = 'Starless Nexus'
    elif x >= 11 and x <= 45:
        type = 'Binary Star System'
    elif x >= 46 and x <= 100:
        type = 'Unary Star System'
    else:
        return null

    return type


# Gives type of star. Same note as before.
def startype():
    x = random.randint(1,100)
    if x <= 5:
        startype = 'Blue Giant'
    elif x >= 6 and x <= 16:
        startype = 'White Star'
    elif x >= 17 and x <= 41:
        startype = 'Yellow Star'
    elif x >= 42 and x <= 66:
        startype = 'Orange Star'
    elif x >= 67 and x <= 85:
        startype = 'Red Star'
    elif x >= 86 and x <= 95:
        startype = 'Red Dwarf'
    elif x >= 96 and x <= 98:
        startype = 'White Dwarf'
    else:
        startype = 'Red Giant'
    
    return startype


# Calculating distance for binary stars.
def binarydist():
    x = random.randint(1,4)
    y = random.randint(1,100)
    
    if x == 1:
        z = 50
    elif x == 2:
        z = 150
    else:
        z = 250
        
    z = z+y
    return z


# Calculating orbits en batch, going as far as the startype allows. 
def planetorbits(star):
    orbits=[]
    orbits.append(random.randint(1,8))
    orbits.append(random.randint(orbits[0]+2,10))

    if star == 'White Star' or star == 'Yellow Star':
        maxdist = 300
    elif star == 'Orange Star':
        maxdist = 250
    else:
        maxdist = 200

    while orbits[-1] < maxdist:
        orbits.append(orbits[0]+((orbits[1]-orbits[0])*pow(2,len(orbits)-1)))

    while orbits[-1] > maxdist:
        del orbits[-1]

    return orbits


# Picks a random star system name from a list.
def systemname():
    with open('data\json\starnames.txt') as f:
        names = json.loads(f.read())

    return random.choice(names)


# Gives the planet class, acording to the startype and the orbit distance.
def planetclass(star,orbit):
    table = {'White Star':[25, 130, 10, 18, 8], 'Yellow Star':[16, 83, 6, 12, 4], 'Orange Star':[9,38,3,5,3], 'Red Star':[5,18,3,4,3], 'Red Dwarf':[3,11,0,0,2]}

    roll = random.randint(1, 100)
    if roll <= 25:
        mass = 'M1'
    elif roll >= 26 and roll <= 85:
        mass = 'M2'
    else:
        mass = 'M3'

    if orbit <= table[star][0]:
        if orbit < table[star][2]:
            if mass == 'M1':
                planetsig = '01'
            else:
                planetsig = 'V'
        if orbit >= table[star][2] and orbit <= table[star][3]:
            if mass == 'M1':
                planetsig = 'O2'
            elif mass == 'M2':
                planetsig = 'T'
            else:
                planetsig = 'ST'
        if orbit > table[star][3]:
            planetsig = 'O2'
    if orbit > table[star][0] and orbit <= table[star][1]:
        planetsig = 'G'
        mass = None
    if orbit > table[star][1]:
        planetsig = 'I'
        mass = None

    planetclass = [mass, planetsig]
    if orbit <= table[star][4]:
        planetclass.append('Tidally Locked')

    return planetclass


# Gets the mineral content of a planet, given its class.
def getminerals(planet):
    x = random.randint(6,15)

    if planet == '02':
        y = x+3
    elif planet == 'O1':
        y = x+5
    elif planet in ['V', 'G', 'I']:
        return None
    else:
        y = x

    if y == 6:
        mcv = 'Very Poor'
    elif y == 7 or y == 8:
        mcv = 'Poor'
    elif y >= 9 and y <= 12:
        mcv = 'Normal'
    elif y == 13 or y == 14:
        mcv = 'Rich'
    else:
        mcv = 'Very Rich'

    return mcv


# Gives a number of moons depending on the planet type and its mass.
def moonsnum(planet, mass='M1'):
    x = random.randint(1,100)
    if planet in ['O2','T'] and mass == 'M2':
        y = x - 20
    elif planet in ['O2','ST'] and mass == 'M3':
        y = x
    elif planet == 'G':
        y = x + 50
    elif planet == 'I':
        y = x + 35
    elif planet in ['V','O1'] or (mass == 'M1' and planet not in ['G', 'I']):
        return 0

    if y <= 55:
        return 1
    elif y >= 56 and y <= 85:
        return 2
    elif y >= 86 and y <= 105:
        return 3
    elif y >= 106 and y <= 126:
        return 4
    elif y >= 127:
        return 5


# Generates the orbits for the moons of a given planet type. Similar process to planetorbits.
def moonorbits(planet, n):
    orbits = []

    while len(orbits) < n:
        if planet == 'G':
            o = random.randint(1,10)

        elif planet == 'I':
            o = random.randint(1,10)/2.0
            o = int(math.ceil(o))

        elif planet in ['O2', 'T', 'ST']:
            o = random.randint(1,10)/2

        if o not in orbits:
            orbits.append(o)

    return orbits


# Simple function that gives the moon tipe relative to the planet. Its only actual purpose is for dealing with I planets
def moonclass(planet):
    if planet == 'I':
        return 'O1'
    else:
        return 'O2'


# Generates a complete starsystem, given it's name. Still lacks WP generation.
# Yes, it's a huge clusterfuck, and honestly I'm fine with the way it is.
def starsys(name):
    system = {'systemtype': systemtype(), "name": name} #'Unary Star System'}] 'Binary Star System']}

# Star(s) and orbital bodies generation
    if system['systemtype'] in ['Unary Star System','Binary Star System']:
        system['star'] = {'startype': startype()}
        star = system['star']        
        star['name'] = str(name+'-A')
# First check if system is binary. If so, do it first because it's easier to deal with the whole distance thingy
        if system['systemtype'] == 'Binary Star System':
            system['star']['secondary'] = {}
            star2 = system['star']['secondary']
            star2['name'] = str(name+'-B')
            star2['startype'] = startype()
            star2['orbit'] = binarydist()
            star2['bearing'] = bodybearing()

# Check if any body can happen at all. If not, don't gen planets at all
            if star2['startype'] in ['Blue Giant', 'White Dwarf', 'Red Giant']:
                star2['planets'] = None

# Otherwise, gen planets
            else:
                star2['planets'] = []
                d = planetorbits(star2['startype'])
                types = []
                for n in range(0, len(d)):
                    if d[n] <= star2['orbit']/4:
                        a = planetclass(star2['startype'], d[n])
                        z = moonsnum(a[1], a[0])
                        lmoonorbits = moonorbits(a[1], z)
                        types.append(a[1])

                        star2['planets'].append({'name': star2['name']+'-'+str(n+1), 'orbit': d[n], 'bearing': bodybearing(), 'mass': a[0], 'type': a[1], 'moons': [], 'minerals': getminerals(a[1])})
                        for m in range(1, z):
                            star2['planets'][n]['moons'].append({'name': star2['name']+'-'+str(n+1)+'-'+str(m+1), 'orbit': lmoonorbits[m-1], 'bearing': moonbearing(), 'type': moonclass(a[1]), 'minerals': getminerals(moonclass(a[1]))})

                    elif d[n] >= star2['orbit']/4 and d[n] <= star2['orbit']/3:
                        star2['planets'].append({'name': star2['name']+'-'+str(n+1), 'orbit': d[n], 'bearing': None, 'mass': None, 'type': 'AB', 'moons': None, 'minerals': 'Rich'})
                for n in range (len(types), 0, -1):
                    if types[n-1] == 'G' and n > 1:
                        x = random.randint(1,5)
                        if x == 1:
                            print("AB")
                            star2['planets'][n-2]['bearing'] = {'name': star2['name']+'-'+str(n-1), 'orbit': d[n], 'bearing': None, 'mass': None, 'type': 'AB', 'moons': None, 'minerals': 'Rich'}

# Check if any body can happen at all. If not, don't gen planets at all
        if star['startype'] in ['Blue Giant', 'White Dwarf', 'Red Giant']:
            star['planets'] = None

# Otherwise, gen planets
        else:
# If the system is binary, only gen up to a certain point
            star['planets'] = []
            d = planetorbits(star['startype'])
            types = []
            if system['systemtype'] == 'Binary Star System':
                for n in range(0, len(d)):
                    if d[n] <= star2['orbit']/4:
                        a = planetclass(star['startype'], d[n])
                        z = moonsnum(a[1], a[0])
                        lmoonorbits = moonorbits(a[1], z)
                        types.append(a[1])

                        star['planets'].append({'name': star['name']+'-'+str(n+1), 'orbit': d[n], 'bearing': bodybearing(), 'mass': a[0], 'type': a[1], 'moons': [], 'minerals': getminerals(a[1])})

                        for m in range(0, z):
                            star['planets'][n]['moons'].append({'name': star['name']+'-'+str(n+1)+'-'+str(m+1), 'orbit': lmoonorbits[m-1], 'bearing': moonbearing(), 'mass': moonclass(a[1]), 'minerals': getminerals(moonclass(a[1]))})

                    elif d[n] >= star2['orbit']/4 and d[n] <= star2['orbit']/3:
                        star['planets'].append({'name': star['name']+'-'+str(n+1), 'orbit': d[n], 'bearing': None, 'mass': None, 'type': 'AB', 'moons': None, 'minerals': 'Rich'})
# Else, generate all
            else:
                for n in range(0, len(d)):         
                    a = planetclass(star['startype'], d[n])
                    z = moonsnum(a[1], a[0])
                    lmoonorbits = moonorbits(a[1], z)
                    types.append(a[1])

                    star['planets'].append({'name': star['name']+'-'+str(n+1), 'orbit': d[n], 'bearing': bodybearing(), 'mass': a[0], 'type': a[1], 'moons': [], 'minerals': getminerals(a[1])})

                    for m in range(0, z):
                        star['planets'][n]['moons'].append({'name': star['name']+'-'+str(n+1)+'-'+str(m+1), 'orbit': lmoonorbits[m-1], 'bearing': moonbearing(), 'mass': moonclass(a[1]), 'minerals': getminerals(moonclass(a[1]))})                   
            for n in range (len(types), 0, -1):
                if types[n-1] == 'G' and n > 1:
                    x = random.randint(1,5)
                    if x == 1:
                        print("AB")
                        star['planets'][n-2] = {'name': star['name']+'-'+str(n-1), 'orbit': d[n], 'bearing': None, 'mass': None, 'type': 'AB', 'moons': None, 'minerals': 'Rich'}
    
    return system


# Deals with moving things on a hex grid, the bane of my existance.
def move(pos,bearing):
    newpos = [0,0]
    if bearing == 1:
        newpos[0] = pos[0]
        newpos[1] = pos[1]+1
    elif bearing == 2:
        if pos[0] % 2 == 0:
            newpos[0] = pos[0]+1
            newpos[1] = pos[1]
        else:
            newpos[0] = pos[0]+1
            newpos[1] = pos[1]+1
    elif bearing == 3:
        if pos[0] % 2 == 0:
            newpos[0] = pos[0]+1
            newpos[1] = pos[1]-1
        else:
            newpos[0] = pos[0]+1
            newpos[1] = pos[1]
    elif bearing == 4:
        newpos[0] = pos[0]
        newpos[1] = pos[1]-1
    elif bearing == 5:
        if pos[0] % 2 == 0:
            newpos[0] = pos[0]-1
            newpos[1] = pos[1]-1
        else:
            newpos[0] = pos[0]-1
            newpos[1] = pos[1]
    elif bearing == 6:
        if pos[0] % 2 == 0:
            newpos[0] = pos[0]-1
            newpos[1] = pos[1]
        else:
            newpos[0] = pos[0]-1
            newpos[1] = pos[1]+1
    return newpos


# Finds ranges. It needs to recognize if there are impassable objects but hey, it serves.
def rangefinder(start,end):
    currpos = start
    range = 0
    while currpos != end:
        if currpos[0] == end[0] and currpos[1] < end[1]:
            currpos = move(currpos,1)
        elif currpos[0] < end[0] and currpos[1] < end[1]:
            currpos = move(currpos,2)
        elif currpos[0] > end[0] and currpos[1] < end[1]:
            currpos = move(currpos,6)
        elif currpos[0] < end[0] and currpos[1] == end[1]:
            if pos[0] % 2 == 0:
                currpos = move(currpos,3)
            else:
                currpos = move(currpos,2)
        elif currpos[0] > end[0] and currpos[1] == end[1]:
            if pos[0] % 2 == 0:
                currpos = move(currpos,5)
            else:
                currpos = move(currpos,6)
        elif currpos[0] < end[0] and currpos[1] > end[1]:
            currpos = move(currpos,3)
        elif currpos[0] > end[0] and currpos[1] > end[1]:
            currpos = move(currpos,5)
        elif currpos[0] == end[0] and currpos[1] > end[1]:
            currpos = move(currpos,4)
        range += 1
    return range


# These three classes return the multipliers for the different GPV variables.
def evm(evm):
    table = {'Benign': 1.0, 'Harsh': 1.0, 'Hostile': 1.0, 'Desolate': 0.7, 'Extreme': 0.6}
    return table[evm]


def mcv(mcv):
    table = {'Very Poor': 0.5, 'Poor': 0.75, 'Normal': 1.0, 'Rich': 1.25, 'Very Rich': 1.5}
    return table[mcv]


def tl(tl):
    table = {'pre-ind': 0.3, 'ind1': 0.6, 'ind2': 0.9, 'ht1': 1.1, 'ht2': 1.2, 'ht3': 1.3, 'ht4': 1.4, 'ht5': 1.5, 'ht6': 1.6, 'ht7': 1.7, 'ht8': 1.8, 'ht9': 1.9, 'ht10': 2.0, 'ht11': 2.1, 'ht12': 2.2, 'ht13': 2.3, 'ht14': 2.4, 'ht15': 2.5, 'ht16': 2.6, 'ht17': 2.7, 'ht18': 2.8, 'ht19': 2.9}
    return table[tl]


# Classes!
class System:

    def __init__(self, data, index):
        self.index = index
        self.data = data
        self.systype = self.data['systemtype']
        self.bodies = []

    def makebodies(self):
        star = Star(self.data['star']['name'], self.data['star']['startype'])
        self.bodies.append(star)
        self.bodies.append([])

        if self.data['systemtype'] == 'Binary Star System':
            star2 = Star(self.data['star']['secondary']['name'], self.data['star']['secondary']['startype'])
            self.bodies[0].append(star2)
            
            for p in range(0, len(self.data['star']['secondary']['planets'])):
                planet = Planet(self.data['star']['secondary']['planets'][p] ,self.data['star']['secondary']['name'])
                self.bodies[0].append(planet)


        for p in range(0, len(self.data['star']['planets'])):
            planet = Planet(self.data['star']['planets'][p] ,self.data['star']['name'])
            self.bodies.append(planet)


class Star:

    def __init__(self, name, startype):
        self.name = name
        self.startype = startype


class Planet:
    
    def __init__(self, data, star):
        self.name = data['name']
        self.orbit = data['orbit']
        self.bearing = data['bearing']
        self.type = data['type']
        self.minerals = data['minerals']
        self.primary = star


'''
class Empire:

    def __init__(self, data):
'''


class Population:

    def __init__(self, data, mcv):
        self.name = data['name']
        self.location = data['location']
        self.evm = data['evm']
        self.mcv = mcv
        self.pop = data['pop']
        self.ind = data['ind']
        self.race = data['race']
        self.tech = data['tech']
        self.rm = data['rm']
        self.rc = data['rc']
        self.capital = data['capital']

    def gpv(self):
        return (self.pop * evm(self.evm) * mcv(self.mcv) + self.ind)* tl(self.tech)


def shipyard(ship = [], type = 'ship', tl = None, modules = None, debug = True):
    with open('data\json\modules.json') as f:
        modules = json.loads(f.read())

    with open('data\json\hulls.json') as f:
        hulls = json.loads(f.read())

    cost = 0
    hs = 0

    for module in ship:
        cost += modules[module]['cost']
        hs += modules[module]['space']

    for hull in hulls:
        if hs >= hulls[hull]['min'] and hs <= hulls[hull]['max']:
            cost += math.ceil(hs) * hulls[hull]['cost']
            return [hs, hull, cost]

    return [hs, cost]


def base(ship = [], tag = 1.0):
    with open('modules.json') as f:
        modules = json.loads(f.read())

    cost = 0
    hs = 0
    mods = []
    spaces = []

    for module in ship:
        cost += modules[module]['cost']
        hs += modules[module]['space']

        mods.append(modules[module]['cost'])
        spaces.append(modules[module]['space'])


    cost += math.ceil(hs) * tag

    return [hs, cost]

