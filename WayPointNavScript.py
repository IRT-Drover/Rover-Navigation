from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time

# for key, value in vehicle.parameters.iteritems():
#     print " Key:%s Value:%s" % (key,value)


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

# Initialize the takeoff sequence to 2m
arm()
print("Arming complete")

vehicle.groundspeed = 7

print("go to waypoint:")

wp3 = LocationGlobalRelative(40.62078446804657, -74.56871825506587, 0)   # <- the 3rd argument is the altitude in meters. (set to 0 for rover)
vehicle.simple_goto(wp3)


# Hover for 10 seconds
time.sleep(10)

wp3 = LocationGlobalRelative(40.62022150142908, -74.5688736823382, 0)   # <- the 3rd argument is the altitude in meters. (set to 0 for rover)
vehicle.simple_goto(wp3)


# Hover for 10 seconds
time.sleep(10)

wp3 = LocationGlobalRelative(40.619904501564356, -74.56900268233817, 0)   # <- the 3rd argument is the altitude in meters. (set to 0 for rover)
vehicle.simple_goto(wp3)


# # Hover for 10 seconds
# time.sleep(10)

# wp3 = LocationGlobalRelative(40.618609,-74.566750, 0)   # <- the 3rd argument is the altitude in meters. (set to 0 for rover)
# vehicle.simple_goto(wp3)


# # Hover for 10 seconds
# time.sleep(10)

# wp3 = LocationGlobalRelative(40.618665,-74.567323, 0)   # <- the 3rd argument is the altitude in meters. (set to 0 for rover)
# vehicle.simple_goto(wp3)


# # Hover for 10 seconds
# time.sleep(10)

print("return to starting point")
vehicle.mode = VehicleMode("RTL")
# Close vehicle object
vehicle.close()
