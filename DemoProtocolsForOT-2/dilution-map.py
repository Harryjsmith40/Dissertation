from opentrons import protocol_api

metadata = {"apiLevel": "2.20", 
            "protocolName": "Serial Dilution Map", 
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
    reservoir["A2"].load_liquid(liquid=stockSolution, volume=1000)
    
    # Loading the pipette
    left_pipette = protocol.load_instrument("p300_multi_gen2", "left", tip_racks=[tips_multi])
    right_pipette = protocol.load_instrument("p1000_single_gen2", "right", tip_racks=[tips_single])

    # Commanding the robot
    dye_volume = [75, 65, 55, 40, 35, 25, 15, 5]
    diluent_volume = [10, 20, 30, 40, 50, 60, 70]

    dye_wells = plate.wells("A1","B1","C1","D1","E1","F1","G1","H1")
    diluent_wells = plate.wells("B1","C1","D1","E1","F1","G1","H1")

    right_pipette.transfer(dye_volume, reservoir["A2"], dye_wells)
    right_pipette.transfer(diluent_volume, reservoir["A1"], diluent_wells)

    row = plate.rows()[0]
    left_pipette.transfer(75, reservoir["A1"], plate.columns()[1:12])
    left_pipette.transfer(25, row[:11], row[1:], mix_before=(3, 20))