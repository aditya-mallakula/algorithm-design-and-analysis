import sys
import os


class FileHandler:
    # Handles file reading and writing

    @staticmethod
    def read_input_file(filename):
        # Reads input from a file
        with open(filename, 'r') as file:
            s1 = file.readline().strip()
            s2 = file.readline().strip()
            s3 = file.readline().strip()
        return s1, s2, s3

    @staticmethod
    def write_output_file(filename, interleaving_exists, count, s1_substrings, s2_substrings):
        # Writes the results to a file
        with open(filename, 'w') as file:
            file.write(f"Interleaving exists: {interleaving_exists}, Count of interleavings: {count}\n")
            if interleaving_exists:
                file.write(f"s1 substrings: {', '.join(s1_substrings)}\n")
                file.write(f"s2 substrings: {', '.join(s2_substrings)}\n")

"""
Algorithm CheckInterleaving(s1, s2, s3):
    Input: Strings s1, s2, and s3
    Output: Boolean (whether s3 is an interleaving of s1 and s2), count of interleavings, and the substrings

    1. Initialize n = length(s1), m = length(s2), p = length(s3)
    2. If n + m != p, return False, 0, [], []
       // Total length mismatch implies s3 cannot be formed.

    3. Create DP tables:
       - dp[n+1][m+1]: Boolean table to check interleaving validity
       - count[n+1][m+1]: Integer table to count distinct interleavings
    4. Set dp[0][0] = True and count[0][0] = 1
       // Base case: Empty strings interleave to form an empty string.

    5. Fill the first row and first column:
       - For i in [1, n]: 
           dp[i][0] = dp[i-1][0] AND s1[i-1] == s3[i-1]
           count[i][0] = count[i-1][0] if dp[i][0] else 0
       - For j in [1, m]: 
           dp[0][j] = dp[0][j-1] AND s2[j-1] == s3[j-1]
           count[0][j] = count[0][j-1] if dp[0][j] else 0

    6. Fill the rest of the DP table:
       - For i in [1, n]:
           For j in [1, m]:
               k = i + j - 1 // Index in s3
               dp[i][j] = (dp[i-1][j] AND s1[i-1] == s3[k]) OR (dp[i][j-1] AND s2[j-1] == s3[k])
               count[i][j] = count[i-1][j] + count[i][j-1] 
                             // Add counts if valid interleaving paths exist.

    7. Extract result:
       - If dp[n][m] is True:
           Use backtracking to extract substrings from s1 and s2 that interleave to form s3
       - Else:
           Return False, 0, [], []

    8. Return dp[n][m], count[n][m], substrings of s1, substrings of s2

"""
class InterleavingChecker:
    # Checks if a string is an interleaving of two other strings

    def __init__(self, s1, s2, s3):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3

    def is_interleaving(self):
        # Checks if s3 is an interleaving of s1 and s2
        n, m, p = len(self.s1), len(self.s2), len(self.s3)
        if n + m != p:
            return False, 0, [], []

        # Initializing tables
        dp = [[False] * (m + 1) for _ in range(n + 1)]
        interleaving_count = [[0] * (m + 1) for _ in range(n + 1)]

        # Base cases
        dp[0][0] = True
        interleaving_count[0][0] = 1

        for i in range(1, n + 1):
            dp[i][0] = dp[i - 1][0] and self.s1[i - 1] == self.s3[i - 1]
            interleaving_count[i][0] = interleaving_count[i - 1][0] if dp[i][0] else 0

        for j in range(1, m + 1):
            dp[0][j] = dp[0][j - 1] and self.s2[j - 1] == self.s3[j - 1]
            interleaving_count[0][j] = interleaving_count[0][j - 1] if dp[0][j] else 0

        # Fill the table
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                k = i + j - 1
                if dp[i - 1][j] and self.s1[i - 1] == self.s3[k]:
                    dp[i][j] = True
                    interleaving_count[i][j] += interleaving_count[i - 1][j]
                if dp[i][j - 1] and self.s2[j - 1] == self.s3[k]:
                    dp[i][j] = True
                    interleaving_count[i][j] += interleaving_count[i][j - 1]

        interleaving_exists = dp[n][m]
        count = interleaving_count[n][m]

        s1_substrings, s2_substrings = self._backtrack(
            dp) if interleaving_exists else ([], [])

        return interleaving_exists, count, s1_substrings, s2_substrings

    def _backtrack(self, dp):
        # Finds substrings that form the interleaving using backtracking
        i, j = len(self.s1), len(self.s2)
        s1_parts, s2_parts = [], []
        s1_current, s2_current = '', ''
        last_used = None

        while i > 0 or j > 0:
            k = i + j - 1
            moved = False

            if i > 0 and dp[i - 1][j] and self.s1[i - 1] == self.s3[k]:
                if last_used != 's1':
                    if s2_current:
                        s2_parts.append(s2_current[::-1])
                        s2_current = ''
                    s1_current = self.s1[i - 1]
                else:
                    s1_current += self.s1[i - 1]
                last_used = 's1'
                i -= 1
                moved = True

            elif j > 0 and dp[i][j - 1] and self.s2[j - 1] == self.s3[k]:
                if last_used != 's2':
                    if s1_current:
                        s1_parts.append(s1_current[::-1])
                        s1_current = ''
                    s2_current = self.s2[j - 1]
                else:
                    s2_current += self.s2[j - 1]
                last_used = 's2'
                j -= 1
                moved = True

            if not moved:
                break

        if s1_current:
            s1_parts.append(s1_current[::-1])
        if s2_current:
            s2_parts.append(s2_current[::-1])

        return s1_parts[::-1], s2_parts[::-1]


class InterleavingApp:
    # Main application class for running the interleaving check

    @staticmethod
    def run(input_filename):

        # Read input
        s1, s2, s3 = FileHandler.read_input_file(input_filename)

        # Check interleaving
        checker = InterleavingChecker(s1, s2, s3)
        interleaving_exists, count, s1_substrings, s2_substrings = checker.is_interleaving()

        # Prepare output filename
        output_filename = f'Output{"".join(filter(str.isdigit, input_filename))}.txt' if not input_filename.rstrip(
            '.txt').isalpha() and input_filename.rstrip('.txt').isalnum() else "Output.txt"

        # Write results
        FileHandler.write_output_file(
            output_filename, interleaving_exists, count, s1_substrings, s2_substrings)


if __name__ == "__main__":
    # Get the input filename from command line argument
    input_filename = sys.argv[1]
    InterleavingApp.run(input_filename)

