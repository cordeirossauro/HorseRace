#!/usr/bin/python3

import time
import os
import random
import numpy as np

def CountMoney():
    with open('money.txt', 'r') as f:
        money = float(f.readline())
        
    return money

def SaveMoney(Money):
    with open('money.txt', 'w') as f:
        f.write(str(Money))

def MountFullTrack(Positions, TrackSize):
    TrackTop = ('x' * TrackSize) + '\n' + '-' * TrackSize + '\n'
    TrackBottom = 'x' * TrackSize
    
    FullTrack = TrackTop
    HorseNumber = 1
    for Position in Positions:
        Position = int(Position)
        FullTrack = FullTrack + str(HorseNumber) + (' ' * Position) + 'ox' + (' ' * (TrackSize - Position)) + '\n' + ('-' * TrackSize) + '\n'
        HorseNumber = HorseNumber + 1
        
    FullTrack = FullTrack + TrackBottom
    return FullTrack

def PrintTrack(Positions, TrackSize):
    Track = MountFullTrack(Positions, TrackSize)
    print(Track)
   
def GenerateHorses(nHorses, SpeedLimit, EnergyLimit):
    Horses = np.empty((nHorses, 2))
    for HorseNumber in range(nHorses):
        Speed = random.random() * SpeedLimit + 2
        Energy = random.random() * EnergyLimit
        
        Horses[HorseNumber, 0] = Speed
        Horses[HorseNumber, 1] = Energy
        
    return Horses

def MoveHorses(OldPositions, Horses):
    Displacements = []
    for HorseNumber in range(len(Horses)):
        if Horses[HorseNumber, 1] > 0:
            Displacements = np.append(Displacements, Horses[HorseNumber, 0])
            Horses[HorseNumber, 1] = Horses[HorseNumber, 1] - 1
        else:
            Displacements = np.append(Displacements, int(Horses[HorseNumber, 0]/2))
    
    NewPositions = OldPositions + Displacements
    return NewPositions


def PrintOptions(Options):
    for Option in Options:
        print(Options[Option])


def BribeMenu(Horses):
    Options = {'tell': '- Pay him 200 credits to tell you the number of the three fastest horses in the race',
               'put': '- Pay him 500 credits to put redbull in one of the horses\' water (increases speed)',
               'return': '- Return'}
    
    Return = False
    TellDone = False
    PutDone = False
    while Return == False:
        os.system('clear')
        print('How would you like to bribe the worker?\n')
        PrintOptions(Options)
        Money = CountMoney()
        Choice = input('You currently have ' + str(Money) + ' credits, what would you like to do? (tell/put/return)\n').lower()

        
        if (Choice == 'tell') & (TellDone == False):
            if Money >= 200:
                FastestHorses = np.array(np.argsort(Horses[:, 0])[-3:])
                Money = Money - 200
                SaveMoney(Money)
                Options['tell'] = ('- The worker takes your money and slips you a note with some numbers written on it: ' + str(FastestHorses + 1))
                TellDone = True
            else:
                print('Sorry, you don\'t have enough money for that...')
                print('\n')
                time.sleep(2)
        elif (Choice == 'put') & (PutDone == False):
            if Money >= 500:
                print('The worker takes your money and asks you which horse should he give redbull to')
                RedBullHorse = int(input('Choose the horse (from 1 to 15):\n'))
                print('He nods and goes to the back of the track.\n')
                Horses[RedBullHorse - 1, 0] = Horses[RedBullHorse - 1, 0] + 5
                Money = Money - 500
                SaveMoney(Money)
                Options['put'] = '- The water of horse ' + str(RedBullHorse) + ' was replaced with Redbull'
                PutDone = True
            else:
                print('Sorry, you don\'t have enough money for that...')
                print('\n')
        elif Choice == 'return':
            Return = True
        else:
            print('Invalid choice, try again...')
            time.sleep(1)
    return Horses

