# Team members: NAME - EMAIL - UID
# 1. Chris Davis Jaldi – jaldi.2@wright.edu – U01099335
# 2. Aditya Mallakula – mallakula.2@wright.edu – U01093160
# 3. Vanaja Uppala – uppala.19@wright.edu – U01080568

import sys

class JobScheduler:
    def __init__(self, input_file):
        self.input_file = input_file
        self.jobs = []
        self.m1_jobs = []
        self.m2_jobs = []
        self.total_jobs = 0
        self.m1_end = 0
        self.m2_end = 0
        self.output_file = self.generate_output_filename()

    def generate_output_filename(self):
        # Determine the output filename based on the input file name
        if not self.input_file.rstrip('.txt').isalpha() and self.input_file.rstrip('.txt').isalnum():
            return f'Output{"".join(filter(str.isdigit, self.input_file))}.txt'
        return "Output.txt"

    """
    Greedy Heuristic Used:
    ----------------------

    This scheduling algorithm's greedy heuristic prioritizes the earliest job finish time:

    Jobs are scheduled by selecting the one that completes the quickest and can be placed on an available machine (prioritizing machine M1 over M2).
    By sorting the jobs by end time, the algorithm ensures that each job selected leaves the most amount of time for subsequent jobs to be scheduled.
    """

    def load_jobs(self):
        # Load jobs from the input file
        try:
            with open(self.input_file, 'r') as file:
                n = int(file.readline().strip())
                for line in file:
                    job_id, start, end = map(int, line.strip().split())
                    self.jobs.append((job_id, start, end))
        except FileNotFoundError:
            print(f"Error: File '{self.input_file}' does not exist.")
            sys.exit(1)
        except ValueError:
            print("Error: Input file is not in the expected format.")
            sys.exit(1)
    """
    Pseudocode - Job scheduling algorithm:
    -----------

    function JobSchedulerAlgorithm(input_file):
    Initialize M1_jobs as an empty list
    Initialize M2_jobs as an empty list
    Initialize M1_end to 0  # Tracks the finish time of the latest job on machine M1
    Initialize M2_end to 0  # Tracks the finish time of the latest job on machine M2
    Initialize total_jobs to 0  # Tracks the total number of scheduled jobs

    jobs = load_jobs_from_file(input_file)  # Load jobs from the input file
    sort jobs by end_time in ascending order

    for each job in jobs:
        job_id, start_time, end_time = job

        if start_time >= M1_end:
            assign job to M1:
                add job_id to M1_jobs
                M1_end = end_time  # Update M1's end time
                total_jobs += 1  # Increment the total number of jobs scheduled
        else if start_time >= M2_end:
            assign job to M2:
                add job_id to M2_jobs
                M2_end = end_time  # Update M2's end time
                total_jobs += 1  # Increment the total number of jobs scheduled

    return the final schedule of jobs assigned to M1 and M2, and total_jobs count

    """

    def schedule_jobs(self):
        # Sort by end time (third element of the tuple)
        self.jobs.sort(key=lambda job: job[2])

        # Schedule jobs on M1 and M2
        for job_id, start, end in self.jobs:
            if start >= self.m1_end:  # Schedule on M1 if it is free
                self.m1_jobs.append(job_id)
                self.m1_end = end
                self.total_jobs += 1
            elif start >= self.m2_end:  # Otherwise, schedule on M2 if it is free
                self.m2_jobs.append(job_id)
                self.m2_end = end
                self.total_jobs += 1

    def write_output(self):
        # Write the scheduling results to the output file
        with open(self.output_file, 'w') as file:
            file.write(f"{self.total_jobs}\n")
            file.write(" ".join(map(str, self.m1_jobs)) + "\n")
            file.write(" ".join(map(str, self.m2_jobs)) + "\n")

    def run(self):
        # Load, schedule, and write results
        self.load_jobs()
        self.schedule_jobs()
        self.write_output()

def main():
    # Validate the command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python assignment2.py <input_filename>")
        sys.exit(1)

    # Get the input file from command line
    input_file = sys.argv[1]

    scheduler = JobScheduler(input_file)
    scheduler.run()

if __name__ == "__main__":
    main()

"""
Time Complexity:
---------------
Job Loading Complexity:
Reading n jobs from the input file takes O(n) time.

Sorting Jobs:
Sorting the jobs by their end times takes O(nlogn).

Scheduling Jobs:
Iterating through the sorted jobs and scheduling them takes O(n) time.

Overall Complexity: O(nlogn)
The dominant step is the sorting of the jobs, so the overall time complexity of the algorithm is O(nlogn).
"""