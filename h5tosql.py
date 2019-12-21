import h5py as h5
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sqlite3
import warnings
from tqdm import tqdm

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore")
setBinSize = 15
decreaseTTLforOverlap = 15000
loop = 0

eventLogFile = 'Animal_3-20180901-143642_eventlog.csv'
flourTTLCSV = 'flour_TTL.csv'

# READ IN FLOUR SIGNAL AND TTL DATA AND TIMESTAMPS FOS SYNCING
with h5.File("Mouse3_Day3_0001.h5", "r") as dataH5:
    collectionHz = int(dataH5['header/AcquisitionSampleRate'][0])
    print('COLLECTION HZ = ' + str(collectionHz))
    rawFluorescent = (dataH5['sweep_0001/analogScans'][0])
    rawFluorescent = pd.DataFrame(rawFluorescent)
    rawTTL = dataH5['sweep_0001/analogScans'][1]
    rawTTL = (pd.DataFrame(rawTTL)) / decreaseTTLforOverlap
    flour_TTL = pd.concat([rawTTL, rawFluorescent], axis=1, join_axes=[rawFluorescent.index])
    flour_TTL.columns = ['TTL', 'Flour']
    flour_TTL['h'] = flour_TTL.index / collectionHz
    flour_TTL['TTL_STATUS'] = np.where(flour_TTL['TTL'] > 1.0, 1, 0)
    flour_TTL['TTL'] = flour_TTL['TTL_STATUS'].diff()
    flour_TTL['HIT'] = np.where(flour_TTL['TTL_STATUS'] > 0.9, 'HIT', '')

    flour_TTL['TTL'] = flour_TTL['TTL'].replace(to_replace=-1,value='TTL_OFF')
    sumTTLs = (flour_TTL['TTL'] == 'TTL_OFF').sum()
    print(str('TTL PULSES = ') + (str(sumTTLs)))
    flour_TTL['TTL'] = flour_TTL['TTL'].replace(to_replace=1, value='TTL_ON')
    flour_TTL['TTL'] = flour_TTL['TTL'].replace(to_replace=0, value='')

    dataH5.close()

firstHitRow = np.argmax(flour_TTL['TTL'] == 'TTL_ON')
flour_TTL['SYNC_TIME1'] = ''
timeZero = flour_TTL['h'].iloc[firstHitRow]
flour_TTL['SYNC_TIME1'] = (flour_TTL['h'] - timeZero)


# READ IN BEHAVIOUR DATA AND CALCULATE TIMESTAMPS FOS SYNCING
eventsLog = pd.read_csv(eventLogFile, sep='\t', skiprows=1)
eventsLog.columns = ['EVENT', 'EVENT_TIME', 'ARDUINO_TIME', 'NONSENSE']
eventsLog = eventsLog.drop(columns='NONSENSE')
eventsLog['EVENT_TIME'] = eventsLog['EVENT_TIME'] / 1000
firstHitRow = np.argmax(eventsLog['EVENT'] == 'HIT')
eventsLog['SYNC_TIME2'] = ''
timeZero = eventsLog['EVENT_TIME'].iloc[firstHitRow]
eventsLog['SYNC_TIME2'] = (eventsLog['EVENT_TIME'] - timeZero) * 1000
sumHits = (eventsLog['EVENT'] == 'HIT').sum()
print(str('HITS = ') + (str(sumHits)))

# EXPORT TABLES TO SQL AND LEFT OUTER JOIN
conn = sqlite3.connect('Fiber.db')
c = conn.cursor()
eventsLog.to_sql('EventsLog', conn, if_exists='replace')
flour_TTL.to_sql('Flour_TTL', conn, if_exists='replace')
if collectionHz == 10000:
    c.execute("UPDATE Flour_TTL SET SYNC_TIME1 = ROUND(SYNC_TIME1, 10)")
    c.execute("UPDATE EventsLog SET SYNC_TIME2 = ROUND(SYNC_TIME2, 10)")
if collectionHz == 1000:
    c.execute("UPDATE Flour_TTL SET SYNC_TIME1 = ROUND(SYNC_TIME1, 3)")
    c.execute("UPDATE EventsLog SET SYNC_TIME2 = ROUND(SYNC_TIME2, 3)")
joining = c.execute("SELECT EventsLog.EVENT, EventsLog.EVENT_TIME, h, EventsLog.SYNC_TIME2, SYNC_TIME1, Flour, TTL_STATUS FROM flour_TTL LEFT OUTER JOIN EventsLog ON flour_TTL.SYNC_TIME1 = EventsLog.SYNC_TIME2")
joining = joining.fetchall()
c.execute('DROP TABLE IF EXISTS JoinedTable')
c.execute("CREATE TABLE JoinedTable (Event text, TTL_Status text, Flourescence integer, Event_Sync_Time integer, Flour_Sync_Time integer, Event_Time integer, Flour_Time integer)")
for i in tqdm(joining):
    Event, EVENT_TIME, h, SYNC_TIME2, SYNC_TIME1, Flour, TTL_STATUS = joining[loop]
    c.execute("INSERT INTO JoinedTable (Event, Event_Time, Flour_Time, Event_Sync_Time, Flour_Sync_Time, Flourescence, TTL_Status) VALUES (?,?,?,?,?,?,?)", (Event, EVENT_TIME, h, SYNC_TIME2, SYNC_TIME1, Flour, TTL_STATUS))
    loop += 1
conn.commit()

#BIN DATA BY SECONDS
maxSeconds = flour_TTL['h'].max()
minSeconds = flour_TTL['h'].min()
binSize = maxSeconds / setBinSize
bins = np.linspace(minSeconds, maxSeconds, binSize)
groups = flour_TTL.groupby(pd.cut(flour_TTL['h'], bins))
binsFlour = (groups['Flour'].mean())

#PLOT TTL / DATA
binsFlour.plot.line()
plt.show()