def StartMenu(SpeedLimit = 5, EnergyLimit = 15, nHorses = 10):
    Horses = GenerateHorses(nHorses, SpeedLimit, EnergyLimit)
    Options = {'bet': '- Bet on a horse',
               'bribe': '- Bribe one of the workers (opens another menu)',
               'start': '- Start the race'}
    
    StartRace = False
    while StartRace == False:
        os.system('clear')
        print('Hello, and welcome to the horse race! (Please maximize your terminal for a better experice)\n')
        PrintOptions(Options)
        Money = CountMoney()
        Choice = input('You currently have ' + str(Money) + ' credits, what would you like to do? (bet/bribe/start)\n').lower()
        
        if Choice == 'bet':
            os.system('clear')
            NumberReceived = False
            while NumberReceived == False:
                BetNumber = int(input('Which horse are you betting on? (1 - 10)\n'))
                if (BetNumber <= len(Horses)) & (BetNumber > 0):
                    NumberReceived = True
                else:
                    print('That\'s not a valid horse number, try again')
                    
            AmountReceived = False
            while AmountReceived == False:
                BetAmount = float(input('How many credits will you bet? You have ' + str(Money) + '\n'))
                if BetAmount <= Money:
                    AmountReceived = True
                    Money = Money - BetAmount
                    SaveMoney(Money)
                    print('Alright! Your bet is officially done!')
                    print('Returning to the main menu now...')
                    time.sleep(3)
                else:
                    print('You don\'t have that much money, try again')
        

            
            Bet = BetAmount, BetNumber
            del Options['bet']
        elif Choice == 'bribe':
            Horses = BribeMenu(Horses)
            del Options['bribe']
            
        elif Choice == 'start':
            StartRace = True
            if 'bet' in Options.keys():
                Bet = -1, -1
            
        else:
            print('That\'s not a valid option, try again')
            time.sleep(1)
    return Horses, Bet


def Race(TrackSize = 150, nHorses = 10):
    Horses, Bet = StartMenu()
    BetAmount, BetNumber = Bet
    
    print('Very well, give us a second to prepare the race!')
    Positions = np.zeros(nHorses)
    isFinished = False
    time.sleep(2)
    
    os.system('clear')
    Countdown = [5,4,3,2,1]
    for Number in Countdown:
        print('All set! The race will start in ' + str(Number), end = '\r')
        time.sleep(1)
    os.system('clear')
    while isFinished == False:
        MountFullTrack(Positions, TrackSize)
        PrintTrack(Positions, TrackSize)
        time.sleep(0.2)
        Positions = MoveHorses(Positions, Horses)
        if Positions.max() >= TrackSize:
            isFinished = True
            os.system('clear')
            PrintTrack(Positions, TrackSize)
        if isFinished == False:
            os.system('clear')
            
    Winner = int(Positions.argmax() + 1)
    print('The race is over! Horse number ' + str(Winner) + ' is the winner!')
    if (BetNumber == Winner):
        print('Congratulations, your horse won the race!')
        print('Your bet of ' + str(BetAmount) + ' credits made you ' + str(BetAmount * 2) + ' credits!')
        Money = CountMoney()
        Money = Money + BetAmount * 2
        SaveMoney(Money)
    elif (BetNumber != -1):
        print('Oof! Your horse ' + str(BetNumber) + ' did not win the race... Better luck next time.')
    
def MainGame():
    RepeatRace = True
    while RepeatRace == True:
        Race()
        ValidInput = False
        while ValidInput == False:
            Input = input('Would you like to see another race? (yes/no)\n').lower()
            if Input in ['yes', 'y']:
                print('Very well, give us a second to organize the next race...')
                time.sleep(3)
                ValidInput = True
                RepeatRace = True
            elif Input in ['no', 'n']:
                print('Okay, see you next time!')
                time.sleep(3)
                ValidInput = True
                RepeatRace = False
            else:
                print('Invalid input, try again...')
                
MainGame()