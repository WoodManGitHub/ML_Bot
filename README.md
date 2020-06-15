# ML_Bot
A simple discord ML bot.  
1. Chinese typo correction use [corrector](https://github.com/WoodManGitHub/corrector).
2. RAISR

# How to use
```
1. pip install -r requirements.txt
2. Add token to bot.py
3. python3 bot.py
```
Send pictures to bot with private message.  
Wait for Bot to send RAISR output picture.

# Model
RAISR: Filter for anime pictures.  
Corrector: BERT-Chinese

# Potential problems
1. The output image may exceed the Discord limit.
2. RAISR output time is too long.
