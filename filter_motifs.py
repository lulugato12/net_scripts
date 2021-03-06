# change ids by its name
# Lourdes B. Cajica
# 20 - 3 - 21

# to create folder
import os

# requirements for resource measurement
import time
import resource

# variables
path = "/datos/ot/lbcajica/"                                            # path to the current directory
log = open(path + "log.txt", "a+")                                      # log file
motifs = path + "datos/ToyMotifData.txt"                                # motif file
updates = path + "datos/mart_export.txt"                                # ids file
genes = path + "output/genes_output.txt"                                # genes used file

log.write("Filter motifs.\n")

# creates an output folder it not exists
def create_folder(path):
    try:
        os.mkdir(path + "output/")                                      # creates the folder where the data is going to be saved
    except OSError as error:
        print("The folder already exists.", end = " ")

# reads the data from the files
def reading_data(motifs, updates, genes):
    file_motif = open(motifs, "r")                                      # opens the file that contains the motif data
    file_names = open(updates, "r")                                     # opens the file that contains the name-id relation
    file_genes = open(genes, "r")                                       # opens the file that contains the genes

    original = file_motif.readlines()                                   # reads all the data
    update = file_names.readlines()                                     # reads all the data
    used_genes = file_genes.readlines()                                 # reads all the data

    file_names.close()
    file_motif.close()
    file_genes.close()

    return original, update, used_genes

# prepares the information
def prep_data(update, used_genes):
    tempo = list()

    # storage
    tf_name = list()                                                    # list of motif names
    gene_name = list()                                                  # list of gene names
    tf_id = list()                                                      # list of motif ids
    gene_id = list()                                                    # list of gene ids

    for l in update:
        line = l.split("\t")                                            # splits the data line
        gene_id.append(line[0])                                         # saves de gene id
        tf_id.append(line[1])                                           # saves the motif id
        gene_name.append(line[3])                                       # saves the gene name
        tf_name.append(line[4].split("\n")[0])                          # saves the motif name

    for l in used_genes:                                                # splits the data line to leave the gene clean
        line = l.split("\n")
        tempo.append(line[0])

    return gene_id, tf_id, gene_name, tf_name, tempo

# executes the filtering process
def filter_exec(gene_id, tf_id, gene_name, tf_name, used_genes):
    # variables
    output = list()                                                     # output data lines
    count = 0

    for p in original:
        print("line " + str(count) + "...", end = " ")
        prep = p.split("\t")                                            # splits the data line to get the motif and the gene
        line = ""
        if prep[0] in gene_name and prep[1] in gene_name:               # check if both the motif and the gene exists in the registries
            if gene_id[gene_name.index(prep[1])] in used_genes:
                print("got one.", end = " ")
                line += tf_id[gene_name.index(prep[0])] + "\t" + gene_id[gene_name.index(prep[1])] + "\t1.0\n"
                output.append(line)                                    # saves the motif id, the gene id and the weight 1.0
            count += 1
        print("finished.")

    return output

# saves the filtered data
def save_data(output):
    new_file = open(path + "output/motif.txt", "w")                     # creates a new file to save the motifs
    new_file.writelines(output)                                         # saves the data
    new_file.close()

print("Creating new folder...", end=" ")
create_folder(path)

print("finished.\nReading files...", end = " ")
original, update, used_genes = reading_data(motifs, updates, genes)

print("finished.\nPreparing data...", end = " ")
gene_id, tf_id, gene_name, tf_name, used_genes = prep_data(update, used_genes)

print("finished.\nFiltering names...")
output = filter_exec(gene_id, tf_id, gene_name, tf_name, used_genes)

print("finished.\nSaving data...", end = " ")
save_data(output)

print("finished.\nData saved in " + path + "motif.txt.")
print("It took: ", time.thread_time()/60, "min\n")

log.write("Time execution:" + str(time.thread_time()/60) + "min\n")
log.close()
