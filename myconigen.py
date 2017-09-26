#! /usr/bin/env python
import json
import random

def get_random_name():
  # Make a random name.
  # open our input files
  mushrooms_a = json.load(open('data/mushroom_a.json'))
  mushrooms_b = json.load(open('data/mushroom_b.json'))
  mushrooms_c = json.load(open('data/mushroom_c.json'))

  patterns = ['ac','abc','bc','bbc','bac']

  out_string = []
  rand_pattern = random.choice(patterns)
  for p in rand_pattern:
    if p == 'a':
      possess = random.choice([0,1])
      rand_a = random.choice(mushrooms_a)
      if possess == 1:
        rand_a = rand_a + "'s"
      out_string.append(rand_a)
    else:
      rand_x = random.choice(eval("mushrooms_" + p))
      out_string.append(rand_x)
  return ' '.join(out_string)

def get_random_dc():
  dcs = [0]*30 + [1]*20 + [2]*15 + [3]*10 + [4]*5 + [5]*3 + [6]*3 + [7,8,9,10,11]*2 + [12,13,14,15,16,17,18,19,20]
  return 10 + random.choice(dcs)

def get_random_die():
  die = ['1d4'] * 50 + ['1d6'] * 30 + ['1d8'] * 10 + ['1d10'] * 5 + ['1d12'] * 3 + ['1d20'] * 2
  return random.choice(die)

def get_random_unit():
  unit = ['round(s)'] * 50 + ['minute(s)'] * 40 + ['day(s)'] * 9 + ['permanently']
  return random.choice(unit)

class Mushroom:
  def __init__(self, name=None, edibility=None, magicality=None):
    self.name = name or get_random_name()

    if not edibility:
      edibility_index = random.choice(range(100))
      if edibility_index < 50:
        self.edibility = 'inedible'
      elif edibility_index < 75:
        self.edibility = 'tasteless'
      elif edibility_index < 95:
        self.edibility = 'toxic'
      elif edibility_index < 99:
        self.edibility = 'tasty'
      else:
        self.edibility = 'deadly'

    if not magicality:
      prob = random.choice(range(3))
      if prob == 0:
        self.magicality = 'magical'
      else:
        self.magicality = 'mundane'

    if self.edibility == 'deadly':
      # this is a deadly mushroom; it has a chance of killing anything that eats it
      self.effect = Effect('death',None,'permanently')
    elif self.edibility != 'deadly' and self.edibility != 'inedible':
      # not an inedible mushroom; inedible mushrooms are inert
      if self.magicality == 'mundane':
        # it's edible but mundane
        if self.edibility == 'toxic':
          # it's edible, mundane, but toxic (non-deadly)
          self.effect = Effect(type='mundane_toxin')
        elif self.edibility == 'tasteless':
          # it's edible, mundane, and otherwise inert; no special culinary uses.
          self.effect = Effect(type='none')
        else:
          # it's edible, mundane, and otherwise inert; has culinary uses
          self.effect = Effect(type='mundane_culinary')
      else:
        # edible and magical
        self.effect = Effect(type='magical')
    else:
      # inedible, therefore inert
        self.effect = Effect(type='none')

  def __str__(self):
    # probably a more elegant approach but..
    if self.edibility == 'inedible':
      return self.name + ': an ' + self.edibility + ' mushroom; ' + self.effect.text
    else:
      return self.name + ': a ' + self.magicality + ', ' + self.edibility + ' mushroom; ' + self.effect.text

class Effect:
  def __init__(self, type, duration_die=None, duration_unit=None, difficulty=None):
    self.type = type
    self.duration_die = duration_die or get_random_die()
    self.duration_unit = duration_unit or get_random_unit()
    self.difficulty = difficulty or get_random_dc()

    if type == 'death':
      # the effect is death; it's as permanent as the game allows
      self.text = "On a failed DC " + str(self.difficulty) + " CON save, you die."
    elif type == 'mundane_toxin':
      # the effect is a nonmagical toxin
      conditions = ['blinded','deafened','fatigued','frightened','paralyzed','poisoned']
      self.text = "On a failed DC " + str(self.difficulty) + " CON save, you are " + random.choice(conditions) + " for " + self.duration_die + " " + self.duration_unit + "."
    elif type == 'none':
      # there is no effect
      self.text = "it has no special uses or effects"
    elif type == 'mundane_culinary':
      # the effect is good cookin'
      races = ['humans','elves','dwarves','halflings','gnomes','tieflings','dragonborn','orcs','goblins','kobolds','lizardfolk']
      foods = ['ale','beer','wine','stews','soups','roasts','tea','a special spice powder', 'various meat dishes', 'various poultry dishes','various seafood dishes','various vegetable dishes','rice dishes','oat dishes','barley dishes','various grain dishes','pickles','fermeneted foods']
      self.text = "it is popular among " + random.choice(races) + " for making " + random.choice(foods) + "."
    else:
      # magical effect, which can overlap with the mundane effects
      self.text = 'it does something shiny, sparkly, or magically dangerous'

  def __str__(self):
    return self.text

m = Mushroom()
print(m)
