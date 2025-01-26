import os

# Directory for storing generated test cases
output_dir = "stress_test_cases"
os.makedirs(output_dir, exist_ok=True)

# Function to create a stress test case
def create_test_case(file_number, len_s1, len_s2, alternating=True):
    """
    Generates test case with strings s1, s2, and s3.
    :param file_number: Identifier for the test case file.
    :param len_s1: Length of s1 string.
    :param len_s2: Length of s2 string.
    :param alternating: Whether the strings should alternate in s3.
    :return: File paths for input and expected output files.
    """
    # Generate s1 and s2
    s1 = 'a' * len_s1
    s2 = 'b' * len_s2

    if alternating:
        # Generate alternating interleaving for s3
        s3 = ''.join(a + b for a, b in zip(s1, s2)) + s1[len(s2):] + s2[len(s1):]
    else:
        # Random concatenation
        s3 = s1 + s2

    # Write input file
    input_filename = os.path.join(output_dir, f"Input{file_number}.txt")
    with open(input_filename, 'w') as f:
        f.write(f"{s1}\n{s2}\n{s3}\n")

    # Write expected output file (placeholders for now)
    output_filename = os.path.join(output_dir, f"Output{file_number}.txt")
    with open(output_filename, 'w') as f:
        f.write(f"Expected interleaving check to run on Input{file_number}.txt\n")

    return input_filename, output_filename

# Generate multiple test cases
test_cases = []
for i, (len_s1, len_s2, alternating) in enumerate([
    (10, 10, True),  # Small balanced case
    (100, 50, True),  # Larger s1
    (50, 100, True),  # Larger s2
    (500, 500, True),  # Medium balanced case
    (1000, 1000, True),  # Large balanced case
    (2000, 1000, True),  # Imbalanced case, s1 larger
    (1000, 2000, True),  # Imbalanced case, s2 larger
    (5000, 5000, True),  # Stress case
    (10000, 10000, True),  # Larger stress case
    (10000, 10000, False)  # Non-alternating stress case
]):
    test_cases.append(create_test_case(i, len_s1, len_s2, alternating))

print("Test cases generated in the 'stress_test_cases' directory.")
