# myconigen
5e focused random mushroom generator.

This is the brain behind the Twitter bot @MagicMyco, which tweets random fantasy mushrooms every two hours. 

If you want to make your own bot, you can use this as an example. The only thing missing from the source tree is the secrets.py file which contains Twitter credentials. The contents of that file are simple enough (supply your own credentials after signing up on Twitter and creating a new app at apps.twitter.com):

```
consumer_key = 'nnnnnnnnnnnnnnn'
consumer_secret = 'nnnnnnnnnnnnnnn'
access_token = 'nnnnnnnnnnnnnnn'
access_secret = 'nnnnnnnnnnnnnnn'
```

If you want to make suggestions for improvement, I have a few areas of definite interest:

1. More concise language to get more variety under the 140 character limit.
2. More descriptive options for tasteless and inedible mushrooms.
3. More mushroom name parts (if you dig, you can see that I used D&D monster names in addition to various real-world mushroom names).
4. A wider range of possible magical and/or mundane effects.

As for extensions, I am inclined to see whether and to what extent I can have the bot autorespond to people who query it, to give it a layer of interactivity. For instance, if you see a mushroom that sounds interesting, you could @ the bot with an action and perhaps a CON ability score, then the bot could come back with a filled in roll for that mushroom. What other interactive possibilities are there?
