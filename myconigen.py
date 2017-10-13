#! /usr/bin/env python
# v2, rewritten with tracery 

import json
import tracery
from tracery.modifiers import base_english
import tweepy
from time import sleep

from secrets import *

# Emojis shorten things maybe.
MUSHROOM = u"\U0001F344"
DELICIOUS = u"\U0001F60B"
DEADLY = u"\U00002620"
MAGICAL = u"\U00002728"
TOXIC = u"\U0001F922"

rules = {
  'sentence': 
  [
    '#mushroom#: an inedible ' + MUSHROOM + '; it has no special uses or effects.',
    '#mushroom#: a mundane, tasteless ' + MUSHROOM + '; it is used for ornamentation.',
    '#mushroom#: a mundane, tasteless ' + MUSHROOM + '; it has gardening applications.',
    '#mushroom#: a mundane, tasteless ' + MUSHROOM + '; it has no special uses or effects.',
    '#mushroom#: a mundane, ' + DELICIOUS + MUSHROOM + '; #race# use it to make #food#.',
  ] * 8 +
  [
    '#mushroom#: a mundane, ' + TOXIC + MUSHROOM + '; CON DC #dc#; fail: #mundaneFail# #duration#; succeed: no effect.',
    '#mushroom#: a mundane, ' + TOXIC + MUSHROOM + '; CON DC #dc#; fail: #mundaneDamage#; succeed: no effect.',
    '#mushroom#: a mundane, ' + TOXIC + MUSHROOM + '; CON DC #dc#; fail: #mundaneDamage#; succeed: half.',
    '#mushroom#: a mundane, ' + TOXIC + MUSHROOM + '; CON DC #dc#; fail: #mundaneDamage# #[dur:#unit#]ongoing#; succeed: no effect.',
    '#mushroom#: a mundane, ' + TOXIC + MUSHROOM + '; CON DC #dc#; fail: #mundaneDamage# #[dur:#unit#]ongoing#; succeed: half.',
  ] * 4 +
  [
    '#mushroom#: a ' + MAGICAL + TOXIC + MUSHROOM + '; CON DC #dc#; fail: #magicalFail# #duration#; succeed: no effect.',
    '#mushroom#: a ' + MAGICAL + TOXIC + MUSHROOM + '; CON DC #dc#; fail: #magicalDamage#; succeed: no effect.',
    '#mushroom#: a ' + MAGICAL + TOXIC + MUSHROOM + '; CON DC #dc#; fail: #magicalDamage#; succeed: half.',
    '#mushroom#: a ' + MAGICAL + TOXIC + MUSHROOM + '; CON DC #dc#; fail: #magicalDamage# #[dur:#unit#]ongoing#; succeed: no effect.',
    '#mushroom#: a ' + MAGICAL + TOXIC + MUSHROOM + '; CON DC #dc#; fail: #magicalDamage# #[dur:#unit#]ongoing#; succeed: half.',
  ] * 2 + 
  [
    '#mushroom#: a mundane ' + DEADLY + MUSHROOM + '; CON DC #dc#; fail: death; succeed: #mundaneDamage#.',
    '#mushroom#: a ' + MAGICAL + DEADLY + MUSHROOM + '; CON DC #dc#; fail: death; succeed: #magicalDamage#.',
  ],
  'mushroom': ['#a# #c#','#a# #b# #c#','#b# #c#','#b# #b# #c#','#b# #a# #c#'],
  'a': json.load(open('data/mushroom_a.json')),
  'b': json.load(open('data/mushroom_b.json')),
  'c': json.load(open('data/mushroom_c.json')),
  'race': ['humans','elves','dwarves','halflings','gnomes','tieflings','dragonborn','orcs','goblins','kobolds','lizardfolk','merfolk'],
  #'food': ['ale','beer','wine','stews','soups','roasts','tea','a special spice powder','various meat dishes', 'various poultry dishes','various seafood dishes','various vegetable dishes','rice dishes','oat dishes','barley dishes','various grain dishes','pickles','fermeneted foods'],
  'food': ['ale',u'\U0001F37A',u'\U0001F377','stews','soups','roasts',u'\U00002615','a special spice powder',u'\U0001F356', u'\U0001F357',u'\U0001F363','various vegetable dishes',u'\U0001F35A','oat dishes','barley dishes',u'\U0001F33E',u'\U0001F952','fermeneted foods'],
  #'mundaneFail': ['blinded','deafened','gain 1 level of exhaustion','frightened','paralyzed','poisoned','stunned','fall unconscious'],
  'mundaneFail': ['blinded','deafened','gain 1 level of exhaustion',u'\U0001F631','paralyzed','poisoned',u'\U0001F635',u'\U0001F634'],
  'duration': ['for #die# #unit.s#','permanently'],
  'ongoing': ['per #dur# for #die# #dur.s#'],
  'n': ['1','2','3'] * 4 + ['4','5','6','7','8','9','10'],
  's': ['4','6','8'] * 2 + ['10','12','20'],
  'die': ['#n#d#s#'],
  'unit': ['round','minute','hour','day'],
  'mundaneDamage':['#die# points of poison damage'],
  'magicalDamage':['#die# points of #element# damage'],
  #'element': ['acid','cold','fire','force','necrotic','poison','psychic','radiant','thunder'],
  'element': ['acid',u'\U00002744',u'\U0001F525','force','necrotic','poison',u'\U0001F52E',u'\U00002600',u'\U000026C8'],
  'dc': ['10']*30 + ['11']*20 + ['12']*15 + ['13']*10 + ['14']*5 + ['15']*3 + ['16']*3 + ['17','18','19','20','21']*2 + ['22','23','24','25','26','27','28','29','30'],
  'magicalFail': ['#mundaneFail#','become invisible','petrified','speed is reduced by half','speed is doubled','grow one size category larger','reduced in size by one category','become ethereal','gain resistance to #element# damage','gain vulnerablity to #element# damage','gain darkvision', 'gain low-light vision', 'lose any darkvision you possess','lose any low-light vision you possess','gain a fly speed equal to your base speed','exude a potent stench as per Stinking Cloud','#ability# score is increased by 2 points','#ability# score is decreased by 2 points'],
  'ability': ['STR','DEX','CON','INT','WIS','CHA'],
}

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)

n = 'always'

while n == 'always':
  m = grammar.flatten("#sentence#")
  while len(m) > 140:
    m = grammar.flatten("#sentence#")
  try:
    print(m)
    #api.update_status(m)
  except tweepy.TweepError as e:
    print(e.reason)
  except StopIteration:
    break
  # do this every 2 hours.
  #sleep(7200)
