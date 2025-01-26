import sys

def read_jobs_from_file(file_name):
    with open(file_name, 'r') as file:
        n = int(file.readline().strip())  # Number of jobs
        jobs = []
        for i in range(n):
            job_data = list(map(int, file.readline().strip().split()))
            jobs.append((job_data[0], job_data[1], job_data[2]))  # (JobID, start, end)
        return jobs

def write_output_to_file(file_name, total_jobs, M1_jobs, M2_jobs):
    with open(file_name, 'w') as file:
        file.write(f"{total_jobs}\n")
        file.write(" ".join(map(str, M1_jobs)) + "\n")
        file.write(" ".join(map(str, M2_jobs)) + "\n")

def schedule_jobs(jobs):
    # Sort jobs by their end time
    jobs.sort(key=lambda job: job[2])  # Sort by job[2] which is the end time
    
    M1_jobs = []
    M2_jobs = []
    end_time_M1 = 0
    end_time_M2 = 0
    total_jobs = 0
    
    for job in jobs:
        job_id, start, end = job
        # Check if we can schedule it on M1
        if start >= end_time_M1:
            M1_jobs.append(job_id)
            end_time_M1 = end
            total_jobs += 1
        # If not M1, check M2
        elif start >= end_time_M2:
            M2_jobs.append(job_id)
            end_time_M2 = end
            total_jobs += 1
    
    return total_jobs, M1_jobs, M2_jobs

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python assignment2.py Input.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = input_file.replace("Input", "Output")
    
    jobs = read_jobs_from_file(input_file)
    total_jobs, M1_jobs, M2_jobs = schedule_jobs(jobs)
    write_output_to_file(output_file, total_jobs, M1_jobs, M2_jobs)
