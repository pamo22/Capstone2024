import timeit

def comparison_cancel (file1, file2, outputname):
    start = timeit.default_timer()
    with open(file1, 'r') as fileA, open(file2, 'r') as fileB, open(outputname,"w") as output:
        print("Comparing ",file1, " to ", file2, " exporting differences to ",outputname)
        print("Differences detected: ")
        linesA = fileA.readlines()
        linesB = fileB.readlines()

        diff_lista = [line_a for line_a in linesA if line_a not in linesB]

        for line in diff_lista:
            print(line)
            output.write(line)


    stop = timeit.default_timer()
    print('Comparison time: ', stop - start)


