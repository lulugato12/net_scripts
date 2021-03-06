# Clean PPI with ids and weight
# Lourdes B. Cajica
# 20 - 3 - 21

# to create folder
import os
import sys

# requirements for resource measurement
import time
import resource

# variables
path = "/datos/ot/lbcajica/"                                                # path to the current directory
log = open(path + "log.txt", "a+")                                          # log file
protein_link = path + "datos/9606.protein.links.v11.0.txt"
proteins = path + "output/proteins.txt"
minw = 700
if len(sys.argv) == 2:
    minw = int(sys.argv[1])

log.write("Filter ppi.\n")

# creates an output folder it not exists
def create_folder(path):
    try:
        os.mkdir(path + "output/")                                          # creates the folder where the data is going to be saved
    except OSError as error:
        print("The folder already exists.", end = " ")

# reads the data from the files
def reading_data(protein_link, proteins):
    file_ppi = open(protein_link, "r")                                      # opens the file that contiains the protein interactions
    file_proteins = open(proteins, "r")                                     # opens the file that contains the proteins

    data_proteins = file_proteins.readlines()                               # reads the data
    data_ppi = file_ppi.readlines()                                         # reads the dats
    data_ppi = data_ppi[1:]                                                 # deletes the head row

    file_ppi.close()
    file_proteins.close()

    return data_proteins, data_ppi

# executes the filtering process
def filter_exec(data_proteins, data_ppi, minw):
    # variables
    output_interactions = list()                                            # list that stores the ppi data
    count = 0

    for line in data_ppi:
        print("Interaction " + str(count) + "...", end = " ")
        l = line.split(" ")                                                 # splits the data line
        p1 = l[0].split(".")[1]                                             # reads the first protein
        p2 = l[1].split(".")[1]                                             # reads the second protein
        w = l[2].split("\n")[0]                                             # reads the interaction weight

        if (p1 + "\n") in data_proteins and (p2 + "\n") in data_proteins and int(w) >= minw:
             print("got one.", end = " ")
             output_interactions.append(p1 + "\t" + p2 + "\t0." + w + "\n") # saves the data

        print("finsihed.")
        count += 1

    return output_interactions

# saves the filtered data
def save_data(output_interactions):
    new_file = open(path + "/output/ppi"+str(minw)+".txt", "w")             # creates a new file to save the data
    new_file.writelines(output_interactions)                                # saves the data
    new_file.close()

print("Creating new folder...", end="")
create_folder(path)

print("finished.\nReading files...", end = "")
data_proteins, data_ppi = reading_data(protein_link, proteins)

print("finished.\nFiltering PPI...")
output_interactions = filter_exec(data_proteins, data_ppi, minw)

print("finished.\nSaving data...", end = "")
save_data(output_interactions)

print("finished.\nData saved in", path + "/output/ppi"+str(minw)+".txt")
print("It took: ", time.thread_time()/60, "min\n")

log.write("Time execution:" + str(time.thread_time()/60) + "min\n")
log.close()
