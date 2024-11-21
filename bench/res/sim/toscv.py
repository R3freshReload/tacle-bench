import os

def extract_stack_cache_statistics(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    
    stats = []
    start_collecting = 0
    
    for line in lines:
        if "Stack Cache Statistics:" in line:
            start_collecting = 1
            continue
        if "total     % cycles" in line or "Data Cache Statistics:" in line or "total        hit      miss    miss-rate     reuse" in line or "total        % ops" in line:
            start_collecting = 2
            continue
        if start_collecting == 1:
            start_collecting = 2
            continue
        if start_collecting == 2:
            # Check if the line contains statistics data
            if ':' not in line:
                start_collecting = 0
                continue
            parts = line.split(':')
            if len(parts) < 2:
                continue
            print("adding values")
            values = parts[1].strip().split()
            stats.extend(values)
    
    # Debugging: Print the collected stats
    print(f"File: {file_name}, Stats: {stats}")
    
    return file_name + ";" + ';'.join(stats) if stats else file_name + ';No Data'

def process_directory(directory, output_file_name):
    directory_path = os.fsdecode(directory)
    
    with open(output_file_name, 'w') as outputFile:
        for file in sorted(os.listdir(directory_path)):
            filename = os.fsdecode(file)
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):  # Ensure it's a file and not a directory
                csv_line = extract_stack_cache_statistics(file_path)
                outputFile.write(csv_line + "\n")

# Process the "opt" directory
process_directory("opt", "opt.csv")

# Process the "noOpt" directory
process_directory("noOpt", "noOpt.csv")

# Process the "arrayOpt" directory
process_directory("arrayOpt", "arrayOpt.csv")
