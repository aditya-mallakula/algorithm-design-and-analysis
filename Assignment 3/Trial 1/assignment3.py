import sys
import threading

sys.setrecursionlimit(10**6)


def main():
    import sys
    import os

    if len(sys.argv) != 2:
        print("Usage: python assignment3.py Input.txt")
        return

    input_file = sys.argv[1]
    output_file = input_file.replace('Input', 'Output', 1)

    # Read input from file
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()

    if len(lines) < 3:
        print("Input file must contain at least three lines.")
        return

    s1 = lines[0]
    s2 = lines[1]
    s3 = lines[2]

    len_s1 = len(s1)
    len_s2 = len(s2)
    len_s3 = len(s3)

    if len_s1 + len_s2 != len_s3:
        # Early check
        interleaving_exists = False
        total_interleavings = 0
        substrings_s1 = []
        substrings_s2 = []
    else:
        memo = {}
        total_interleavings = 0
        substrings_s1 = []
        substrings_s2 = []
        substrings_found = False

        max_substring_difference = 1

        from collections import defaultdict

        def dp(i, j, last_used, n_s1, n_s2, path_s1, path_s2):
            nonlocal total_interleavings, substrings_found

            key = (i, j, last_used, n_s1, n_s2)
            if key in memo:
                return memo[key]

            k = i + j

            if k == len_s3:
                if i == len_s1 and j == len_s2:
                    if abs(n_s1 - n_s2) <= 1:
                        total_interleavings += 1
                        if not substrings_found:
                            # Record the substrings used
                            substrings_s1.extend(path_s1)
                            substrings_s2.extend(path_s2)
                            substrings_found = True
                        return 1
                    else:
                        return 0
                else:
                    return 0

            count = 0

            if last_used != 1 and n_s1 <= n_s2 + 1 and i < len_s1:
                # Try to take a substring from s1 starting at i
                max_len = min(len_s1 - i, len_s3 - k)
                for l in range(max_len, 0, -1):
                    if s1[i:i+l] == s3[k:k+l]:
                        # Proceed to next state
                        res = dp(i+l, j, 1, n_s1+1, n_s2, path_s1 + [s1[i:i+l]], path_s2)
                        count += res
            if last_used != 2 and n_s2 <= n_s1 +1 and j < len_s2:
                # Try to take a substring from s2 starting at j
                max_len = min(len_s2 - j, len_s3 - k)
                for l in range(max_len, 0, -1):
                    if s2[j:j+l] == s3[k:k+l]:
                        res = dp(i, j+l, 2, n_s1, n_s2+1, path_s1, path_s2 + [s2[j:j+l]])
                        count += res
            memo[key] = count
            return count

        total_interleavings = dp(0, 0, 0, 0, 0, [], [])

        interleaving_exists = total_interleavings > 0

    # Write output to file
    with open(output_file, 'w') as f:
        f.write(f"Interleaving exists: {interleaving_exists}, Count of interleavings: {total_interleavings}\n")
        if interleaving_exists:
            f.write("s1 substrings: " + ', '.join(substrings_s1) + '\n')
            f.write("s2 substrings: " + ', '.join(substrings_s2) + '\n')

if __name__ == "__main__":
    threading.Thread(target=main).start()
