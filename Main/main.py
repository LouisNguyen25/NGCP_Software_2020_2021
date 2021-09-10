"""
Main file for running thread processes concurrently:
    > Run main on startup/reboot  (^–^=)~
    > Camera feed   (✖╭╮✖)
    > GCS Comms     (´･Д･lll)ゞ
    > Autonomous Navigation Processes:
        - IMU
        - Waypoint Nav
        - Object Avoidance
"""
import time, math, requests, threading, struct
from digi.xbee.devices import DigiMeshDevice
# from Comms import xbee, listen
# from xbee import ToERU, ToGCS, Orientation, LatLng, ManualControl, Geofence

#=================================================================== Start - From SampleERU ===================================================================

E_STOP = False

comm_port = "/dev/ttyAMA0" # can be swapped out for "/dev/ttyUSB0" for serial connection - Might change based off how things are plugged in
baud_rate = "9600"

device = DigiMeshDevice(port=comm_port, baud_rate=baud_rate)
device.open()

print("This device's name: ", device.get_node_id())

telemetry_data = ToGCS(0, 0, Orientation(0,0,0), LatLng(35.082094, -120.512722), 0.98, True, 0, False, LatLng(0,0), 0, False, True)
gcs_lock = threading.Lock()
gcs_addr = None

hiker_pos = LatLng(0,0)
current_pos = LatLng(35.082094, -120.512722)
current_state = 0

packet_buffer = b''
packet_counter = 0

def packet_received_with(packet):
    print('Received packet from ', packet.remote_device.get_node_id())
    global gcs_addr 
    global packet_counter
    global packet_buffer
    global current_state
    global hiker_position

    with gcs_lock:
        gcs_addr = packet.remote_device.get_64bit_addr()
    data = None

    if packet_counter is 0:
        packet_counter = struct.unpack("I", packet.data[:4])[0] -1
        data = packet.data[4:]
        print("expecting ", packet_counter," packets")
        packet_buffer = b''
    else:
        packet_counter -= 1
        data = packet.data

    packet_buffer += data

    if packet_counter is 0:
        with xbee.read_lock: # Acquire lock to read command data from GCS  ||  Read data from GCS
            command_data = ToERU.deserialize(packet_buffer)
            if command_data.stop:
                print("STOPPPING AT ", current_pos)     # Emergency Stop
            hiker_pos = command_data.hiker_position     # use command_data.(whatever) to receive whatever data is needed
            current_state = command_data.perform_state
            # man_con = command_data.manual_control    # Manual Control Data from XBee

def transmit_packet():
    with telemetry_data.lock: # Acquire lock to update telemetry data
        telemetry_data.hiker_positon = hiker_pos
        telemetry_data.gps = current_pos
        telemetry_data.orientation.yaw += 1
        telemetry_data.battery -= 0.0001
        telemetry_data.current_state = current_state
    if gcs_addr:
        telemetry_data.serialize().transmit(device, gcs_addr)
        print("Transmitting")

    time.sleep(0.5) #========= Max says a lil less than 1 is good

# transmitThread = xbee.TransmitThread(transmit_packet)

#==================================================================== End - From SampleERU ====================================================================


# For GCS:
#     > Receive data from Xbee
#     > update relevant position/health status data
#         - Video feed
#         - position/direction (MPU)
#         - State code/error codes
#     > Transmit data to GCS


# ========================================================================= Main Loop =========================================================================
try:
    while (True):

    # > Read xbee data
    
    # > Determine State

    # > Call appropriate functions
    
    # > Manipulate data
    
    # > Send data to xbee
    
    # ***use try-except-finally for catching errors and cleaning up

        print("Successfully ran setup for script!")

        # device.add_data_received_callback(packet_received_with)
        # print("Successfully pinged XBee for a data packet")
        
        print("exiting main while loop")
        break

        while E_STOP: 
            # Might become IF statement if GCS doesn't plan to get out of E_STOP
            # Clean up/ shut down all peripherals unless GCS clears E_STOP
            # Only move on from E_STOP if GCS says so
            pass

        pass

except KeyboardInterrupt():
    # GPIO clean-up
    sys.exit()

finally:
    print("yeet")