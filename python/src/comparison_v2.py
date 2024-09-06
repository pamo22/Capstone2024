import timeit

class compare_obj:
    def __init__(self):
        return None

    def compare_file(self, file1: str, file2: str) -> [str] :
        with open(file1, 'r') as fileA, open(file2, 'r') as fileB:
            linesA = fileA.readlines()
            linesB = fileB.readlines()

            diff_list = [line_a for line_a in linesA if line_a not in linesB]
            return diff_list


    def compare_save_to_file(self, file1: str, file2: str, outputname: str):
        outputlist = self.compare_file(file1, file2)

        with open(outputname, 'w') as outputFile:
            for line in outputlist:
                outputFile.write(line)


    def compare_file_verbose(self, file1: str, file2: str):
            start = timeit.default_timer()

            with open(file1, 'r') as fileA, open(file2, 'r') as fileB:
                print("Comparing ",file1, " to ", file2)
                print("Differences detected: ")
                linesA = fileA.readlines()
                linesB = fileB.readlines()

                diff_list = [line_a for line_a in linesA if line_a not in linesB]

                print("Differences found: ")
                for line in diff_list:
                    print(line)

                return diff_list

            stop = timeit.default_timer()
            print('Comparison time: ', stop - start)

