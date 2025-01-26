

import sys

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
        men_preferences[man] = preferences
    
    # Read women's preferences
    for i in range(n + 1, 2 * n + 1):
        # Split each line into woman and her preference list
        line = lines[i].strip().split()
        woman = line[0]
        preferences = line[1:]
        women_preferences[woman] = preferences
    
    # Return the number of participants and their preference lists
    return n, men_preferences, women_preferences


def gale_shapley(n, men_preferences, women_preferences):
    # List of free men
    free_men = list(men_preferences.keys())
    # Dictionary to store current engagements of women
    women_current = {woman: None for woman in women_preferences}
    # Dictionary to keep track of the next woman each man should propose to
    men_next_proposal = {man: 0 for man in men_preferences}
    # Counter for the number of proposals made
    proposals = 0
    
    # Create a dictionary to rank men according to each woman's preferences
    women_rankings = {}
    for woman, preferences in women_preferences.items():
        women_rankings[woman] = {man: rank for rank, man in enumerate(preferences)}
    
    # Loop until there are no free men left
    while free_men:
        # Get the first free man from the list
        man = free_men.pop(0)
        # Get the man's preference list
        man_pref_list = men_preferences[man]
        # Get the next woman the man should propose to
        woman = man_pref_list[men_next_proposal[man]]
        # Increment the proposal count for the man
        men_next_proposal[man] += 1
        # Increment the total number of proposals
        proposals += 1
        
        print(f"{man} proposes to {woman}")  # Print each proposal
        
        if women_current[woman] is None:
            # If the woman is free, engage her with the man
            women_current[woman] = man
        else:
            # If the woman is already engaged, check if she prefers this new proposal
            current_man = women_current[woman]
            if women_rankings[woman][man] < women_rankings[woman][current_man]:
                # If the woman prefers the new man, engage her with the new man
                women_current[woman] = man
                # Add the current engaged man back to the free men list
                free_men.append(current_man)
            else:
                # If the woman prefers her current engagement, the new man remains free
                free_men.append(man)
    
    # Return the final matching and the total number of proposals made
    return women_current, proposals


def write_output(filename, matching, proposals):
    # Open the output file in write mode
    with open(filename, 'w') as file:
        # Write each man-woman pair to the file
        for woman, man in matching.items():
            file.write(f"{man} {woman}\n")
        # Write the total number of proposals made
        file.write(f"{proposals}\n")


def main():
    # Define the input and output file names
    if len(sys.argv) != 2:
        print("Usage: python assignment1.py <input_filename>")
        return
    input_filename = sys.argv[1]
    output_filename = 'Output.txt'
    output_toverify_filename = 'OutputToBeVerified.txt'

    # Read the input data
    n, men_preferences, women_preferences = read_input(input_filename)
    # Execute the Gale-Shapley algorithm
    matching, proposals = gale_shapley(n, men_preferences, women_preferences)
    # Write the output data
    write_output(output_filename, matching, proposals)
    write_output(output_toverify_filename, matching, proposals)

if __name__ == "__main__":
    # Call the main function
    main()
