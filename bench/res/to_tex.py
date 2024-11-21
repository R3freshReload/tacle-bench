import os

def process_directory_platin(directory, outputFile):
    directory_path = os.fsdecode(directory)

    for file in sorted(os.listdir(directory_path)):
        filename = os.fsdecode(file)
        testname = filename.split("_")[1]
        optName = filename.split("_")[0].capitalize()
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):  # Ensure it's a file and not a directory
            with open(file_path, encoding="utf-8", errors='ignore') as file:
                for line in file.readlines():
                    newcommand = "\\newcommand{\\" + testname
                    value = "-1"
                    statname = ""
                    if " cycles: " in line:
                        statname = "Cycles"
                        value = line.split("cycles: ")[1].strip()
                    elif " cache-max-cycles-data: " in line:
                        statname = "MaxDataCycles"
                        value = line.split("cache-max-cycles-data: ")[1].strip()
                    else:
                        continue
                    newcommand += statname + optName + "}"
                    newcommand += "{" + value + "}"
                    outputFile.write(newcommand + "\n")
                outputFile.write("\n")

def process_directory_pasim(directory, outputFile):
    directory_path = os.fsdecode(directory)

    for file in sorted(os.listdir(directory_path)):
        filename = os.fsdecode(file)
        testname = filename.split("_")[1].split(".")[0]
        optName = filename.split("_")[0].capitalize()
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):  # Ensure it's a file and not a directory
            with open(file_path, encoding="utf-8", errors='ignore') as file:
                missstallcyclecounter = 0
                bytesreadcounter = 0
                byteswrittencounter = 0
                for line in file.readlines():
                    newcommand = "\\newcommand{\\" + testname
                    value = "-1"
                    statname = ""
                    if " Miss Stall Cycles " in line:
                        missstallcyclecounter += 1
                        if missstallcyclecounter == 2: # 2 is Data Cache Statistics
                            statname = "DataCacheStallCycles"
                            tmp = "".join(line.split(":")[1].split(" ")[0:-1])
                            value = tmp.strip()
                        else:
                            continue
                    elif " Bytes Read " in line:
                        bytesreadcounter += 1
                        if bytesreadcounter == 1: # 1 is Data Cache Statistics
                            statname = "DataCacheBytesRead"
                            tmp = [item for item in line.split(":")[1].split(" ") if item != ""][0]
                            value = tmp.strip()
                        elif bytesreadcounter == 2:  # 2 is Stack Cache Statistics
                            statname = "StackCacheBytesRead"
                            tmp = [item for item in line.split(":")[1].split(" ") if item != ""][0]
                            value = tmp.strip()
                        else:
                            continue
                    elif " Bytes Written " in line:
                        byteswrittencounter += 1
                        if byteswrittencounter == 1: # 1 is Data Cache Statistics
                            statname = "DataCacheBytesWrite"
                            tmp = [item for item in line.split(":")[1].split(" ") if item != ""][0]
                            value = tmp.strip()
                        elif byteswrittencounter == 2:  # 2 is Stack Cache Statistics
                            statname = "StackCacheBytesWrite"
                            tmp = [item for item in line.split(":")[1].split(" ") if item != ""][0]
                            value = tmp.strip()
                        else:
                            continue
                    elif "  Stall Cycles " in line:
                        statname = "MainMemoryStallCycles"
                        tmp = "".join(line.split(":")[1].split(" ")[0:-1])
                        value = tmp.strip()
                    else:
                        continue
                    newcommand += statname + optName + "}"
                    newcommand += "{" + value + "}"
                    outputFile.write(newcommand + "\n")
                outputFile.write("\n")


with open("outfile.tex", mode="w", encoding="utf-8") as file:
    process_directory_platin("platin/arrayOpt", file)
    process_directory_platin("platin/opt", file)
    process_directory_platin("platin/noOpt", file)
    process_directory_pasim("sim/arrayOpt", file)
    process_directory_pasim("sim/opt", file)
    process_directory_pasim("sim/noOpt", file)