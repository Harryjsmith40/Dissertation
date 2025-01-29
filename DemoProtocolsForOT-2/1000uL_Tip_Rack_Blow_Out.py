from opentrons import protocol_api

metadata = {"apiLevel": "2.20", 
            "protocolName": "1000uL Blow Out Clean", 
            "description": """A simple protocol that blows out 
            all of the pipette tips in a 1000uL tip rack for 
            cleaning and drying.""", 
            "author": "Harry Smith - University of Bristol"}

requirements = {"robotType": "OT-2"}

def run(protocol: protocol_api.ProtocolContext):
    
    # Loading Labware
    tips_single = protocol.load_labware("opentrons_96_tiprack_1000ul", 11)

    # Loading the pipette
    right_pipette = protocol.load_instrument("p1000_single_gen2", "right", tip_racks=[tips_single])

    # Commanding the robot
    for _ in range(96):
        right_pipette.pick_up_tip()
        right_pipette.blow_out(right_pipette.trash_container)
        right_pipette.return_tip()
