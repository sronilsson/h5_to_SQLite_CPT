import sqlite3
import pandas as pd
from tqdm import tqdm


filename = 'Outfile.csv'

def findHits():
    outcomeList = []
    duringStimList = []
    windowList4 = []
    windowList5 = []
    windowList6 = []
    windowList7 = []
    afterSimList1 = []
    afterSimList2 = []
    afterSimList3 = []
    afterSimList4 = []
    afterSimList5 = []
    afterSimList6 = []
    afterSimList7 = []
    afterSimList8 = []
    afterSimList9 = []
    afterSimList10 = []
    afterSimList11 = []
    afterSimList12 = []
    afterSimList13 = []
    afterSimList14 = []
    afterSimList15 = []
    afterSimList16 = []
    recodingNecessery = 0
    conn = sqlite3.connect('fiber.db', isolation_level=None)
    c = conn.cursor()
    c.execute("PRAGMA TEMP_STORE = OFF")
    c.execute("PRAGMA SYNCHRONOUS = OFF")
    c.execute("PRAGMA JOURNAL_MODE = OFF")
    hitEvent = str('HIT')
    missEvent = str('MISS')
    crEVENT = str('CORRECT REJECTION')
    frEVENT = str('FALSE ALARM')
    stimONevent = str('STIMULUS ON')
    stimONrows = c.execute("SELECT Flour_Sync_Time FROM JoinedTable WHERE Event = ?", (stimONevent,))
    stimONrows = stimONrows.fetchall()
    stimOFFevent = str('STIMULUS OFF')
    stimOFFrows = c.execute("SELECT Flour_Sync_Time FROM JoinedTable WHERE Event = ?", (stimOFFevent,))
    stimOFFrows = stimOFFrows.fetchall()

    #CORRECTION FOR INITALLY BAD CODING
    if not tqdm(stimONrows):
        print('NO STIM ON recordings, FIXING IT....')
        stimONrows = []
        recodingNecessery = 1
        for i in stimOFFrows[::2]:
            value = i[0]
            stimONrows.append(value)
        stimOFFrows = stimOFFrows[1::2]
    loop = 0
    if len(stimONrows) != len(stimOFFrows):
        stimONrows = stimONrows[:-1]
    trialOutcome = c.execute("SELECT Event FROM JoinedTable WHERE (Event = ? OR Event = ? OR Event = ? OR Event = ?)",(hitEvent, missEvent, crEVENT, frEVENT))
    trialOutcome = trialOutcome.fetchall()

    # RAW AVERAGE FLOURECENCE 2s-Windows BEFORE EACH TRIAL ONSET AN TRIAL OUTCOME
    print(stimONrows)
    print(stimOFFrows)

    for i in tqdm(stimONrows):
        if recodingNecessery == 1:
            stimONtime = float(i)
        if recodingNecessery == 0:
            stimONtime = float(i[0])
        stimOFFtime = stimOFFrows[loop]
        stimOFFtime = float(stimOFFtime[0])
        outcome = trialOutcome[loop]
        outcome = outcome[0]
        outcomeList.append(outcome)

        window4startTime = stimONtime - 0.8
        window4endTime = stimONtime - 0.6
        window4 = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)",(window4endTime, window4startTime))
        window4 = window4.fetchone()
        window4 = float(window4[0])
        windowList4.append(window4)

        window5startTime = stimONtime - 0.6
        window5endTime = stimONtime - 0.4
        window5 = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)",(window5endTime, window5startTime))
        window5 = window5.fetchone()
        window5 = float(window5[0])
        windowList5.append(window5)

        window6startTime = stimONtime - 0.4
        window6endTime = stimONtime - 0.20
        window6 = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)",(window6endTime, window6startTime))
        window6 = window6.fetchone()
        window6 = float(window6[0])
        windowList6.append(window6)

        window7startTime = stimONtime - 0.20
        window7endTime = stimONtime
        window7 = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)", (window7endTime, window7startTime))
        window7 = window7.fetchone()
        window7 = float(window7[0])
        windowList7.append(window7)

        # # During stimulus presentation
        duringStim = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)",(stimOFFtime, stimONtime))
        duringStim = duringStim.fetchone()
        duringStim = float(duringStim[0])
        duringStimList.append(duringStim)

        # After trial 1 0-0.2
        begin = stimOFFtime
        end = begin + 0.2
        afterStim = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)", (end, begin))
        afterStim = afterStim.fetchone()
        afterStim = float(afterStim[0])
        afterSimList1.append(afterStim)

        # After trial 2 0.2-0.4
        begin = stimOFFtime + 0.2
        end = begin + 0.2
        afterStim = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)", (end, begin))
        afterStim = afterStim.fetchone()
        afterStim = float(afterStim[0])
        afterSimList2.append(afterStim)

        # After trial 3 0.4-0.6
        begin = stimOFFtime + 0.4
        end = begin + 0.2
        afterStim = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)",(end, begin))
        afterStim = afterStim.fetchone()
        afterStim = float(afterStim[0])
        afterSimList3.append(afterStim)

        # After trial 4 - 0.6-0.8
        begin = stimOFFtime + 0.6
        end = begin + 0.2
        afterStim = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)", (end, begin))
        afterStim = afterStim.fetchone()
        afterStim = float(afterStim[0])
        afterSimList4.append(afterStim)

        # After trial 5 0.8-1.0
        begin = stimOFFtime + 0.8
        end = begin + 0.2
        afterStim = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)",(end, begin))
        afterStim = afterStim.fetchone()
        afterStim = float(afterStim[0])
        afterSimList5.append(afterStim)

        # After trial 6 1.0-1.2
        begin = stimOFFtime + 1.0
        end = begin + 0.2
        afterStim = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)",(end, begin))
        afterStim = afterStim.fetchone()
        afterStim = float(afterStim[0])
        afterSimList6.append(afterStim)

        # After trial 7 - 1.2-1.4
        begin = stimOFFtime + 1.2
        end = begin + 0.2
        afterStim = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)", (end, begin))
        afterStim = afterStim.fetchone()
        afterStim = float(afterStim[0])
        afterSimList7.append(afterStim)

        # After trial 8 - 1.4-1.6
        begin = stimOFFtime + 1.4
        end = begin + 0.2
        afterStim = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)",(end, begin))
        afterStim = afterStim.fetchone()
        afterStim = float(afterStim[0])
        afterSimList8.append(afterStim)

        # After trial 9 - 1.6-1.8
        begin = stimOFFtime + 1.6
        end = begin + 0.2
        afterStim = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)",(end, begin))
        afterStim = afterStim.fetchone()
        afterStim = float(afterStim[0])
        afterSimList9.append(afterStim)

        #After trial 10 - 1.8-2.0
        begin = stimOFFtime + 1.8
        end = begin + 0.2
        afterStim = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)",(end, begin))
        afterStim = afterStim.fetchone()
        afterStim = float(afterStim[0])
        afterSimList10.append(afterStim)

        #After trial 11 - 2.0-2.2
        begin = stimOFFtime + 2.0
        end = begin + 0.2
        afterStim = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)",(end, begin))
        afterStim = afterStim.fetchone()
        afterStim = float(afterStim[0])
        afterSimList11.append(afterStim)

        #After trial 12 - 2.2-2.4
        begin = stimOFFtime + 2.2
        end = begin + 0.2
        afterStim = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)",(end, begin))
        afterStim = afterStim.fetchone()
        afterStim = float(afterStim[0])
        afterSimList12.append(afterStim)

        #After trial 13 - 2.4-2.6
        begin = stimOFFtime + 2.4
        end = begin + 0.2
        afterStim = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)",(end, begin))
        afterStim = afterStim.fetchone()
        afterStim = float(afterStim[0])
        afterSimList13.append(afterStim)

        #After trial 14 - 2.6-2.8
        begin = stimOFFtime + 2.6
        end = begin + 0.2
        afterStim = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)",(end, begin))
        afterStim = afterStim.fetchone()
        afterStim = float(afterStim[0])
        afterSimList14.append(afterStim)

        #After trial 15 - 2.8-3.0
        begin = stimOFFtime + 2.8
        end = begin + 0.2
        afterStim = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)",(end, begin))
        afterStim = afterStim.fetchone()
        afterStim = float(afterStim[0])
        afterSimList15.append(afterStim)

        # After trial 15 - 2.8-3.0
        begin = stimOFFtime + 3.0
        end = begin + 0.2
        afterStim = c.execute("SELECT AVG(Flourescence) FROM JoinedTable WHERE (Flour_Sync_Time < ? AND Flour_Sync_Time > ?)", (end, begin))
        afterStim = afterStim.fetchone()
        afterStim = float(afterStim[0])
        afterSimList16.append(afterStim)

        loop += 1

    binWindows = pd.DataFrame(windowList4)
    binWindows['0.6-0.4'] = pd.DataFrame(windowList5)
    binWindows['0.4-2'] = pd.DataFrame(windowList6)
    binWindows['0.2-0'] = pd.DataFrame(windowList7)
    binWindows['STIMULUS'] = pd.DataFrame(duringStimList)
    binWindows['0-0.2'] = pd.DataFrame(afterSimList1)
    binWindows['0.2-0.4'] = pd.DataFrame(afterSimList2)
    binWindows['0.4-0.6'] = pd.DataFrame(afterSimList3)
    binWindows['0.6-0.8'] = pd.DataFrame(afterSimList4)
    binWindows['0.8-1.0'] = pd.DataFrame(afterSimList5)
    binWindows['1.0-1.2'] = pd.DataFrame(afterSimList6)
    binWindows['1.2-1.4'] = pd.DataFrame(afterSimList7)
    binWindows['1.4-1.6'] = pd.DataFrame(afterSimList8)
    binWindows['1.6-1.8'] = pd.DataFrame(afterSimList9)
    binWindows['1.8-2.0'] = pd.DataFrame(afterSimList10)
    binWindows['2.0-2.2'] = pd.DataFrame(afterSimList11)
    binWindows['2.2-2.4'] = pd.DataFrame(afterSimList12)
    binWindows['2.4-2.6'] = pd.DataFrame(afterSimList13)
    binWindows['2.6-2.8'] = pd.DataFrame(afterSimList14)
    binWindows['2.8-3.0'] = pd.DataFrame(afterSimList15)
    binWindows['3.0-3.2'] = pd.DataFrame(afterSimList16)
    binWindows['OUTCOME'] = pd.DataFrame(outcomeList)

    binWindows.to_csv(filename)


findHits()