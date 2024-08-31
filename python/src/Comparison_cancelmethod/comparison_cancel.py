import timeit

example1 = "eg_1.txt"
example2 = "eg_2.txt"
test1 = "MonteChristo.txt"
test2 = "MonteChristo_altered.txt"

def comparison_cancel (file1, file2, outputname):
    with open(file1, 'r') as fileA, open(file2, 'r') as fileB, open(outputname,"w") as output:
        print("Comparing ",file1, " to ", file2, " exporting differences to ",outputname)
        print("Differences detected: ")
        linesA = fileA.readlines()
        linesB = fileB.readlines()

        diff_lista = [line_a for line_a in linesA if line_a not in linesB]

        for line in diff_lista:
            print(line)
            output.write(line)


start = timeit.default_timer()
#comparison_cancel(example1, example2,"eg1_differences.txt")
#comparison_cancel(example2, example1,"eg2_differences.txt")

comparison_cancel(test1, test2,"t1_differences.txt")
comparison_cancel(test2, test1,"t2_differences.txt")

stop = timeit.default_timer()
print('Time: ', stop - start)

