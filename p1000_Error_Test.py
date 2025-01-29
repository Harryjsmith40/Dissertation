import subprocess
from opentrons import protocol_api

audio_file = "etc/audio/speaker-test.mp3"


metadata = {"apiLevel": "2.20", 
            "protocolName": "p1000 Error Test", 
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
    
    test_speaker()

    # Loading Labware
    tips_single = protocol.load_labware("opentrons_96_tiprack_1000ul", 1)
    reservoir = protocol.load_labware("nest_12_reservoir_15ml", 3)
    tube_Rack = protocol.load_labware("opentrons_24_tuberack_nest_1.5ml_snapcap", 2)

    # Defining Liquid Starting Positions
    water = protocol.define_liquid(
        name="Water",
        description="Water for use in calculating real dispensed volume. 1.00 g/ml at room temperature thus 1g = 1ml.",
        display_color="#0000FF"
    )

    # Loading liquid into wells
    reservoir["A1"].load_liquid(liquid=water, volume=12000)
    
    # Loading the pipette
    right_pipette = protocol.load_instrument("p1000_single_gen2", "right", tip_racks=[tips_single])

    # Commanding the robot
    volume_List = []
    volume = 0

    while len(volume_List) < 24:
        volume += 40
        volume_List.append(volume)

    right_pipette.transfer(volume_List, reservoir["A1"], tube_Rack.wells(), blow_out=True, new_tip="always", touch_tip=True)