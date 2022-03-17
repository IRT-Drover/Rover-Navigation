from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
from pygeodesy.ellipsoidalVincenty import LatLon
from pygeodesy import Datums

import numpy as np

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

# Moves the vehicle to a position latitude, longitude, altitude.
# The method takes a function pointer argument with a single `dronekit.lib.LocationGlobal` parameter for
# the target position. This allows it to be called with different position-setting commands.
# By default it uses the standard method: dronekit.lib.Vehicle.simple_goto().
# It uses pygeodesy methods to calculate distance between coordinates.
# The method reports the distance to target every two seconds.
#
# note: simple_goto(), by itself, can be interrupted by a later command,
# and does not provide any functionality to indicate when the vehicle has reached its destination.
def goto(latitude, longitude, altitude, gotoFunction=vehicle.simple_goto):
    vehicle.mode = VehicleMode("GUIDED")
    # currentLocation=vehicle.location.global_relative_frame
    currentCoord = LatLon(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, datum=Datums.NAD83)

    targetCoord = LatLon(latitude, longitude, datum=Datums.NAD83)
    targetDistance = currentCoord.distanceTo(targetCoord)

    targetLocation = LocationGlobalRelative(latitude, longitude, altitude)
    gotoFunction(targetLocation)

    #print "DEBUG: targetCoord: %s" % targetCoord
    #print "DEBUG: targetCoord: %s" % targetDistance
    print(vehicle.mode.name)

    while vehicle.mode.name == "GUIDED": # Stop action if we are no longer in guided mode.
        # remainingDistance=get_distance_metres(vehicle.location.global_relative_frame, targetLocation)
        currentCoord = LatLon(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, datum=Datums.NAD83)
        remainingDistance = currentCoord.distanceTo(targetCoord)
        print ("Distance to target: " + str(remainingDistance))
        if remainingDistance <= targetDistance*0.3: #Just below target, in case of undershoot. # MAYBE WILL CHANGE TO A CONSTANT
            print ("Reached target")
            break
        time.sleep(2)

arm()
print("Arming complete")

vehicle.groundspeed = 5
print("Set ground speed to " + str(vehicle.groundspeed))

GPSDATAFILE = np.load('GPSDATA_TOSEND.npz')
GPSPATHS = GPSDATAFILE['GPSPATHS']
GPSDATAFILE.close()

for point in GPSPATHS[0]:
    print("Go to waypoint:")
    #wp3 = LocationGlobalRelative(GPSPATHS[0][0], GPSPATHS[0][1]], 0)   # <- the 3rd argument is the altitude in meters. (set to 0 for rover)
    #vehicle.simple_goto(wp3)
    goto(GPSPATHS[0][0], GPSPATHS[0][1], 0)

# Hover for 10 seconds
time.sleep(5)

print("Return to starting point")
vehicle.mode = VehicleMode("RTL")
# Close vehicle object
vehicle.close()
