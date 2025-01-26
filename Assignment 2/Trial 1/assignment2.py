import sys

def schedule_jobs(jobs):
    # Sort jobs by their end time (eᵢ)
    jobs.sort(key=lambda job: job[2])
    
    M1_end_time = 0  # Keeps track of when machine M1 becomes available
    M2_end_time = 0  # Keeps track of when machine M2 becomes available
    
    M1_jobs = []  # List of jobs scheduled on M1
    M2_jobs = []  # List of jobs scheduled on M2
    total_jobs = 0
    
    for job in jobs:
        job_id, start_time, end_time = job
        # Check if M1 is available for the job
        if start_time >= M1_end_time:
            M1_jobs.append(job_id)
            M1_end_time = end_time
            total_jobs += 1
        # If M1 is not available, check if M2 is available
        elif start_time >= M2_end_time:
            M2_jobs.append(job_id)
            M2_end_time = end_time
            total_jobs += 1
    
    # Return the total number of scheduled jobs and the job IDs for M1 and M2
    return total_jobs, M1_jobs, M2_jobs

def read_input(file_name):
    with open(file_name, 'r') as file:
        n = int(file.readline().strip())  # First line is the number of jobs
        jobs = []
        for _ in range(n):
            job_details = list(map(int, file.readline().strip().split()))
            jobs.append((job_details[0], job_details[1], job_details[2]))  # (JobID, Start Time, End Time)
        return jobs

def write_output(file_name, total_jobs, M1_jobs, M2_jobs):
    with open(file_name, 'w') as file:
        file.write(f"{total_jobs}\n")
        file.write(f"{' '.join(map(str, M1_jobs))}\n")
        file.write(f"{' '.join(map(str, M2_jobs))}\n")
    
    # Print to console as well
    print(f"{total_jobs}")
    print(f"{' '.join(map(str, M1_jobs))}")
    print(f"{' '.join(map(str, M2_jobs))}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python <program_file_name> Input.txt")
        sys.exit(1)

    input_file = sys.argv[1]  # Get the input file from the command-line argument
    jobs = read_input(input_file)
    
    # Schedule the jobs using the greedy algorithm
    total_jobs, M1_jobs, M2_jobs = schedule_jobs(jobs)
    
    # Write the output to the Output.txt file
    write_output("Output.txt", total_jobs, M1_jobs, M2_jobs)
