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
    # Your Code Here
