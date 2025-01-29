import subprocess
from opentrons import protocol_api, types

audio_file = "/Audio Files/Mariah Carey - All I Want For Christmas Is You.mp3"

metadata = {"apiLevel": "2.20", 
            "protocolName": "300uL Blow Out Clean", 
            "description": """A simple protocol designed to test the 
            precision and accuracy of the single channel p1000 gen2 
            pipette.""", 
            "author": "Harry Smith - University of Bristol"}

requirements = {"robotType": "OT-2"}

def run_quiet_process(command): 
    subprocess.check_output('{} &> /dev/null'.format(command), shell=True) 

def test_speaker(): 
    print('Speaker') 
    print('Next\t--> CTRL-C')
    try:
        run_quiet_process('mpg123 {}'.format(audio_file))
    except KeyboardInterrupt:
        pass
        print()

def run(protocol: protocol_api.ProtocolContext):
    
    # Loading Labware
    tips_multi = protocol.load_labware("opentrons_96_tiprack_300ul", 11)

    # Loading the pipette
    left_pipette = protocol.load_instrument("p300_multi_gen2", "left", tip_racks=[tips_multi])

    # Commanding the robot
    for _ in range(12):
        left_pipette.pick_up_tip()
        left_pipette.blow_out(left_pipette.trash_container)
        left_pipette.return_tip()