# Team members: NAME - EMAIL - UID
# 1. Chris Davis Jaldi – jaldi.2@wright.edu – U01099335
# 2. Aditya Mallakula – mallakula.2@wright.edu – U01093160
# 3. Vanaja Uppala – uppala.19@wright.edu – U01080568

import sys
sys.setrecursionlimit(10**6)


class StringInterleavingChecker:
    def __init__(self, input_file):
        self.input_file = input_file

        # Determine the output filename based on the input file name
        self.output_file = f'Output{"".join(filter(str.isdigit, self.input_file))}.txt' if not self.input_file.rstrip(
            '.txt').isalpha() and self.input_file.rstrip('.txt').isalnum() else "Output.txt"

        self.s1 = ""
        self.s2 = ""
        self.s3 = ""
        self.len_s1 = 0
        self.len_s2 = 0
        self.len_s3 = 0
        self.memo = {}
        self.total_interleavings = 0
        self.substrings_s1 = []
        self.substrings_s2 = []
        self.substrings_found = False

    def read_input(self):
        # Reads and validates the input file
        try:
            with open(self.input_file, 'r') as f:
                lines = f.read().splitlines()
        except FileNotFoundError:
            print(f"Error: File '{self.input_file}' not found.")
            return False

        if len(lines) < 3:
            print("Error: Input file must contain three lines: s1, s2, and s3.")
            return False

        self.s1, self.s2, self.s3 = lines[0], lines[1], lines[2]
        self.len_s1, self.len_s2, self.len_s3 = len(
            self.s1), len(self.s2), len(self.s3)

        if self.len_s1 + self.len_s2 != self.len_s3:
            self.write_output(False, 0, [], [])
            return False

        return True

    def write_output(self, interleaving_exists, total_interleavings, substrings_s1, substrings_s2):
        # Writes the result to the output file
        with open(self.output_file, 'w') as f:
            f.write(f"Interleaving exists: {interleaving_exists}, Count of interleavings: {total_interleavings}\n")
            if interleaving_exists:
                f.write("s1 substrings: " + ', '.join(substrings_s1) + '\n')
                f.write("s2 substrings: " + ', '.join(substrings_s2) + '\n')

    def check_interleaving(self):
        # Checks if s3 is an interleaving of s1 and s2.
        self._dp(0, 0, 0, 0, 0, [], [])
        interleaving_exists = self.total_interleavings > 0
        self.write_output(interleaving_exists, self.total_interleavings,
                          self.substrings_s1, self.substrings_s2)

    def _dp(self, i, j, last_used, n_s1, n_s2, path_s1, path_s2):
        # Recursive DP function for interleaving check
        key = (i, j, last_used, n_s1, n_s2)
        if key in self.memo:
            return self.memo[key]

        k = i + j  # Combined index in s3

        if k == self.len_s3:
            if i == self.len_s1 and j == self.len_s2 and abs(n_s1 - n_s2) <= 1:
                self.total_interleavings += 1
                if not self.substrings_found:
                    self.substrings_s1.extend(path_s1)
                    self.substrings_s2.extend(path_s2)
                    self.substrings_found = True
                return 1
            return 0

        count = 0

        def try_substring(source, idx, last_used_value, path, n_count):
            max_len = min(len(source) - idx, self.len_s3 - k)
            for l in range(max_len, 0, -1):
                if source[idx:idx+l] == self.s3[k:k+l]:
                    new_path = path + [source[idx:idx+l]]
                    res = self._dp(i + l * (source == self.s1), j + l * (source == self.s2),
                                   last_used_value, n_s1 +
                                   (source == self.s1), n_s2 +
                                   (source == self.s2),
                                   new_path if source == self.s1 else path_s1,
                                   new_path if source == self.s2 else path_s2)
                    nonlocal count
                    count += res

        if last_used != 1 and n_s1 <= n_s2 + 1 and i < self.len_s1:
            try_substring(self.s1, i, 1, path_s1, n_s1)

        if last_used != 2 and n_s2 <= n_s1 + 1 and j < self.len_s2:
            try_substring(self.s2, j, 2, path_s2, n_s2)

        self.memo[key] = count
        return count


def main():
    # Validate the command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python assignment3.py Input.txt")
        return

    # Get the input file from command line
    input_file = sys.argv[1]

    checker = StringInterleavingChecker(input_file)
    if checker.read_input():
        checker.check_interleaving()


if __name__ == "__main__":
    main()
