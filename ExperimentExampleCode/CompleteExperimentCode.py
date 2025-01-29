from opentrons import protocol_api
import pandas as pd

metadata = {
    "apiLevel": "2.20",
    "protocolName": "Ksp determination of Cu (II) glycinate",
    "description": """A protocol that finds the approx Ksp
    of Cu(OAc).H20 + Gly via a spread of different reactions
    varying the volume fractions.""",
    "author": "Harry Smith - University of Bristol"
}

requirements = {"robotType": "OT-2"}


def read_excel(file_path: str, sheet_name: str = None) -> pd.DataFrame:
    """
    Reads the Excel file and returns a DataFrame.
    
    Args:
        file_path (str): Path to the Excel file.
        sheet_name (str): Optional, specific sheet to read.
    
    Returns:
        pd.DataFrame: DataFrame with the Excel content.
    """
    try:
        return pd.read_excel(file_path, sheet_name=sheet_name)
    except Exception as e:
        raise ValueError(f"Failed to read the Excel file: {e}")


def process_arrays(file_path: str, sheet_name: str, x: int):
    """
    Processes the Excel file columns, calculates the totals and subtracts from x.
    
    Args:
        file_path (str): Path to the Excel file.
        sheet_name (str): Name of the sheet to process.
        x (int): The value to subtract the total from.
    
    Returns:
        list: A list of dictionaries with processed arrays for Cu and Glycine, along with totals and remaining values.
    """
    # Read the Excel data
    df = read_excel(file_path, sheet_name)

    # Ensure column names are correct based on the input file
    if "Cu Values" not in df.columns or "Glycine Values" not in df.columns:
        raise KeyError("Excel file must contain 'Cu Values' and 'Glycine Values' columns.")

    # Convert columns to NumPy arrays to ensure proper array behavior
    cu_values = df["Cu Values"].to_numpy()  # Convert column to NumPy array
    gly_values = df["Glycine Values"].to_numpy()  # Convert column to NumPy array

    results = []
    
    for cu, gly in zip(cu_values, gly_values):
        # Ensure all values are valid floats
        cu = float(cu)
        gly = float(gly)
        overall_total = cu + gly
        remaining = float(x - overall_total)  # DI water volume is the remaining volume to reach x

        # Append results as dictionaries
        results.append({
            "cu_array": cu,  # Now properly read as array values
            "gly_array": gly,
            "total": overall_total,
            "remaining": max(0, remaining)  # Ensure remaining is not negative
        })
    
    return results


def run(protocol: protocol_api.ProtocolContext):
    # Load Labware
    tips_single = protocol.load_labware("opentrons_96_tiprack_1000ul", 4)
    reservoir = protocol.load_labware("nest_12_reservoir_15ml", 5)
    plate = protocol.load_labware("nest_96_wellplate_100ul_pcr_full_skirt", 2)

    # Define Liquids
    diwater = protocol.define_liquid(
        name="DI Water",
        description="The solvent for further diluting the stock solution",
        display_color="#00FFFF"
    )
    cuStockSolution = protocol.define_liquid(
        name="Cu Stock Solution",
        description="The stock solution that will be further diluted",
        display_color="#000080"
    )
    glyStockSolution = protocol.define_liquid(
        name="Glycine Stock Solution",
        description="The stock solution that will be further diluted",
        display_color="#FFFFFF"
    )

    # Load Liquids
    reservoir["A1"].load_liquid(liquid=diwater, volume=120000)
    reservoir["A2"].load_liquid(liquid=cuStockSolution, volume=10000)
    reservoir["A3"].load_liquid(liquid=glyStockSolution, volume=10000)

    # Load Pipettes
    right_pipette = protocol.load_instrument("p1000_single_gen2", "right", tip_racks=[tips_single])

    # Example Excel File and Parameters
    file_path = "LabData.xlsx"
    sheet_name = "OT-2 Input"
    x = 100  # Define total volume for each well

    # Process the data
    results = process_arrays(file_path, sheet_name, x)

    # Map results to wells and command the robot
    well_mapping = plate.wells()  # Get all wells in the plate

    # Step 1: Dispense all Cu values using a single tip
    right_pipette.pick_up_tip()
    for i, result in enumerate(results):
        if i >= len(well_mapping):  # Avoid overflow
            break
        target_well = well_mapping[i]
        
        # Dispense Cu into the well
        right_pipette.transfer(
            float(result["cu_array"]),  # Ensure volume is a valid float
            reservoir["A2"], 
            target_well.top(),
            new_tip='never'  # Reuse the same tip
        )
    right_pipette.drop_tip()

    # Step 2: Dispense DI Water using the "remaining" value
    right_pipette.pick_up_tip()
    for i, result in enumerate(results):
        if i >= len(well_mapping):  # Avoid overflow
            break
        target_well = well_mapping[i]
        
        # Dispense DI Water (remaining volume)
        if result["remaining"] > 0:  # Ensure there's remaining volume to dispense
            right_pipette.transfer(
                float(result["remaining"]),  # Ensure volume is a valid float
                reservoir["A1"],
                target_well.top(),
                new_tip='never'  # Reuse the same tip
            )
    right_pipette.drop_tip()

    # Step 3: Dispense all Glycine values using a single tip
    right_pipette.pick_up_tip()
    for i, result in enumerate(results):
        if i >= len(well_mapping):  # Avoid overflow
            break
        target_well = well_mapping[i]
        
        # Dispense Glycine into the well
        right_pipette.transfer(
            float(result["gly_array"]),  # Ensure volume is a valid float
            reservoir["A3"], 
            target_well.top(),
            new_tip='never'  # Reuse the same tip
        )
    right_pipette.drop_tip()

    protocol.comment("Liquid transfer completed.")
