# Team members: NAME - EMAIL - UID
# 1. Aditya Mallakula – mallakula.2@wright.edu – U01093160
# 2. Chris Davis Jaldi – jaldi.2@wright.edu – U01099335
# 3. Vanaja Uppala – uppala.19@wright.edu – U01080568

import sys

class Human:
    def __init__(self, human_name, human_preferences):
        self.human_name = human_name
        self.human_preferences = human_preferences
        self.current_partner = None
        self.next_proposal_index = 0

    def get_next_proposal(self):
        if self.next_proposal_index < len(self.human_preferences):
            return self.human_preferences[self.next_proposal_index]
        return None

    def propose(self):
        proposal = self.get_next_proposal()
        self.next_proposal_index += 1
        return proposal

class FileHandler:
    @staticmethod
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

    @staticmethod
    def write_output(filename, matching, proposals):
        # Open the output file in write mode
        with open(filename, 'w') as file:
            # Write each man-woman pair to the file
            for woman, man in matching.items():
                file.write(f"{man} {woman}\n")
            # Write the total number of proposals made
            file.write(f"{proposals}\n")

class StableMarriage:
    def __init__(self, men_preferences, women_preferences):
        self.men = {name: Human(name, preferences) for name, preferences in men_preferences.items()}
        self.women = {name: Human(name, preferences) for name, preferences in women_preferences.items()}
        self.free_men = list(self.men.values())
        self.women_rankings = self._compute_women_rankings()
        self.proposals_count = 0

    def _compute_women_rankings(self):
        rankings = {}
        for woman_name, woman in self.women.items():
            rankings[woman_name] = {man: rank for rank, man in enumerate(woman.human_preferences)}
        return rankings

    def engage(self, woman, man):
        if woman.current_partner:
            # If woman is already engaged, her current partner becomes free
            self.free_men.append(self.men[woman.current_partner])
        woman.current_partner = man.human_name
        man.current_partner = woman.human_name

    def is_preferred(self, woman, new_man):
        current_man = self.men[woman.current_partner]
        return self.women_rankings[woman.human_name][new_man.human_name] < self.women_rankings[woman.human_name][current_man.human_name]


    """
    Pseudocode - Gale Shapley Algorithm:
    
    function GaleShapleyAlgorithm():
        Initialize free_men as a list of all men
        Initialize proposals_count to 0

        while free_men is not empty:
            man = remove first man from free_men
            woman_name = man's next preferred woman to propose to
            proposals_count += 1

            if woman_name is None:
                continue  # No more women to propose to, move on to the next man

            woman = get woman object by woman_name

            if woman is not engaged:
                engage(man, woman)  # Engage the man and the woman
            else:
                if woman prefers the new man over her current partner:
                    engage(man, woman)  # Engage the man and the woman
                else:
                    add man back to free_men  # Man remains free, woman stays with current partner

        return the final matching of women to their partners and proposals_count

    """
    def gale_shapley_algorithm(self):
        while self.free_men:
            # Get the first free man from the list
            man = self.free_men.pop(0)
            # Get the next woman the man should propose to
            woman_name = man.propose()
            # Counter for the number of proposals made
            self.proposals_count += 1

            if woman_name is None:
                continue  # No more women to propose to
            
            woman = self.women[woman_name]
            print(f"{man.human_name} proposes to {woman.human_name}") # Print each proposal

            if not woman.current_partner:
                # If the woman is free, engage her with the man
                self.engage(woman, man)
            else:
                # Check if the woman prefers this man over her current partner
                if self.is_preferred(woman, man):
                    self.engage(woman, man)  # If the woman prefers the new man, engage her with the new man
                else:
                    # If the woman prefers her current engagement, the new man remains free
                    self.free_men.append(man)

        return {woman.human_name: woman.current_partner for woman in self.women.values()}, self.proposals_count

class StableMarriageApp:
    def __init__(self, input_filename, output_filename, verification_filename):
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.verification_filename = verification_filename

    def run(self):
        # Read input data
        n, men_preferences, women_preferences = FileHandler.read_input(self.input_filename)
        
        # Execute Gale-Shapley algorithm
        stable_marriage = StableMarriage(men_preferences, women_preferences)
        matching, proposals = stable_marriage.gale_shapley_algorithm()
        
        # Write output
        FileHandler.write_output(self.output_filename, matching, proposals)
        FileHandler.write_output(self.verification_filename, matching, proposals)

def main():
    # Define the input and output file names
    if len(sys.argv) != 2:
        print("Usage: python assignment1.py <input_filename>")
        return
    input_filename = sys.argv[1]
    output_filename = 'Output.txt'
    verification_filename = 'OutputToBeVerified.txt'

    app = StableMarriageApp(input_filename, output_filename, verification_filename)
    app.run()

if __name__ == "__main__":
    # Call the main function
    main()
