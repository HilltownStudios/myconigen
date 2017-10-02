#! /usr/bin/env python
#
# v2, rewritten with tracery 

import json
import tracery
from tracery.modifiers import base_english

rules = {
  'sentence': 
  [
    '#mushroom#: an inedible mushroom; it has no special uses or effects.',
    '#mushroom#: a mundane, tasteless mushroom; it is used for ornamentation.',
    '#mushroom#: a mundane, tasteless mushroom; it has gardening applications.',
    '#mushroom#: a mundane, tasteless mushroom; it has no special uses or effects.',
    '#mushroom#: a mundane, tasty mushroom; #race# use it to make #food#.',
  ] * 8 +
  [
    '#mushroom#: a mundane, toxic mushroom; CON DC #dc#; fail: #mundaneFail# #duration#; succeed: no effect.',
    '#mushroom#: a mundane, toxic mushroom; CON DC #dc#; fail: #mundaneDamage#; succeed: no effect.',
    '#mushroom#: a mundane, toxic mushroom; CON DC #dc#; fail: #mundaneDamage#; succeed: half.',
    '#mushroom#: a mundane, toxic mushroom; CON DC #dc#; fail: #mundaneDamage# #[dur:#unit#]ongoing#; succeed: no effect.',
    '#mushroom#: a mundane, toxic mushroom; CON DC #dc#; fail: #mundaneDamage# #[dur:#unit#]ongoing#; succeed: half.',
  ] * 4 +
  [
    '#mushroom#: a magical, toxic mushroom; CON DC #dc#; fail: #magicalFail#; succeed: no effect.',
    '#mushroom#: a magical, toxic mushroom; CON DC #dc#; fail: #magicalDamage#; succeed: no effect.',
    '#mushroom#: a magical, toxic mushroom; CON DC #dc#; fail: #magicalDamage#; succeed: half.',
    '#mushroom#: a magical, toxic mushroom; CON DC #dc#; fail: #magicalDamage# #[dur:#unit#]ongoing#; succeed: no effect.',
    '#mushroom#: a magical, toxic mushroom; CON DC #dc#; fail: #magicalDamage# #[dur:#unit#]ongoing#; succeed: half.',
  ] * 2 + 
  [
    '#mushroom#: a mundane deadly mushroom; CON DC #dc#; fail: death; succeed: #mundaneDamage#.',
    '#mushroom#: a magical deadly mushroom; CON DC #dc#; fail: death; succeed: #magicalDamage#.',
  ],
  'mushroom': ['#a# #c#','#a# #b# #c#','#b# #c#','#b# #b# #c#','#b# #a# #c#'],
  'a': json.load(open('data/mushroom_a.json')),
  'b': json.load(open('data/mushroom_b.json')),
  'c': json.load(open('data/mushroom_c.json')),
  'race': ['humans','elves','dwarves','halflings','gnomes','tieflings','dragonborn','orcs','goblins','kobolds','lizardfolk','merfolk'],
  'food': ['ale','beer','wine','stews','soups','roasts','tea','a special spice powder','various meat dishes', 'various poultry dishes','various seafood dishes','various vegetable dishes','rice dishes','oat dishes','barley dishes','various grain dishes','pickles','fermeneted foods'],
  'mundaneFail': ['you are blinded','you are deafened','you gain 1 level of exhaustion','you are frightened','you are paralyzed','you are poisoned','you are stunned','you fall unconscious'],
  'duration': ['for #die# #unit.s#','permanently'],
  'ongoing': ['per #dur# for #die# #dur.s#'],
  'n': ['1','2','3','4','5','6','7','8','9','10'],
  's': ['4','6','8','10','12','20'],
  'die': ['#n#d#s#'],
  'unit': ['round','minute','hour','day'],
  'mundaneDamage':['#die# points of poison damage'],
  'magicalDamage':['#die# points of #element# damage'],
  'element': ['acid','cold','fire','force','necrotic','poison','psychic','radiant','thunder'],
  'dc': ['10']*30 + ['11']*20 + ['12']*15 + ['13']*10 + ['14']*5 + ['15']*3 + ['16']*3 + ['17','18','19','20','21']*2 + ['22','23','24','25','26','27','28','29','30'],
  'magicalFail': ['#mundaneFail#','you become invisible','you are petrified','you are stunned','your speed is reduced by half','your speed is doubled','you grow one size category larger','you are reduced in size by one size category','you become ethereal','you gain resistance to random_element','you gain vulnerablity to random_element','you gain darkvision', 'you gain low-light vision', 'you lose any darkvision you possess','you lose any low-light vision you possess','you gain a fly speed equal to your base speed','you exude a potent stench as per Stinking Cloud','your #ability# score is increased by 2 points','your #ability# score is decreased by 2 points'],
  'ability': ['STR','DEX','CON','INT','WIS','CHA'],
}

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)
print(grammar.flatten("#sentence#"))
