import csv
import codecs
import datetime

filename = "meetingAttendanceList_1.csv"
teacher = "Anju S Pillai"
with open(filename) as file:
    csvreader = csv.reader(codecs.open(filename, 'rU', 'utf-16'), delimiter='\t')
    lines = 0
    headings = []
    data = []
    for row in csvreader:
        if(lines == 0):
            headings = row
        else:
            data.append(row)
        lines += 1
    
    data = [i for i in data if teacher not in i[0]]
    
    data.sort(key=lambda x:x[0])
    
    ppl = []
    person = data[0][0]
    duration,start,end = datetime.timedelta(),0,0
    for i in range(len(data)):
        if(data[i][0] != person):
            if(start != 0 and end == 0):
                duration += datetime.timedelta(hours=1)
            seconds = duration.total_seconds()
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            
            ppl.append([data[i-1][0],hours,minutes,seconds])
            start = 0
            end = 0
            duration = datetime.timedelta()
            person = data[i][0]

        if(data[i][1] == 'Joined' or data[i][1] == 'Joined before'):
            start = datetime.datetime(day=int(data[i][2][:2]),month=int(data[i][2][3:5]),year=int(data[i][2][6:10]),hour=int(data[i][2][12:14]),minute=int(data[i][2][15:17]),second=int(data[i][2][18:]))
            
        elif(data[i][1] == 'Left'):
            end = datetime.datetime(day=int(data[i][2][:2]),month=int(data[i][2][3:5]),year=int(data[i][2][6:10]),hour=int(data[i][2][12:14]),minute=int(data[i][2][15:17]),second=int(data[i][2][18:]))
        
        if(start != 0 and end != 0):
            duration += end-start
            start = 0
            end = 0
    
    for i in ppl:
        print(i)
