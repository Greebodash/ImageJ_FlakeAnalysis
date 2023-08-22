## temporary file 

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os 
import imagej


user_input = input("Run Macro? y/n: ")
if user_input.lower() in ["y", "yes"]:
    print("Loading...")
    ij = imagej.init(mode='interactive')
    ij.ui().showUI() # if you want to display the GUI immediately

    # Add a blocking loop to keep the script running
    while True:
        # You can add any additional code or processing here
        
        # For now, we'll just keep the loop running until the user enters "exit"
    
        macro  = '''
        path = getDirectory("image");

        Dialog.create("Contrast difference macro");
        Dialog.addMessage("Hello! This ImageJ macro makes taking and saving plot profiles easier.\\n" \
        + "Choose the input directory you want to take images from, and the output directory you want to save the plot profile values to.\\n" \
        + "The macro will loop through all images in the directory.\\n" \
        + "Why not use the INPUT and OUTPUT files under my name in the OneDrive?\\n");
        Dialog.addDirectory("Image Path", path);
        Dialog.addDirectory("Output Directory", path);
        //Dialog.addString("Bin? (More bins = reduced noise, at the cost of image resolution.)", "1");
        Dialog.show();

        // get user input values
        path = Dialog.getString();
        output_dir = Dialog.getString();
        //bin_num = Dialog.getString();

        // initialize lists
        img_list = getFileList(path);
        img_list = Array.sort(img_list);

        // loop through images, and let the user make alterations 
        for (i = 0; i < img_list.length; i++) {
            current_img = img_list[i];
            open(path + '\' + current_img);
        
            //run("Bin...", "x=" + bin_num + " y=" + bin_num + " bin=Average");
            run("Despeckle"); // image preprocessing
            run("Median...", "radius=2");

            waitForUser("Draw on line selection now. When you are ready, press OK.");

            // Get profile and display values in "Results" window
            run("Clear Results");
            profile = getProfile();
            for (j = 0; j < profile.length; j++)
                setResult("Value", j, profile[j]);
            updateResults;

            // Name your file
            Dialog.create("Name your file");
            Dialog.addString("Name your file. Please follow the format NAME_DD_MM_YY_MATERIAL_SAMPLE", "Enter filename");

            Dialog.show();

            name = Dialog.getString();
            name = name.trim(); // Remove leading and trailing whitespace
            if (name.length() == 0) {
                print("No filename provided. Exiting."); // Handle case where user provides no input
                exit();
            }

            name += ".csv"; // Append ".csv" to the filename

            // Plot profile
            Plot.create("Profile", "X", "Value", profile);

            // Save processed image to the output directory
            saveAs("Results", output_dir + '\' + name);
            close("*");
        }
        '''
        ij.py.run_macro(macro)
        
        user_input = input("Enter 'exit' to close ImageJ: ")
        if user_input.lower() == 'exit':
            break
else:
    print("Not running the macro. Continue with plot profile analysis by entering an existing filename.")
################################

dir_path = r"C:\Users\talan\INRS\Shagar, Mostafa - OrgiuLab_Flakes\Talan\OUTPUT plot profile values"

user_input = input("Enter filename you wish to analyse: ")

file_prefixes = [user_input]

################################

input("Do you want the rgb channels to for these bad boys?")
if "yes":
    print("too bad i haven't coded it yet")

else:
    print("good choice. lets continue.")



max_difference = 1
min_number_points = 20
substrate_similarity_threshold = 15
#plateau_intensities = []


def read_values_from_file(file_path):
    _, file_extension = os.path.splitext(file_path)

    # If the file is in .txt format, read each line as a float value
    if file_extension.lower() == ".txt":
        with open(file_path, "r") as file:
            lines = file.readlines()
        values = [float(line.strip()) for line in lines]

    # If the file is in .csv format, read the values from the second column of the CSV file
    elif file_extension.lower() == ".csv":
        csv_dataframe = pd.read_csv(file_path, header=None, skiprows=1)
        values = csv_dataframe.iloc[:, 1].astype(float).tolist()

    # Raise an exception for unsupported file formats
    else:
        raise ValueError("Invalid file format. Only .txt and .csv files are supported.")

    return values


