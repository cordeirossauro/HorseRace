# Horse Race
Simple game written in python that simulates a horse race and allows the player to bet on a horse.
<img src="https://media.giphy.com/media/4N5Us2tO1QN5zYvfRt/giphy.gif"/>
# Instructions
Just download the ZIP file, extract it and run HorseRace.py from the terminal with
```
$ python3 HorseRace.py
```
From there, just follow the instructions on screen and you will be good to go!

If there are any missing libraries (very unlikely, since the game only uses a couple), you can install them with:

```
$ pip3 install -r requirements.txt
```

# Game Principle
Everytime a new race starts, the game creates 10 horses and randomly generates two attributes for each one:

- Speed (Between 2 and 12): The amount of spaces a horse can move in a single time step;
- Energy (Between 0 and 10): The amount of moves a horse can make before it gets tired.

After that, all horses go to the starting line and the race happens following the loop:

1. All horses move according to their speed;
2. All horses lose 1 point of energy;
3. If a horse becomes tired (Energy = 0), it loses half of its speed for the rest of the race;

Steps 1, 2 and 3 are repeated until one of the horses reaches the finish line.

# Details
Created by: Vinicius Cordeiro
