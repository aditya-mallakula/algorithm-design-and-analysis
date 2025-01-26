# Team members: NAME - EMAIL - UID
# 1. Aditya Mallakula – mallakula.2@wright.edu – U01093160
# 2. Chris Davis Jaldi – jaldi.2@wright.edu – U01099335
# 3. Vanaja Uppala – uppala.19@wright.edu – U01080568

import os
import sys

class PreferenceReader:
    """Class responsible for reading preferences from the input file."""
    
    def __init__(self, filename):
        self.filename = filename
    
    def read_input(self):
        """Reads the input file and returns the number of participants, men's preferences, and women's preferences."""

        # Open the input file in read mode
        with open(self.filename, 'r') as file:
            # Read all lines from the file
            lines = file.readlines()

        # The first line contains the number of men and women
        n = int(lines[0].strip())
        # Initialize dictionaries to store men and women's preference lists
        men_preferences = {}
        women_preferences = {}

        # Read men's preferences
        for i in range(1, n + 1):
            # Split each line into man and his preference list
            line = lines[i].strip().split()
            man = line[0]
            preferences = line[1:]
            # Store the preferences in the men_preferences dictionary
            men_preferences[man] = preferences

        # Read women's preferences
        for i in range(n + 1, 2 * n + 1):
            # Split each line into woman and her preference list
            line = lines[i].strip().split()
            woman = line[0]
            preferences = line[1:]
            # Store the preferences in the women_preferences dictionary
            women_preferences[woman] = preferences

        # Return the number of participants and their preference lists
        return n, men_preferences, women_preferences

class MatchingReader:
    """Class responsible for reading the matching result from the output file."""
    
    def __init__(self, filename):
        self.filename = filename
    
    def read_output(self):
        """Reads the output file and returns the matching and number of proposals."""
        
        # Open the output file in read mode
        with open(self.filename, 'r') as file:
            # Read all lines from the file
            lines = file.readlines()

        # Initialize a dictionary to store the matching
        matching = {}
        # Read each man-woman pair from the file
        for line in lines[:-1]:
            man, woman = line.strip().split()
            # Store the pair in the matching dictionary
            matching[woman] = man

        # Read the total number of proposals made
        proposals = int(lines[-1].strip())

        # Return the matching and the number of proposals
        return matching, proposals

class StabilityChecker:
    """Class responsible for checking the stability of the matching."""
    
    def __init__(self, input_file, output_file, verification_file):
        self.input_file = input_file
        self.output_file = output_file
        self.verification_file = verification_file

    def stabilityChecker(self):
        """Checks if the matching is stable and writes the result to the verification file."""
        # Read input data from the input file
        input_reader = PreferenceReader(self.input_file)
        n, men_preferences, women_preferences = input_reader.read_input()

        # Read output data from the output file
        output_reader = MatchingReader(self.output_file)
        matching, _ = output_reader.read_output()

        # Current engagements of women
        women_current = matching

        # Current engagements of men
        men_current = {man: woman for woman, man in matching.items()}

        # Create a dictionary to rank men according to each woman's preferences
        women_rankings = self._create_women_rankings(women_preferences)

        # Check stability
        is_stable = self._is_stable(men_preferences, women_current, women_rankings)

        # Write result to the verification file
        self._write_verification(is_stable)

    def _create_women_rankings(self, women_preferences):
        """Helper method to create rankings for women based on their preferences."""
        women_rankings = {}
        for woman, preferences in women_preferences.items():
            women_rankings[woman] = {man: rank for rank, man in enumerate(preferences)}
        return women_rankings

    def _is_stable(self, men_preferences, women_current, women_rankings):
        """Helper method to check if the matching is stable."""
        # Check for stability by iterating through each man's preferences
        for man, man_pref_list in men_preferences.items():
            for woman in man_pref_list:
                # Get the current engagement of the woman
                current_man = women_current[woman]
                # If the woman prefers the current man less than the proposing man, it's unstable
                if women_rankings[woman][man] < women_rankings[woman][current_man]:
                    # Return false to the verification
                    return False
        return True

    def _write_verification(self, is_stable):
        """Writes the stability result to the verification file."""
        # If no instability is found, write "stable" to the verification file, else write "unstable"
        result = "stable\n" if is_stable else "unstable\n"
        with open(self.verification_file, 'w') as file:
            file.write(result)

def generate_verified_filename(input_filename):
    """Generates a verified filename based on the input file name."""
    # Extract the number from the input filename (e.g., input1.txt -> 1)
    base_name = os.path.splitext(os.path.basename(input_filename))[0]
    number = ''.join([c for c in base_name if c.isdigit()])  # Extract the number part
    return f"Verified{number}.txt"  # e.g., Verified1.txt

if __name__ == "__main__":
    # Get input and output filenames from command line arguments
    if len(sys.argv) != 3:
        print("Usage: python stabilityChecker.py <inputX.txt> <OutputToBeVerifiedX.txt>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    # Dynamically generate the verified file name
    verification_filename = generate_verified_filename(input_filename)

    # Call the stability checker function
    stability_checker = StabilityChecker(input_filename, output_filename, verification_filename)
    stability_checker.stabilityChecker()

    
