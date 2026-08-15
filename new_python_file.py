import numpy as np
import numpy as np
import pandas as pd

# Google Doc URL here
# url = "https://docs.google.com/document/u/0/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub?pli=1"

url = "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"


def get_grid_from_google_doc(url):

    list_of_tables = pd.read_html(url, header=0)
    data_table = list_of_tables[0]
    x_cord_min = int(data_table["x-coordinate"].min())
    x_cord_max = int(data_table["x-coordinate"].max())
    y_cord_min = int(data_table["y-coordinate"].min())
    y_cord_max = int(data_table["y-coordinate"].max())

    width = x_cord_max - x_cord_min + 1
    height = y_cord_max - y_cord_min + 1

    # Initialize a grid with spaces
    grid = np.full((height, width), " ")

    for _, row in data_table.iterrows():
        # Normalize X to start at index 0
        grid_x = int(row["x-coordinate"] - x_cord_min)

        # Normalize Y to start at index 0
        grid_y = int(y_cord_max - row["y-coordinate"])
        # Assign character to grid position
        grid[grid_y, grid_x] = str(row.iloc[1])

    for row in grid:
        print("".join(row))


get_grid_from_google_doc(url)  # Test the function with a Google Doc URL
