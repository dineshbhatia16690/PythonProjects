import re
from datetime import datetime

global invalidRecordCounter
invalidRecordCounter = 0
path = "./sample"    # Please change the path according to the file's location

global dataDictionary
dataDictionary = {}

# validate the record for no. of fields and ID
def isValidRecord(line):
    global invalidRecordCounter
    record = line.strip().split(" ", 1)
    record_id = int(record[0].strip())

    if record_id <= 0:
        invalidRecordCounter += 1
        return

    date_record = record[1].strip().split(" ", 1)
    date = date_record[0].strip()

    if isValidDate(date) is False:
        invalidRecordCounter += 1
        return

    remaining_record = date_record[1].strip()
    formatted_remaining = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', remaining_record)
    string2 = formatted_remaining[1]

    if len(formatted_remaining) != 3:
        invalidRecordCounter += 1
        return
    else:
        if record_id in dataDictionary:
            dataDictionary[record_id].append(string2)
        else:
            dataDictionary[record_id] = [string2]

# verify the date is in valid format
def isValidDate(date_input):
    try:
        datetime.strptime(date_input, '%Y-%m-%d-%H:%M:%S')
        return True
    except ValueError:
        return False


# Pass the text from a file
print "Begin ..."
record_file = open(path, 'r')
records = [record.rstrip('\n') for record in record_file]

for record in records:
    isValidRecord(record)

print("Total invalid records: " + str(invalidRecordCounter))
userinputs = raw_input("Please enter the IDs separated by a comma: ")
userinputs_list = userinputs.split(",")
requested_id_list = []

# loop through ID's provided by user and store it in a list
for userinput in userinputs_list:
    try:
        requested_id_list.append(int(userinput.strip()))
    except ValueError:
        print "Invalid input"

for id_requested in requested_id_list:
    try:
        for str2 in dataDictionary[id_requested]:
            print str(id_requested) + ", " + str2
    except KeyError:
        print "ID not found: ", id_requested