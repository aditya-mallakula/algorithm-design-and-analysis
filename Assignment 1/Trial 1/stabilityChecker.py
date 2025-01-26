def read_input(filename):
    # Open the input file in read mode
    with open(filename, 'r') as file:
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

def read_output(filename):
    # Open the output file in read mode
    with open(filename, 'r') as file:
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

def stability_checker(input_file, output_file, verification_file):
    # Read input data from the input file
    n, men_preferences, women_preferences = read_input(input_file)
    # Read output data from the output file
    matching, proposals = read_output(output_file)
    
    # Current engagements of women
    women_current = matching
    # Current engagements of men
    men_current = {man: woman for woman, man in matching.items()}
    
    # Create a dictionary to rank men according to each woman's preferences
    women_rankings = {}
    for woman, preferences in women_preferences.items():
        women_rankings[woman] = {man: rank for rank, man in enumerate(preferences)}
    
    # Check for stability by iterating through each man's preferences
    for man in men_preferences:
        man_pref_list = men_preferences[man]
        for woman in man_pref_list:
            # Get the current engagement of the woman
            current_man = women_current[woman]
            # If the woman prefers the current man less than the proposing man, it's unstable
            if women_rankings[woman][man] < women_rankings[woman][current_man]:
                # Write "unstable" to the verification file
                with open(verification_file, 'w') as file:
                    file.write("unstable\n")
                return
    
    # If no instability is found, write "stable" to the verification file
    with open(verification_file, 'w') as file:
        file.write("stable\n")

if __name__ == "__main__":
    # Define the input, output, and verification file names
    input_filename = 'VerifierTests/Input5.txt'
    output_filename = 'VerifierTests/OutputToBeVerified5.txt'
    verification_filename = 'VerifierTests/Verified5.txt'
    
    # Call the stability_checker function with the file names
    stability_checker(input_filename, output_filename, verification_filename)
