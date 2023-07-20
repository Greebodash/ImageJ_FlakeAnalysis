import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculate_contrast_differences(values, threshold, min_consecutive_x, similarity_threshold):
    #It's pretty important for the contrast difference values that your line selection starts and ends with a good bit of substrate. 
    #This is because i've calculated a mean substrate value using the substrate contrast value on either side of the crystal.
    #These can often be different due to non-uniform circular distribution of light caused by the microscope lens.
    #Alternatively, you could run the image first through a Lens modulation transfer function filter and avoid the problem entirely. But I bet you won't.

    #insert file path of crystal plot profile values.
    #file_path = r"C:\Users\talan\OneDrive - University of Bath\Contrast method work\Contrast method\Plot profile analysis automation\ALL LIST DATA\Maxime s8.csv"
    ##"C:\Users\talan\OneDrive - University of Bath\Contrast method work\Contrast method\Plot profile analysis automation\plot profile list data.csv"

    # Read the file
    #with open(file_path, "r") as file:
    #    lines = file.readlines()

    #df = pd.read_csv(file_path, header = None, skiprows = 1)
    #values = df.iloc[:, 1].astype(float).tolist()

    # Print the extracted values
    #print(values)

    threshold = 2  # Adjust threshold as needed. DEtermines tolerance of a plateau.

    # Create a binary array based on thresholding
    binary_array = np.greater_equal(values, threshold)

    # Specify the minimum number of consecutive x-values for plateau detection
    min_consecutive_x = 5  # Adjust as needed

    # Initialize variables for plateau detection
    start_index = None
    current_interval = []
    plateau_segments = []

    # Detect plateaus
    for i in range(len(values)):
        if start_index is None:
            start_index = i
            current_interval.append(values[i])
        elif abs(values[i] - values[i-1]) <= threshold:
            current_interval.append(values[i])
        else:
            if len(current_interval) >= min_consecutive_x:
                plateau_segments.append((start_index, i - 1))
            start_index = i
            current_interval = [values[i]]

    # Check if the last interval forms a plateau
    if start_index is not None and len(current_interval) >= min_consecutive_x:
        plateau_segments.append((start_index, len(values) - 1))

    # Calculate mean y-value for each plateau segment
    plateau_intensities = []
    for segment in plateau_segments:
        start_index, end_index = segment
        plateau_values = values[start_index:end_index + 1]
        mean_intensity = np.mean(plateau_values)
        plateau_intensities.append(mean_intensity)
        plateau_intensities.append(mean_intensity)
        print("Plateau segment:", segment)
        print("Mean intensity:", mean_intensity)

    #this stuff might be wrong if your line selection does not start and end in the substrate.
    plateau_intensities.sort(reverse=True)

    # Check if the two highest plateau intensities are similar
    if len(plateau_intensities) >= 2:
        highest1 = plateau_intensities[0]
        highest2 = plateau_intensities[1]
        similarity_threshold = 1.0  # Adjust as needed

        if abs(highest1 - highest2) <= similarity_threshold:
            substrate_mean = np.mean([highest1, highest2])
            print("Substrate Mean Intensity:", substrate_mean)

    # Calculate contrast difference for each plateau segment
    contrast_differences = []
    for segment in plateau_segments[1:]:
        start_index, end_index = segment
        plateau_values = values[start_index:end_index + 1]
        mean_intensity = np.mean(plateau_values)
        contrast_diff = mean_intensity - substrate_mean
        contrast_differences.append(contrast_diff)
    
    # Print the contrast differences
    print("Contrast Differences:")
    print(contrast_differences)       
    
    #plt.figure  
      
        # Plotting the plateaus on a graph
    plt.plot(values)
    plt.xlabel("Pixel number")
    plt.ylabel("Contrast value")
    plt.title("Plot Profile")
    plt.grid(True)

    for segment in plateau_segments:
        start_index, end_index = segment
        plt.axvspan(start_index, end_index, color='green', alpha=0.3)

    plt.show()

    print("The last contrast difference value is the difference between the substrate value and the end of your line selection. You can see how different the mean is to your actual value.")
    return contrast_differences