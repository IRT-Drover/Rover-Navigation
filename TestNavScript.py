from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
from pygeodesy.ellipsoidalVincenty import LatLon
from pygeodesy import Datums
import time

import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


# Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

# Function to arm
def arm():

  print("Basic pre-arm checks")
  # Don't let the user try to arm until autopilot is ready
  while not vehicle.is_armable:
    print(" Waiting for vehicle to initialise...")
    time.sleep(1)

  print("Arming motors")
  # Copter should arm in GUIDED mode
  vehicle.mode    = VehicleMode("GUIDED")
  vehicle.armed   = True

  while not vehicle.armed:
    print(" Waiting for arming...")
    time.sleep(1)

  # THIS SECTION NOT RELEVANT TO ROVER (takeoff and altitude check only make sense for copter)

  # print("Taking off!")
  # vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

  # Check that vehicle has reached takeoff altitude
  # while True:
  #   print(" Altitude: ", vehicle.location.global_relative_frame.alt)
  #   #Break and return from function just below target altitude.
  #   if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
  #     print("Reached target altitude")
  #     break
  #   time.sleep(1)

def goto(latitude, longitude, altitude, gotoFunction=vehicle.simple_goto):
    vehicle.mode = VehicleMode("GUIDED")
    # currentLocation=vehicle.location.global_relative_frame
    currentCoord = LatLon(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, datum=Datums.NAD83)

    targetCoord = LatLon(latitude, longitude, datum=Datums.NAD83)
    targetDistance = currentCoord.distanceTo(targetCoord)

    targetLocation = LocationGlobalRelative(latitude, longitude, altitude)
    gotoFunction(targetLocation)

    #print("DEBUG: targetCoord: %s" % targetCoord)
    #print("DEBUG: targetCoord: %s" % targetDistance)
    print(vehicle.mode.name)

    while vehicle.mode.name == "GUIDED": # Stop action if we are no longer in guided mode.
        # remainingDistance=get_distance_metres(vehicle.location.global_relative_frame, targetLocation)
        currentCoord = LatLon(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, datum=Datums.NAD83)
        remainingDistance = currentCoord.distanceTo(targetCoord)
        print ("Distance to target: " + str(remainingDistance))
        print("Ground speed: " + str(vehicle.groundspeed))
        if remainingDistance <= targetDistance*0.2: #Just below target, in case of undershoot. # MAYBE WILL CHANGE TO A CONSTANT
            print ("Reached target")
            break
        time.sleep(2)

# Initialize the takeoff sequence to 2m
arm()
print("Arming complete")

print("Set ground speed: " + str(1))
vehicle.groundspeed = 5

print("go to waypoint:")

# wp3 = LocationGlobalRelative(40.68134027435853, -74.48265755170037, 0)   # <- the 3rd argument is the altitude in meters. (set to 0 for rover)
# vehicle.simple_goto(wp3)
# goto(40.67056161850959, -74.47503293046965, 0)
goto(40.670515834417216, -74.47471420970764, 0)
time.sleep(5)
goto(40.670818008846034, -74.47490254470338, 0)
time.sleep(5)
goto(40.67066234340221, -74.47546513513936, 0)
time.sleep(5)
goto(40.6703363604719, -74.47521885091416, 0)

# Hover for 10 seconds
time.sleep(5)

print("return to starting point")
# vehicle.groundspeed = 1.5 # idk if this does anything
vehicle.mode = VehicleMode("RTL")
# vehicle.groundspeed = 1.5 # idk if this does anything
# Close vehicle object
vehicle.close()
