import sys

def schedule_jobs(input_file, output_file):
    # Read the input from the input file
    jobs = []
    with open(input_file, 'r') as file:
        n = int(file.readline().strip())  # Read the number of jobs
        for line in file:
            job_id, start, end = map(int, line.strip().split())
            jobs.append((job_id, start, end))
    
    # Sort jobs by their end time
    jobs.sort(key=lambda job: job[2])  # Sort by end time (third element of the tuple)
    
    m1_end = m2_end = 0  # Tracks the end time of jobs on M1 and M2
    m1_jobs = []  # Jobs scheduled on M1
    m2_jobs = []  # Jobs scheduled on M2
    total_jobs = 0  # Total number of scheduled jobs
    
    for job_id, start, end in jobs:
        if start >= m1_end:  # Schedule on M1 if it is free
            m1_jobs.append(job_id)
            m1_end = end
            total_jobs += 1
        elif start >= m2_end:  # Otherwise, schedule on M2 if it is free
            m2_jobs.append(job_id)
            m2_end = end
            total_jobs += 1
    
    # Write the output to the output file
    with open(output_file, 'w') as file:
        file.write(f"{total_jobs}\n")
        file.write(" ".join(map(str, m1_jobs)) + "\n")
        file.write(" ".join(map(str, m2_jobs)) + "\n")

if __name__ == "__main__":
    input_file = sys.argv[1]  # Input file passed as command-line argument
    output_file = input_file.replace("Input", "Output")  # Create corresponding output file name
    schedule_jobs(input_file, output_file)