def plateau_finder(values, file_name):
    # example data
    plateaus = []
    plateau_intensities = []
    values_df = pd.DataFrame(
        {
        'time': np.arange(0, len(values)),  # Assuming 1 unit time interval between each data point
        'data': values
        }
    )
    plt.plot(
        values_df['time'], values_df['data'], label=f"original data",
        marker='x', lw=0.5, ms=2.0, color="black",
    )

    # filter and group plateaus
    
    # group by maximum difference
    group_ids = (abs(values_df['data'].diff(1)) > max_difference).cumsum()
    plateau_idx = 0
    for group_idx, group_data in values_df.groupby(group_ids):
        # filter non-plateaus by min number of points
        if len(group_data) < min_number_points:
            continue
        plateau_idx += 1
        start_index = group_data.index[0]
        end_index = group_data.index[-1]
        plateaus.append((start_index, end_index))
        

          
        #print("Start, End: ", "(", df['time'][start_index], ",", df['time'][end_index], ")")
        

        # Get the data values within the plateau
        plateau_values = group_data['data'].values
        
        # Calculate the mean intensity over the plateau interval
       
        
        plt.plot(
            group_data['time'], group_data['data'], label=f"Plateau-{plateau_idx}",
            marker='x', lw=1.5, ms=5.0,
        )
        _time = group_data['time'].mean()
        _value = group_data['data'].mean()
        plateau_intensities.append(_value)

        print(f"Plateau number {plateau_idx}: ", "(", values_df['time'][start_index], ",", values_df['time'][end_index], ") has intensity: ", _value)
        #print("PLATEAU INTENSITIES: ", plateau_intensities)
        plt.annotate(
            f"Plateau-{plateau_idx}", (_time, _value), ha="center",
            
        )
        
    
   
    
    return plateau_idx, plateau_intensities, plateaus







def substrate_calculator(plateau_intensities, substrate_similarity_threshold):
    if len(plateau_intensities) >= 2:
            sorted_intensities = sorted(plateau_intensities, reverse=True)
            highest1 = sorted_intensities[0]
            highest2 = sorted_intensities[1]
            # If the difference between the two highest intensities is within the threshold, take their mean as the 'substrate' value
            if abs(highest1 - highest2) <= substrate_similarity_threshold:
                substrate = np.mean([highest1, highest2])
            else:
                # Otherwise, set the 'substrate' value to the highest intensity
                substrate = sorted_intensities[0]
    else:
            # If there's only one intensity, set the 'substrate' value to that intensity
         substrate = sorted_intensities[0]

        # Print the highest plateau intensity and the 'substrate' value
    print("The highest plateau intensity is:", sorted_intensities[0], "\n")    
    print("The substrate value is:", substrate, "\n")
    return substrate

def contrast_diff_calculator(substrate, plateau_intensities):
    contrast_differences = []
    normalized_contrast_differences = []
    
    for i in plateau_intensities:
        
        contrast_diff = i - substrate
        contrast_differences.append(contrast_diff)

    # Print the contrast differences
    print("The contrast differences are:", contrast_differences[1:-1], "\n")     # This assumes the line starts and ends in the substrate, and both these platuea values are used in the detection of a mean. 
    try:
        normalized_contrast_differences = contrast_differences/(substrate + plateau_intensities)  #ok this bit is not good coding. Change this soon.
    except ValueError:
        print("\n There aren't the same number of contrast differences and plateuas. I'll recode this soon, but it's because the blue filter gives shitty plot profiles. \n")
    
    # Print the normalized contrast differences
    print("The normalized contrast differences are:", normalized_contrast_differences[1:-1], "\n")

    return contrast_differences, normalized_contrast_differences

