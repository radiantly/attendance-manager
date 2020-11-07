import csv
import codecs
from pathlib import Path
from datetime import datetime, timedelta


def parseAttendanceCSV(filename):
    def parseGivenDate(datestring):
        for fmt in ["%m/%d/%Y, %I:%M:%S %p", "%m/%d/%Y, %H:%M:%S"]:
            try:
                return datetime.strptime(datestring, fmt)
            except ValueError:
                pass

    filePath = Path.cwd() / "uploads" / filename
    with open(filePath) as file:
        csvreader = csv.reader(codecs.open(filePath, "rU", "utf-16"), delimiter="\t")
        lines = 0
        headings = []
        data = []
        for row in csvreader:
            if lines == 0:
                headings = row
            else:
                data.append(row)
            lines += 1

        data = [i for i in data if "[" in i[0]]

        data.sort(key=lambda x: x[0])

        ppl = []
        person = data[0][0]
        duration, start, end = timedelta(), 0, 0
        for i in range(len(data)):
            if data[i][0] != person:
                if start != 0 and end == 0:
                    duration += timedelta(hours=1)
                seconds = duration.total_seconds()
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60

                ppl.append([data[i - 1][0], hours, minutes, seconds])
                start = 0
                end = 0
                duration = timedelta()
                person = data[i][0]

            if data[i][1] == "Joined" or data[i][1] == "Joined before":
                start = parseGivenDate(data[i][2])
            elif data[i][1] == "Left":
                end = parseGivenDate(data[i][2])

            if start != 0 and end != 0:
                duration += end - start
                start = 0
                end = 0
    return ppl