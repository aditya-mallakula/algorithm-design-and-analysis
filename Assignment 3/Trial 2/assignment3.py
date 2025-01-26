import sys
import os


def main():
    if len(sys.argv) != 2:
        print("Usage: python assignment3.py Input.txt")
        return

    input_file = sys.argv[1]
    output_file = input_file.replace('Input', 'Output', 1)

    # Read input from file
    try:
        with open(input_file, 'r') as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return

    if len(lines) < 3:
        print("Error: Input file must contain three lines: s1, s2, and s3.")
        return

    s1, s2, s3 = lines[0], lines[1], lines[2]

    len_s1, len_s2, len_s3 = len(s1), len(s2), len(s3)

    # Early check
    if len_s1 + len_s2 != len_s3:
        write_output(output_file, False, 0, [], [])
        return

    # Initialize DP table
    dp = [[None] * (len_s2 + 1) for _ in range(len_s1 + 1)]
    dp[0][0] = [([], [])]  # Base case: Empty substrings from s1 and s2

    # Fill the DP table
    for i in range(len_s1 + 1):
        for j in range(len_s2 + 1):
            if i == 0 and j == 0:
                continue

            current_interleavings = []

            # Extend with substrings from s1
            if i > 0 and dp[i - 1][j] is not None and s1[i - 1] == s3[i + j - 1]:
                for p1, p2 in dp[i - 1][j]:
                    if p1 and p1[-1] == s1[i - 1]:
                        new_p1 = p1[:-1] + [p1[-1] + s1[i - 1]]
                    else:
                        new_p1 = p1 + [s1[i - 1]]
                    current_interleavings.append((new_p1, p2))

            # Extend with substrings from s2
            if j > 0 and dp[i][j - 1] is not None and s2[j - 1] == s3[i + j - 1]:
                for p1, p2 in dp[i][j - 1]:
                    if p2 and p2[-1] == s2[j - 1]:
                        new_p2 = p2[:-1] + [p2[-1] + s2[j - 1]]
                    else:
                        new_p2 = p2 + [s2[j - 1]]
                    current_interleavings.append((p1, new_p2))

            dp[i][j] = current_interleavings if current_interleavings else None

    # Extract valid interleavings
    valid_interleavings = dp[len_s1][len_s2]
    if not valid_interleavings:
        write_output(output_file, False, 0, [], [])
        return

    # Filter valid interleavings for balanced substrings
    valid_interleavings = [
        (p1, p2) for p1, p2 in valid_interleavings if abs(len(p1) - len(p2)) <= 1
    ]

    if not valid_interleavings:
        write_output(output_file, False, 0, [], [])
        return

    # Result
    interleaving_exists = True
    total_interleavings = len(valid_interleavings)
    substrings_s1, substrings_s2 = valid_interleavings[0]

    write_output(output_file, interleaving_exists, total_interleavings, substrings_s1, substrings_s2)


def write_output(output_file, interleaving_exists, total_interleavings, substrings_s1, substrings_s2):
    """
    Writes the output to the specified file.
    """
    with open(output_file, 'w') as f:
        f.write(f"Interleaving exists: {interleaving_exists}, Count of interleavings: {total_interleavings}\n")
        if interleaving_exists:
            f.write("s1 substrings: " + ', '.join(substrings_s1) + '\n')
            f.write("s2 substrings: " + ', '.join(substrings_s2) + '\n')


if __name__ == "__main__":
    main()
