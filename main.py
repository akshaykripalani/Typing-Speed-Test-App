#Standard Libraries
import time
import random
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
thisdir = os.path.dirname(os.path.abspath(__file__))

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

def TakeTest(SelectedTest):
    #Display the test to the user
    start_time = time.time()
    AnswerString = simpledialog.askstring(title="Test Window", prompt = "Press Enter to submit\n\n"+SelectedTest)
    end_time = time.time()
    TimeTaken = end_time-start_time
    AnswerList = AnswerString.split(" ")
    return (AnswerList,TimeTaken)

def AssessTest(AnswerList,TimeTaken,NormalizationFactor, TestList):
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
    username = simpledialog.askstring(title="Save Results", prompt ="Enter your username: ")
    if (username in leadf['Name'].values):
        idx = leadf.index[leadf['Name']==username][0]
        newHistory = eval(leadf.at[idx,'History'])
        newHistory.append(wpm)
        leadf.at[idx,'History'] = newHistory
        if(score > leadf.at[idx,'Highscore']):
            leadf.at[idx,'Highscore'] = score
        messagebox.showinfo(title="Success", message="Score Updated!")
    else:
        newUser = {'Name':username, 'Highscore':score, 'History':[wpm]}
        leadf = leadf._append(newUser,ignore_index = True)
        messagebox.showinfo(title="Success", message="New User Created!")
    leadf = leadf.sort_values('Highscore', ascending = False)
    leadf.to_csv(csvfilename,index=False)

def viewGraph():
    userName = simpledialog.askstring(title="View History", prompt="Enter your username: ")
    csvfilename = os.path.join(thisdir,'Leaderboards.csv')
    df = pd.read_csv(csvfilename)
    if (userName in df["Name"].values):
        idx = df.index[df["Name"]==userName][0]
        ypoints = eval(df.at[idx,'History'])
        xpoints = range(1, len(ypoints)+1)
        temp = [30,40,50,60,70,80,90,100,110,120,130,140,150]

        graph_window = tk.Toplevel(master=window)
        graph_window.title("Graph")

        fig = plt.figure(figsize=(5,5), dpi=100)
        plt.plot(xpoints, ypoints)
        plt.xticks(xpoints)
        plt.yticks(temp)

        btn_delete = tk.Button(master=graph_window, 
                               text="Close Window", 
                               command=graph_window.destroy)
        btn_delete.pack()

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    else:
        messagebox.showerror(title="Error!", message="Username does not exist!")
    
def handleTest():
    SelectedTest = PickTest()
    #Convert selected test to a list of words so we can compare user input
    TestList = SelectedTest.split(" ")
    NormalizationFactor = PrepareTest(TestList)
    AnswerList, TimeTaken = TakeTest(SelectedTest)
    WPM, Accuracy, ErrorPercent = AssessTest(AnswerList,TimeTaken,NormalizationFactor, TestList)
    userScore = round(((1-(ErrorPercent/100)) * WPM))
    
    wpmresults = "Your speed in words per minute is: " + str(WPM)
    accresults = "\nAccuracy: " +str(Accuracy)+"%"
    errresults = "\nError Percent: "+ str(ErrorPercent)+"%"
    scoreresults = "\nScore: "+ str(userScore)

    userChoice = messagebox.askquestion(title = "Results", 
                                        message = wpmresults+accresults+errresults+scoreresults+"\n\nDo you want to save results?")

    if userChoice == 'yes':
        saveResults(userScore,WPM)
    else:
        messagebox.showinfo(title="Message", message="Not saving results")

def main(): 
    global window
    window = tk.Tk()
    window.geometry("1280x720")
    window.configure(bg='#161d20')

    frm_testing = tk.Frame(master=window, bg='#2d7c9d')
    btn_testing = tk.Button(master=frm_testing,
                            takefocus=True, 
                            text='Take Test',
                            command=handleTest, 
                            height = 20, 
                            width = 40, 
                            bg='#2d7c9d', 
                            fg='#cccccc', 
                            relief=tk.FLAT)

    btn_testing.pack()
    frm_testing.pack(side=tk.LEFT, anchor=tk.CENTER, padx = (250,0))

    frm_graphing = tk.Frame(master=window)
    btn_graphing = tk.Button(master=frm_graphing,
                             takefocus=True, 
                             text='View History',
                             command=viewGraph, 
                             height = 20, 
                             width = 40, 
                             bg='#2d7c9d', 
                             fg='#cccccc', 
                             relief = tk.FLAT)

    btn_graphing.pack()
    frm_graphing.pack(side=tk.RIGHT, anchor=tk.CENTER, padx = (0,250))

    btn_close = tk.Button(text="Close", 
                          command=window.quit, 
                          bg='#36498f', 
                          fg='#cccccc', 
                          relief = tk.FLAT)
    btn_close.place(relx=0.98, rely=0.02, anchor='ne')

    window.resizable(False,False)
    window.mainloop()

if (__name__ ==  '__main__'):
    main()