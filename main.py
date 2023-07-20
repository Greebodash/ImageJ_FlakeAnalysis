import os
import pandas as pd
from contrast_difference_calculator import calculate_contrast_differences
import matplotlib.pyplot as plt

# TO DEAL WITH DIFFERENT FORMAT FILES 
def read_values_from_file(file_path):
    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == ".txt":
        with open(file_path, "r") as file:
            lines = file.readlines()
        values = [float(line.strip()) for line in lines]

    elif file_extension.lower() == ".csv":
        df = pd.read_csv(file_path, header=None, skiprows=1)
        values = df.iloc[:, 1].astype(float).tolist()

    else:
        raise ValueError("Invalid file format. Only .txt and .csv files are supported.")

    return values
###########################################################################################

# ENTER FILEPATH BELOW #

###########################################################################################
dir_path = r"C:\Users\talan\INRS\Shagar, Mostafa - OrgiuLab_Flakes\Talan\Plot profile list values"
file_prefix = "Plot"

# Get a list of files in the directory that start with the specified prefix
file_list = [file_name for file_name in os.listdir(dir_path) if file_name.startswith(file_prefix)]

for file_name in file_list:
    file_path = os.path.join(dir_path, file_name)
    values = read_values_from_file(file_path)
    
    print(values)

    # Call the calculate_contrast_differences function here with 'values'
    # Assuming you have this function defined separately in your code
    # calculate_contrast_differences(values, threshold, min_consecutive_x, similarity_threshold)
    # Set the threshold and minimum consecutive x-values to define a plateau
    threshold = 2
    min_consecutive_x = 5

    # Set the similarity threshold for highest plateau intensities. Finds a mean on the first and last ones, which should be the substrate, to account for a difference in background intensity.
    similarity_threshold = 1.0



    # Calculate contrast differences and plots them
    contrast_differences = calculate_contrast_differences(values, threshold, min_consecutive_x, similarity_threshold)

    # Print the contrast differences
    print("Contrast Differences:")
    print(contrast_differences)
    plt.show()