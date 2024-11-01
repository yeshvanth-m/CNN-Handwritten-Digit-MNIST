weights_mif_file = 'w_1_0.mif'
weights_txt_from_mif = 'w_1_0.txt'
# Input file containing binary values
digit_input_binary_file = 'test_data.txt'
# Output file to store the decimal values
digit_output_decimal_file = 'test_data_decimal.txt'
# Input text file containing JSON data
weightsAndBiases_input_file = 'WeightsAndBiases.txt'
# Output file to store the first 784 weights
weights_txt_file = 'weights_1_0.txt'

bias_mif_file = 'b_1_0.mif'

# Constants based on your specifications
DATA_WIDTH = 8   # Total width of each binary value
INT_BITS = 4      # Number of integer bits (including the sign bit)
FRAC_BITS = DATA_WIDTH - INT_BITS  # Remaining bits are fractional

def twos_complement_to_decimal(binary_str, data_width, int_bits, frac_bits):
    """Convert a two's complement binary string to a floating-point decimal value."""
    # Convert binary string to integer
    int_value = int(binary_str, 2)
    
    # Check if the sign bit is set (indicating a negative number in two's complement)
    if int_value & (1 << (data_width - 1)):  # Sign bit check
        # Adjust for two's complement to make it negative
        int_value -= (1 << data_width)
    
    # Divide by 2^fractional_bits to get the floating-point value
    float_value = int_value / (2 ** frac_bits)
    return float_value

def read_and_decode(filename):
    """Reads binary strings from a file and decodes them to floating-point decimal values."""
    float_values = []
    with open(filename, 'r') as file:
        for line in file:
            binary_str = line.strip()
            if binary_str:  # Only process non-empty lines
                float_value = twos_complement_to_decimal(binary_str, DATA_WIDTH, INT_BITS, FRAC_BITS)
                float_values.append(float_value)
    return float_values

def write_fixed_point_values(filename, values):
    """Writes fixed-point values to a file in binary string format."""
    with open(filename, 'w') as file:
        for value in values:
            file.write(str(value) + '\n')

def DtoB(num, dataWidth, fracBits):
    """Converts a decimal number into two's complement binary string."""
    if num >= 0:
        num = num * (2 ** fracBits)
        num = int(num)
        e = bin(num)[2:].zfill(dataWidth)  # Zero-fill to ensure correct width
    else:
        num = -num
        num = num * (2 ** fracBits)  # number of fractional bits
        num = int(num)
        if num == 0:
            d = 0
        else:
            d = 2 ** dataWidth - num
        e = bin(d)[2:].zfill(dataWidth)  # Zero-fill to ensure correct width
    return e

# Read and decode values from the file
decoded_values = read_and_decode(weights_mif_file)
#print("Decoded decimal values:", decoded_values)

write_fixed_point_values(weights_txt_from_mif, decoded_values)

# Read binary values from the file, convert them to decimal, and write to the output file
with open(digit_input_binary_file, 'r') as infile, open(digit_output_decimal_file, 'w') as outfile:
    for line in infile:
        binary_value = line.strip()
        
        # Ensure we only process non-empty lines
        if binary_value:
            # Convert binary to decimal
            decimal_value = int(binary_value, 2)
            
            # Write the decimal value to the output file
            outfile.write(f"{decimal_value}\n")

print(f"Decimal values saved to '{digit_output_decimal_file}'.")

import json

# Read JSON data from the text file
with open(weightsAndBiases_input_file, 'r') as file:
    # Read the entire content and parse it as JSON
    data = file.read()
    parsed_data = json.loads(data)

# Extract the first 784 weights from the parsed data
weights = parsed_data["weights"][0][0][:784]

# Write the weights to the output text file
with open(weights_txt_file, 'w') as file:
    for weight in weights:
        file.write(f"{weight}\n")

print(f"First 784 weights saved to '{weights_txt_file}'.")

# Read values from both files
with open(digit_output_decimal_file, 'r') as test_file, open(weights_txt_from_mif, 'r') as weights_file:
    # Read lines from both files and convert them to float values
    test_data = [float(line.strip()) for line in test_file]
    weights = [float(line.strip()) for line in weights_file]

# Ensure both files have the same number of values
min_length = min(len(test_data), len(weights))
if len(test_data) != len(weights):
    print("Warning: Files have different lengths; only processing the overlapping values.")

# Calculate the sum of all multiplications
total_sum = 0
for i in range(min_length):
    mul = test_data[i] * weights[i]
    #print(f"Multiplication {i + 1}: {test_data[i]} * {weights[i]} = {mul}")
    total_sum = total_sum + mul

# Print the final result
print("Sum of all multiplications:", total_sum)

bias_values = read_and_decode(bias_mif_file)
print("Bias:", bias_values[0])

# Print the final result
print("Sum with bias:", total_sum + bias_values[0])
