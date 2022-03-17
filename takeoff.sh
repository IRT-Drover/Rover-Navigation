#!/bin/bash

FLIGHTSCRIPT=$1
cd /home/pi/Desktop

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

echo
echo 'Connect Mission Planner before preceding'
echo
echo 'READY TO EXECUTE TAKEOFF SCRIPT...' $FLIGHTSCRIPT
echo
echo "Type 'takeoff' when ready to arm and takeoff or 'q' to cancel..."
echo "Then, arm vehicle in mission planner or type 'arm throttle force' in the mavproxysetup window..."
read -p '>>> ' TAKEOFFVAR

while [[ $TAKEOFFVAR != 'takeoff' && $TAKEOFFVAR != 'q' ]]
  do
    echo 'Error: invalid input'
    read -p '>>> ' TAKEOFFVAR
  done

if [ $TAKEOFFVAR == 'takeoff' ]; then
  echo '||>>>RUNNING TAKEOFF SCRIPT<<<||'
  status 'python '$FLIGHTSCRIPT' --connect udp:127.0.0.1:14551'

elif [ $TAKEOFFVAR == 'cancel' ]; then
  exit -1
fi