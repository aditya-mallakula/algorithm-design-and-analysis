# Team members: NAME - EMAIL - UID
# 1. Chris Davis Jaldi – jaldi.2@wright.edu – U01099335
# 2. Aditya Mallakula – mallakula.2@wright.edu – U01093160
# 3. Vanaja Uppala – uppala.19@wright.edu – U01080568

import sys
import os

def read_input_file(filename):
    with open(filename, 'r') as file:
        s1 = file.readline().strip()
        s2 = file.readline().strip()
        s3 = file.readline().strip()
    return s1, s2, s3

def write_output_file(filename, interleaving_exists, count, s1_substrings, s2_substrings):
    with open(filename, 'w') as file:
        file.write(f"Interleaving exists: {interleaving_exists}, Count of interleavings: {count}\n")
        if interleaving_exists:
            file.write(f"s1 substrings: {', '.join(s1_substrings)}\n")
            file.write(f"s2 substrings: {', '.join(s2_substrings)}\n")

def is_interleaving(s1, s2, s3):
    n, m, p = len(s1), len(s2), len(s3)
    if n + m != p:
        return False, 0, [], []

    # dp[i][j] will be True if s3[0:i+j] is an interleaving of s1[0:i] and s2[0:j]
    dp = [[False]*(m+1) for _ in range(n+1)]
    dp[0][0] = True  # Empty strings are interleaving

    # Fill first column
    for i in range(1, n+1):
        dp[i][0] = dp[i-1][0] and s1[i-1] == s3[i-1]

    # Fill first row
    for j in range(1, m+1):
        dp[0][j] = dp[0][j-1] and s2[j-1] == s3[j-1]

    # Fill the dp table
    for i in range(1, n+1):
        for j in range(1, m+1):
            k = i + j - 1
            dp[i][j] = (dp[i-1][j] and s1[i-1] == s3[k]) or (dp[i][j-1] and s2[j-1] == s3[k])

    interleaving_exists = dp[n][m]

    # Now count the number of interleavings
    dp_count = [[0]*(m+1) for _ in range(n+1)]
    dp_count[0][0] = 1

    for i in range(1, n+1):
        dp_count[i][0] = dp_count[i-1][0] if s1[i-1] == s3[i-1] else 0

    for j in range(1, m+1):
        dp_count[0][j] = dp_count[0][j-1] if s2[j-1] == s3[j-1] else 0

    for i in range(1, n+1):
        for j in range(1, m+1):
            k = i + j - 1
            if s1[i-1] == s3[k]:
                dp_count[i][j] += dp_count[i-1][j]
            if s2[j-1] == s3[k]:
                dp_count[i][j] += dp_count[i][j-1]

    count = dp_count[n][m]

    # Backtracking to find one valid interleaving with substrings
    s1_substrings = []
    s2_substrings = []
    if interleaving_exists:
        i, j = n, m
        s1_parts = []
        s2_parts = []
        s1_current = ''
        s2_current = ''
        last_used = None

        while i > 0 or j > 0:
            k = i + j - 1
            moved = False

            if i > 0 and dp[i-1][j] and s1[i-1] == s3[k]:
                if last_used != 's1':
                    if s2_current:
                        s2_parts.append(s2_current[::-1])
                        s2_current = ''
                    s1_current = s1[i-1]
                else:
                    s1_current += s1[i-1]
                last_used = 's1'
                i -= 1
                moved = True
            elif j > 0 and dp[i][j-1] and s2[j-1] == s3[k]:
                if last_used != 's2':
                    if s1_current:
                        s1_parts.append(s1_current[::-1])
                        s1_current = ''
                    s2_current = s2[j-1]
                else:
                    s2_current += s2[j-1]
                last_used = 's2'
                j -= 1
                moved = True

            if not moved:
                # This situation shouldn't occur if dp table is correctly filled
                break

        # Add any remaining substrings
        if s1_current:
            s1_parts.append(s1_current[::-1])
        if s2_current:
            s2_parts.append(s2_current[::-1])

        s1_substrings = s1_parts[::-1]
        s2_substrings = s2_parts[::-1]

        # Ensure the number of substrings differ by at most one
        n_subs1 = len(s1_substrings)
        n_subs2 = len(s2_substrings)
        while abs(n_subs1 - n_subs2) > 1:
            # Merge adjacent substrings from the longer list
            if n_subs1 > n_subs2:
                s1_substrings = [s1_substrings[0] + s1_substrings[1]] + s1_substrings[2:]
            else:
                s2_substrings = [s2_substrings[0] + s2_substrings[1]] + s2_substrings[2:]
            n_subs1 = len(s1_substrings)
            n_subs2 = len(s2_substrings)

    return interleaving_exists, count, s1_substrings, s2_substrings

def main():
    # Get the input filename from command line argument
    input_filename = sys.argv[1]
    s1, s2, s3 = read_input_file(input_filename)

    interleaving_exists, count, s1_substrings, s2_substrings = is_interleaving(s1, s2, s3)

    # Prepare output filename
    base_name = os.path.basename(input_filename)
    name_part = base_name.replace('Input', '').replace('.txt', '')
    output_filename = f"Output{name_part}.txt" if name_part else "Output.txt"

    write_output_file(output_filename, interleaving_exists, count, s1_substrings, s2_substrings)

if __name__ == "__main__":
    main()
