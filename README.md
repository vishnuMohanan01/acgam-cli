## TODO
+ clean up fonts dir
+ 

## Requirements
+ Needs `PROGRAM_NAME` as env var.

## Read info
+ To generate certs we need,
  1. csv file path
  2. template name
  3. organization name
  4. name
  5. event name
  6. is winner
  7. position (if is winner)


## command call
childProcess.spawn('python3', [path.join(__dirname + '/../../scripts/main.py'), templateType, recipientType, eventName, filePath, user_name, email, actionTime, eventID, eventStartDate, isWinner]);

python3 main.py CS\ Template Participants Caffeinated\ Phase\ 1\ -\ Make\ Sript /home/vm/Desktop/Project/ieee-cs/ACGAM/acgam-express/fileSystem/97911a29participants.csv Vishnu\ Mohanan vishnumohanan@ieee.org Tue\ Jun\ 01\ 2021\ 16:20:00\ GMT+0000 591d3a64df574f68 2021-10-05 0
