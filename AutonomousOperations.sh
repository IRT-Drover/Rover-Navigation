#!/bin/bash

echo Welcome to Drover
echo

# run to allow permission to run:
# ls -l filename.sh
# chmod 755 filename.sh

VEHICLE='rover'
FLIGHTSCRIPT='TestNavScript.py'
#FLIGHTSCRIPT='FieldNavScriptCopy.py'

prompt_err() {
  echo -e "COMMAND FAILED"
}

status() {
$1
if !( $? -eq 0 ); then
  prompt_err
  exit -1
fi
}

echo 'Setting up mavproxy...'
echo 'Setting up launch...'
# On Raspberry pi (linux)
lxterminal --command "cd /home/pi/Rover-Navigation && ./mavproxysetup.sh "$VEHICLE &
lxterminal --command "cd /home/pi/Rover-Navigation && ./takeoff.sh "$FLIGHTSCRIPT &

#On Mac
# osascript -e 'tell app "Terminal"
#   do script "cd /Users/charlesjiang/Downloads && ./mavproxysetup.sh drone"
#   do script "cd /Users/charlesjiang/Downloads && ./takeoff.sh SimpleTakeOffLand.py"
# end tell'

wait

if [ $VEHICLE == 'rover' ]; then
  echo '... NAVIGATION COMPLETE... DESTINATION REACHED'
elif [ $VEHICLE == 'drone' ]; then
  echo '... NAVIGATION COMPLETE... IMAGES AND FLIGHT DATA SAVED'
  ./imageprocessing.sh
fi
# Send coordinate data to computer on ground


# bad interpreter error because of differing carriage return characters:
# sed -i -e 's/\r$//' file.sh
