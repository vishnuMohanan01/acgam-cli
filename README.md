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