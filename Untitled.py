#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Standard Libraries
import time
import random
import pandas as pd
import matplotlib as plt
''' The program first uses the PickTest() function to randomly pick one of the available paragraphs pre-defined in a text file. These paragraphs can be added on the fly.
The PrepareTest() function finds the Normalization Factor - Since the length of words is not same for all words, this allows us to find the average length per word to have a more accurate reading of typing speed
The TakeTest() function starts a timer and then makes the user input the paragraph that they are supposed to. The timing is marked and the resultant answer and time taken are passes to AssessTest()
The AssessTest() function is the main function that analyses different parameters that the user needs measured.'''
def PickTest():
    #Modular Testing. Having a single file with all possible pre-defined tests allows us to add tests on the fly without hardcoding.
    AllTests = open('Samples.txt','r')

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
            CorrectChars += len(AnswerList[i]) + 1 #+1 to account for additional space at the end of the word.

    WPM = round(((CorrectChars/NormalizationFactor)/TimeTaken)*60)
    Accuracy = round(CorrectWords/NumofTypedWords*100)
    ErrorPercent = round(((abs(CorrectWords - len(TestList)))/len(TestList))*100,2)
    return(WPM, Accuracy, ErrorPercent)

SelectedTest = PickTest()
#Convert selected test to a list of words so we can compare user input
TestList = SelectedTest.split(" ")
NormalizationFactor = PrepareTest(TestList)
AnswerList, TimeTaken = TakeTest()
WPM, Accuracy, ErrorPercent = AssessTest(AnswerList,TimeTaken)
userScore = ((1-(ErrorPercent/100)) * WPM)
print("Your speed in words per minute is: ", WPM)
print("Accuracy: ",Accuracy,"%")
print("Error Percent: ", ErrorPercent,"%")
print("Score: ", userScore)