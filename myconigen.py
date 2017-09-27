#! /usr/bin/env python
import json
import random

# Setup; these are needed everywhere. If the script grows, this will have to move.
CONDITIONS = ['you are blinded','you are deafened','you gain 1 level of exhaustion','you are frightened','you are paralyzed','you are poisoned','you are stunned','you fall unconscious']

MAGICAL_CONDITIONS = CONDITIONS + ['you become invisible','you are petrified','you are stunned','your speed is reduced by half','your speed is doubled','you grow one size category larger','you are reduced in size by one size category','you become ethereal','you gain resistance to random_element','you gain vulnerablity to random_element','you gain darkvision', 'you gain low-light vision', 'you lose any darkvision you possess','you lose any low-light vision you possess','you gain a fly speed equal to your base speed','you exude a potent stench as per Stinking Cloud','your random_ability score is increased by 2 points','your random_ability score is decreased by 2 points','special_damage_condition']

DAMAGE_CONDITIONS = ['you take random_die hit points of random_element','you regain random_die hit points','you take random_die hit points of random_element per random_unit','you regain random_die hit points per random_unit']

ELEMENTS = ['acid damage','cold damage','fire damage','force damage','necrotic damage','poison damage','psychic damage','radiant damage','thunder damage']

ABILITIES = ['Strength','Dexterity','Constitution','Intelligence','Wisdom','Charisma']

DCS = [0]*30 + [1]*20 + [2]*15 + [3]*10 + [4]*5 + [5]*3 + [6]*3 + [7,8,9,10,11]*2 + [12,13,14,15,16,17,18,19,20]

DICE = ['1d4'] * 50 + ['1d6'] * 30 + ['1d8'] * 10 + ['1d10'] * 5 + ['1d12'] * 3 + ['1d20'] * 2

UNITS = ['rounds'] * 50 + ['minutes'] * 40 + ['days'] * 9 + ['permanently']

RACES = ['humans','elves','dwarves','halflings','gnomes','tieflings','dragonborn','orcs','goblins','kobolds','lizardfolk','merfolk']

FOODS = ['ale','beer','wine','stews','soups','roasts','tea','a special spice powder', 'various meat dishes', 'various poultry dishes','various seafood dishes','various vegetable dishes','rice dishes','oat dishes','barley dishes','various grain dishes','pickles','fermeneted foods']

# One function to build a random name. 
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

def singularize(plural):
  # only removes the trailing s
  singular = plural
  if plural.endswith('s'):
    singular = plural[:-1]
  return singular

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
    self.duration_die = duration_die or random.choice(DICE)
    self.duration_unit = duration_unit or random.choice(UNITS)
    self.difficulty = difficulty or 10 + random.choice(DCS)
    condition = None

    if type == 'death':
      # the effect is death; it's as permanent as the game allows
      self.text = "On a failed DC " + str(self.difficulty) + " CON save, you die."
    elif type == 'mundane_toxin':
      # the effect is a nonmagical toxin
      self.text = "CON (DC " + str(self.difficulty) + ") or " + random.choice(CONDITIONS) + " for " + self.duration_die + " " + self.duration_unit + "."
    elif type == 'none':
      # there is no effect
      self.text = "it has no special uses or effects"
    elif type == 'mundane_culinary':
      # the effect is good cookin'
      self.text = "it is popular among " + random.choice(RACES) + " for making " + random.choice(FOODS) + "."
    else:
      # magical effect, which can overlap with the mundane effects
      # parse selected conditions
      condition = random.choice(MAGICAL_CONDITIONS)
      if condition == 'special_damage_condition':
        # throw out the old condition and get a new one from a different list
        condition = random.choice(DAMAGE_CONDITIONS)
        condition = condition.replace('random_element', random.choice(ELEMENTS))
        condition = condition.replace('random_die', random.choice(DICE))
        condition = condition.replace('random_unit', singularize(self.duration_unit))
        if ' per ' in condition and self.duration_unit != 'permanently':
          self.text = "CON (DC " + str(self.difficulty) + ") or " + condition + " for " + self.duration_die + " " + self.duration_unit + "."
        #elif ' per ' in condition and self.duration_unit == 'permaently':
        #  self.text = "CON (DC " + str(self.difficulty) + ") or " + condition + " " + self.duration_unit + "."
        else:
          self.text = "CON (DC " + str(self.difficulty) + ") or " + condition + "  " + self.duration_unit + "."
      else:
        # make these substitutions as necessary
        condition = condition.replace('random_element', random.choice(ELEMENTS))
        condition = condition.replace('random_die', random.choice(DICE))
        condition = condition.replace('random_unit', self.duration_unit)
        condition = condition.replace('random_ability', random.choice(ABILITIES))
        if self.duration_unit == 'permanently':
          self.text = "CON (DC " + str(self.difficulty) + ") or " + condition + "  " + self.duration_unit + "."
        else:
          self.text = "CON (DC " + str(self.difficulty) + ") or " + condition + " for " + self.duration_die + " " + self.duration_unit + "."

  def __str__(self):
    return self.text

m = Mushroom()
print(m)
