from opentrons import protocol_api

metadata = {"apiLevel": "2.20", 
            "protocolName": "Serial Dilution", 
            "description": """This protocol is the outcome of following the
                   Python Protocol API Tutorial located at
                   https://docs.opentrons.com/v2/tutorial.html. It takes a
                   solution and progressively dilutes it by transferring it
                   stepwise across a plate.""", 
            "author": "Harry Smith - University of Bristol"}

requirements = {"robotType": "OT-2"}

def run(protocol: protocol_api.ProtocolContext):
    
    # Loading Labware
    tips_multi = protocol.load_labware("opentrons_96_tiprack_300ul", 6)
    tips_single = protocol.load_labware("opentrons_96_tiprack_1000ul", 4)
    reservoir = protocol.load_labware("nest_12_reservoir_15ml", 5)
    plate = protocol.load_labware("nest_96_wellplate_100ul_pcr_full_skirt", 2)

    # Defining Liquid Starting Positions
    diluent = protocol.define_liquid(
        name="Diluent",
        description="The solvent for further diluting the stock solution",
        display_color="#0000FF"
    )
    stockSolution = protocol.define_liquid(
        name="Stock Solution",
        description= "The stock solution that will be further diluted",
        display_color= "#FF0000"
    )

    # Loading liquid into wells
    reservoir["A1"].load_liquid(liquid=diluent, volume=12000)
    reservoir["A5"].load_liquid(liquid=stockSolution, volume=1000)
    
    # Loading the pipette
    left_pipette = protocol.load_instument("p300_multi_gen2", "left", tip_racks=[tips_multi])
    right_pipette = protocol.load_instrument("p1000_single_gen2", "right", tip_racks=[tips_single])

    # Commanding the robot
    dye_volume = 100
    diluent_volume = 0

    for i in range(8):
        row = plate.rows()[i]
        
        right_pipette.transfer(dye_volume, reservoir["A1"], row, new_tips="never")
        dye_volume -= 5
        
        right_pipette.transfer(dye_volume, reservoir["A1"], row, new_tips="never")
        diluent_volume += 5

        # right_pipette.transfer(100, reservoir["A5"], row[0], mix_after=(3, 50), new_tips="never")
        # right_pipette.transfer(100, row[:11], row[1:], mix_after=(3, 50), new_tips="never")