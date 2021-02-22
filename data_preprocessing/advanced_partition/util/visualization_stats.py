import statistics
import os
import h5py
import matplotlib.pyplot as plt
import argparse


parser = argparse.ArgumentParser()

parser.add_argument('--partition_name', type=str, metavar='PN',
                        help='name of the method ')
parser.add_argument('--partition_file', type=str, default='data/partition_files/wikiner_partition.h5',
                        metavar="DF", help='data file path')
parser.add_argument('--task_name', type=str, metavar="TN", help="task name")


args = parser.parse_args()

f = h5py.File(args.partition_file,"r")

lda_samples = []
lda_total = 0
partition_name = ""
client_number = 0

for i in f.keys():
    if args.partition_name in i:
        partition_name = i
        client_number = f[i+"/n_clients"][()]
        break

partition_data_path = "/"+partition_name+"/partition_data/"

for i in f[partition_data_path].keys():
    train_path = partition_data_path+str(i)+'/train/'
    test_path = partition_data_path+str(i)+'/test/'
    lda_samples.append(len(f[train_path][()]) + len(f[test_path][()]))
    lda_total = lda_total + len(f[train_path][()]) + len(f[test_path][()])



f.close()


print("")
print("users")
print(client_number)

print("sample total")
print(lda_total)

print("sample mean")
mean  = lda_total / client_number
print(mean)

print("std")
std = statistics.stdev(lda_samples)
print(std)

print("std/mean")
print(std/mean)

data_dir = "./partition_figure"

plt.hist(lda_samples) 
fig_name = args.task_name + " %s_hist_nolabel.png" % args.partition_name
fig_dir = os.path.join(data_dir, fig_name)
plt.savefig(fig_dir)
plt.title(args.task_name)
plt.xlabel('number of samples')
plt.ylabel("number of clients")
fig_name = args.task_name + " %s_hist.png" % args.partition_name
fig_dir = os.path.join(data_dir, fig_name)
plt.savefig(fig_dir)

