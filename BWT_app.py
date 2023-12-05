# written by B. Gaber, M. Sivaswami, H. Gholizadeh, Himali Pandhi

import pandas as pd

# Define the Burrows-Wheeler Transform function
def bwt(string):
    # I'll add '$' to the end of my string
    string += '$'
    # create a list to store the position of each character in the string
    indices = [string[i:] + string[:i] for i in range(len(string))]
    # sort the rotated strings and start a cycle of rotation where the characters from the end are moved to the beginning
    sorted_indices = sorted(indices)
    # This line will concatenate the last characters of each rotated string
    bwt_encoded = ''.join(sorted_indices[-1][-1] for sorted_indices in sorted_indices)
    matrix = pd.DataFrame({
        "Possible rotations": indices,
        "Sorted": sorted_indices
    })
    return matrix, bwt_encoded


# Defining inverse BWT function
def bwt_inverse(bwt_encoded):
    # let's check if $ is present in BWT encoded strings
    if '$' not in bwt_encoded:
        raise ValueError("'$' character not found in the BWT-encoded string.")

    # length of BWT encoded string
    ln = len(bwt_encoded)

    # Creating a list of tuples with each character and index followed by sorting
    tuples = [(char, i) for i, char in enumerate(bwt_encoded)]
    tuples.sort()

    # To reconstruct the first column of Matrix
    column_1 = [char for char, n in tuples]

    # Initializing current BWT row to the row containing '$'
    current_BWT_row = tuples[bwt_encoded.index('$')][1]

    # Now we will reconstruct the original string input by the user
    string_original = ''
    for n in range(ln):
        string_original = column_1[current_BWT_row] + string_original
        current_BWT_row = tuples[current_BWT_row][1]

    # Creating a data frame to view the matrix containing the first column, last column (BWT result), and the Original sequence column
    df = pd.DataFrame({
        "First Column": column_1,
        "Last Column": list(bwt_encoded),
        "Original Sequence Column": list(string_original)
    })

    return df, string_original


# first ask the user if they want to preform forward or inverse BWT
user_input_direction = input(
    "Do you want to perform Forward or Inverse BWT? (Type 'Forward' or 'Inverse'): ").strip().lower()

# If thet chooses to perform Forward BWT it will ask the following
if user_input_direction == 'forward':
    user_input = input("Please enter the sequence: ").strip()
    bwt_result, bwt_encoded = bwt(user_input)

    # Ask if the user wants to see all the possible permutations sorted
    user_input_2 = input("Do you want to see all the possible permutations sorted? ").strip().lower()

    if user_input_2 in ["yes", "Yes"]:
        print()
        print("Here are all the possible permutations and sorted form: ")
        print(bwt_result)
        print()
        print("BWT result of your entered sequence is: ", bwt_encoded)
        print()
    else:
        print("BWT result of your entered sequence is: ", bwt_encoded)
        print()

# If the user chooses to Inverse BWT
elif user_input_direction == 'inverse':
    user_input_inverse = input("Please enter the BWT sequence: ").strip()
    inverse_result, string_original = bwt_inverse(user_input_inverse)

    # lets print IBWT results and visualize the 2 columns and original sequence column
    print("\nInverse BWT sequence is:", string_original)
    print("\nVisualization:")
    print(inverse_result)
    print()

# if thy wrote incorrect input
else:
    print("Invalid input. Please enter either 'Forward' or 'Inverse'.")

