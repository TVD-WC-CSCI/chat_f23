'''
Created on May 30, 2023

Structure and other ideas taken from https://github.com/wadetb/eliza

@author: tvandrun
'''

import re
import random


# Make a function that will perform a regex replacement.
# Given two regular expressions, make a function that will
# take a string and test whether it has a match for the first
# regex, and, if so, will replace it using the other regex.
def replacement(reSearch, reReplace) :
    return lambda str : re.sub(reSearch, reReplace, str) if re.search(reSearch, str) else None

# Like replacement, but for the case where there are
# several substitutions to be made
def pattern_response(reSearch, response_orig) :
    def ff(str):
        match = re.search(reSearch, str)
        if match :
            replacements = match.groupdict()
            response = response_orig
            for x in replacements :
                response = re.sub(x, replacements[x], response)
            return response
        else :
            return None
    return ff

last_resort = ["I'm not sure I understand you.", 
               "Go on.", 
               "Perhaps we should change the subject.",
               "What does that suggest to you?", 
               "Are you sure?"]

basicSubList = [(r'\bI was\b', "you were"), (r"\bI wasn't\b", "you weren't"), (r'\bme\b', "you"), (r'\bmy\b', "your"), (r'\bmine\b', "yours"), ("(i|I)\'m", "you are"), (r'\b(i|I)\b', "you"), (r'\bam\b', "are"), 
                (r'\byou\b', "me"), (r'\byours\b', "mine"), (r'\byour\b', "my"), (r'\bare\b', "to be"), (r'\bcan\'t\b', "can not"), (r'\W$', "")]                       
                       
basicSubs = [replacement(basicSubList[i][0], "X%sX" % i) for i in range(len(basicSubList))] + [replacement("X%sX" % i, basicSubList[i][1]) for i in range(len(basicSubList))]


rule_regexes = [(r'you are sorry', 'You have nothing to apologize for.'),
                (r'you (dreamed|dreamt) that (?P<xxx>.*$)', 'Had you ever dreamt that xxx before?'),
                (r'[pP]ython', 'Do you mean the snake, the language, or the Monty?'),
                (r'dream', 'Tell me more about your dreams.'),
                ('(egg|pancake|waffle|cereal|bacon|toast)', 'Do you usually have a good breakfast?'),
                ('(dream|sleep)', "It's important to get a good night of rest."),
                (r'my(?P<xxx>father|dad|mother|mom|brother|sister|friend|roommate|chapel buddy)', r'Do you get along with your xxx?'),
                (r'(all|any|every)', 'Can you think of a specific example?'),
                (r'(alike|similar|same)', 'In what way are they alike?'),
                (r'me to be (a|an) (bot|agent|computer)', 'Does it bother you that you are talking to a chatbot?'),
                (r'you are (?P<xxx>depressed|sad|hungry|tired|angry|unhappy)', r'I am sorry to hear you are xxx'),
                (r'you are (?P<xxx>tired|exhausted|worn out)', r'What is making you so xxx?')]

rules = [pattern_response(p, q) for (p, q) in rule_regexes]



print("Please chat with me.")

while True :
    given = input()
    if not given:
        print("Please talk to me")
        continue
    # Make some modifications to the input
    given = given[0].lower() + given[1:]
    for sub in basicSubs :
        revised = sub(given)
        if revised :
            given = revised
    
    response = None
    
    random.shuffle(rules)
    for rule in rules :
        if not response :
            response = rule(given)
    
    if not response:
        response = random.choice(last_resort)
    
    print(response)
