#Standard Libraries
import time
import random
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
thisdir = os.path.dirname(os.path.abspath(__file__))
''' The program first uses the PickTest() function to randomly pick one of the available paragraphs pre-defined in a text file. These paragraphs can be added on the fly.
The PrepareTest() function finds the Normalization Factor - Since the length of words is not same for all words, this allows us to find the average length per word to have a more accurate reading of typing speed
The TakeTest() function starts a timer and then makes the user input the paragraph that they are supposed to. The timing is marked and the resultant answer and time taken are passes to AssessTest()
The AssessTest() function is the main function that analyses different parameters that the user needs measured.'''
def PickTest():
    #Modular Testing. Having a single file Twith all possible pre-defined tests allows us to add tests on the fly without hardcoding.
    textfilename =  os.path.join(thisdir,"Samples.txt")
    AllTests = open(textfilename,'r')

    #Convert all given tests in files as a list of strings
    PossibleTests = AllTests.readlines()
    AllTests.close()

    #Pick a random string from this list. This will be the paragraph the user writes.
    return (random.choice(PossibleTests)).encode().decode('unicode_escape')

def PrepareTest(TestList):
    TotalChars = 0
    NormalizationFactor = 0
    #Replace newline characters with empty, also count number of words.
    for i,word in enumerate(TestList):
        if "\n" in word:
            TestList[i] = word.replace('\n','')
        TotalChars += len(TestList[i])
    NormalizationFactor = TotalChars/len(TestList)
    return (NormalizationFactor)

def TakeTest():
    #Display the test to the user
    print("Your time begins now \n")
    print(SelectedTest)
    start_time = time.time()

    AnswerString = input()

    end_time = time.time()
    TimeTaken = end_time-start_time

    AnswerList = AnswerString.split(" ")
    return (AnswerList,TimeTaken)

def AssessTest(AnswerList,TimeTaken):
    CorrectWords = 0
    CorrectChars = 0
    Accuracy = 0
    ErrorPercent = 0
    NumofTypedWords = len(AnswerList)
    checkLimit = min(NumofTypedWords, len(TestList))
    for i in range(checkLimit):
        if (AnswerList[i] == TestList[i]):
            CorrectWords += 1
            CorrectChars += (len(AnswerList[i]) + 1)

    WPM = round(((CorrectChars/NormalizationFactor)/TimeTaken)*60)
    Accuracy = round(CorrectWords/NumofTypedWords*100)
    ErrorPercent = round(((abs(CorrectWords - len(TestList)))/len(TestList))*100)
    return(WPM, Accuracy, ErrorPercent)

def saveResults(score,wpm):
    print("Saving Results...")
    csvfilename =  os.path.join(thisdir,"Leaderboards.csv")
    leadf = pd.read_csv(csvfilename)
    username = input("Enter your username: ")
    if (username in leadf['Name'].values):
        idx = leadf.index[leadf['Name']==username][0]
        newHistory = eval(leadf.at[idx,'History'])
        newHistory.append(wpm)
        leadf.at[idx,'History'] = newHistory
        if(score > leadf.at[idx,'Highscore']):
            leadf.at[idx,'Highscore'] = score
        print("Score Updated!")
    else:
        newUser = {'Name':username, 'Highscore':score, 'History':[wpm]}
        leadf = leadf._append(newUser,ignore_index = True)
        print("New user created!")
    leadf = leadf.sort_values('Highscore', ascending = False)
    leadf.to_csv(csvfilename,index=False)

def viewGraph(userName):
    csvfilename = os.path.join(thisdir,'Leaderboards.csv')
    df = pd.read_csv(csvfilename)
    if (userName in df["Name"].values):
        idx = df.index[df["Name"]==userName][0]
        ypoints = eval(df.at[idx,'History'])
        xpoints = range(1, len(ypoints)+1)
        plt.plot(xpoints, ypoints)
        plt.xticks(xpoints)
        plt.show()
    else:
        print("Username does not exist!")
    
userChoice = input("Do you want to give test? Y/N ")
if userChoice.lower() == 'y':
    SelectedTest = PickTest()
    #Convert selected test to a list of words so we can compare user input
    TestList = SelectedTest.split(" ")
    NormalizationFactor = PrepareTest(TestList)
    AnswerList, TimeTaken = TakeTest()
    WPM, Accuracy, ErrorPercent = AssessTest(AnswerList,TimeTaken)
    userScore = round(((1-(ErrorPercent/100)) * WPM))
    print("Your speed in words per minute is: ", WPM)
    print("Accuracy: ",Accuracy,"%")
    print("Error Percent: ", ErrorPercent,"%")
    print("Score: ", userScore)
    print()
    userChoice = input("Do you want to save results? Y/N: ")
    if userChoice.lower() == 'y':
        saveResults(userScore,WPM)
    else:
        print("Not saving results")
else:
    print("Not Attempting Test")

userChoice = input("Do you want to view graph of history? Y/N ")
if  userChoice.lower() == 'y':
    name = input("Enter your username: ")
    viewGraph(name)
    del name
else:
    print("Not showing graph")