##################################################################################
# CODE RELATING TO ADDING CONTRAST DIFFERENCE VALUES TO DATAFRAME 
##################################################################################

def get_input(prompt):
    user_input = input(prompt)
    try:
        return float(user_input)
    except ValueError:
        return np.nan


# Define function to append user input to DataFrame
def append_to_dataframe(dataframe):
    name = input("Enter Name: ")
    dd = input("Enter DD: ")
    mm = input("Enter MM: ")
    yy = input("Enter YYYY: ")
    material = input("Enter MATERIAL: ")
    sample = input("Enter SAMPLE: ")
    estimated_layer_number = input("Enter Estimated Layer Number: ")
    cd = get_input("Enter Contrast Difference: ")
    cd_red = get_input("Enter Contrast Difference RED: ")
    cd_green = get_input("Enter Contrast Difference GREEN: ")
    cd_blue = get_input("Enter Contrast Difference BLUE: ")
  
    # Append user input to DataFrame
    new_entry = {
        'NAME': name,
        'DD': dd,
        'MM': mm,
        'YY': yy,
        'MATERIAL': material,
        'SAMPLE': sample,
        'ESTIMATED LAYER NUMBER': estimated_layer_number,
        'CD' : cd,
        'CD Red': cd_red,
        'CD Green': cd_green,
        'CD Blue': cd_blue
    }
    
    dataframe = dataframe.append(new_entry, ignore_index=True)

    return dataframe


def main():
    
    
    for file_prefix in file_prefixes:
        file_list = [file_name for file_name in os.listdir(dir_path) if file_name.startswith(file_prefix)]   
        
        for file_name in file_list:
            file_path = os.path.join(dir_path, file_name)
            values = read_values_from_file(file_path)

            

            print("\n NOW ANALYSING FILE: ", file_name, "\n")
            plateau_intensities = []
           
            plateau_idx, plateau_intensities, plateaus = plateau_finder(values, file_name)
            
            substrate = substrate_calculator(plateau_intensities, substrate_similarity_threshold)
            
            contrast_differences = contrast_diff_calculator(substrate, plateau_intensities)
            plt.xlabel("Pixel number")
            plt.ylabel("Contrast value")
            plt.title("Plot Profile: " +  file_name)    
            plt.legend()
            print("Check that each plateau has been correctly identified, and that the contrast differences are physical. \nThen close the graph to continue.")
            for start, end in plateaus:
                plt.axvspan(start, end, color='green', alpha=0.3)
            plt.show()

            print("\n STILL ANALYSING FILE: ", file_name, "\n")
            answer = input("\n Do you want to add these values to the dataframe? y/n: ")
            if answer.lower() in ["y", "yes"]:
                print("Now it is time to add these values to the data frame ")
                dataframe_file_path = r"C:\Users\talan\INRS\Shagar, Mostafa - OrgiuLab_Flakes\Talan\DATAFRAME\DATAFRAME.csv"
                try:
                    dataframe = pd.read_csv(dataframe_file_path)
                except FileNotFoundError:
                    # If file doesn't exist, create an empty DataFrame
                    dataframe = pd.DataFrame(columns=['NAME', 'DD', 'MM', 'YY', 'MATERIAL', 'SAMPLE', 'ESTIMATED LAYER NUMBER', 'CD', 'CD Red', 'CD Green', 'CD Blue'])

                # Print existing data
                print("Existing Data:")
                print(dataframe)

                # Append user input to DataFrame
                dataframe = append_to_dataframe(dataframe)

                # Print updated DataFrame
                print("Updated Data:")
                print(dataframe)
                
                

                # Save updated DataFrame to CSV
                dataframe.to_csv(dataframe_file_path, index=False)
            else:
                print("Moving on to the next file...") 
    print("Program finished.")            
                       
            

           
if __name__ == "__main__":
    main()