Cyber Intelligent Automata (CIA) is a discord.py bot integrated with a Tensorflow ML chatbot. I modified the baseline code from Tech with Tim's chatbot tutorial.

This bot is intended to facilitate and provide hints for CTF challenges in UCSD's ACM Cyber Discord Server. To ensure the privacy of the CTF flags, index.JSON (the file containing the CTF-related data that the chatbot trains on) will not be pushed to this repository. Also, main.py will have some sections redacted that perform flag checking. 

To run this discord.py bot, install PyCharm and Anaconda. Then, run the command "create -n chatbot python=3.6" in windows command prompt, creating a conda env called chatbot. Then, type "activate chatbot" in the command prompt to activate the environment.

Then, install tensorflow, tflearn, numpy, nltk, and discord.py, all using pip.

Lastly, I didn't upload my token.txt for privacy reasons, but please create a bot in the discord developer portal and put its token in that file.
