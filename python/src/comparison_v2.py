import timeit
import hashlib

class compare_obj:
    def __init__(self):
        return None

    def _compare(self, list_string1: [str], list_string2: [str]) -> [(int, str)]:
        linesA = list_string1
        linesB = list_string2
        diff_list = []
        same_ID = -1

        #Check every line, if match found change to arbitrary value. This is so duplicate lines get detected.
        for i,line_a in enumerate(linesA):
                for j,line_b in enumerate(linesB):
                    if (line_a == line_b):
                        linesA[i] = same_ID
                        linesB[j] = same_ID
                        break

        #check line for arbitrary value, dont include those lines because they had matches
        for i,line in enumerate(linesA):
            if line!=same_ID:
                diff_list.append((i, line))

        return diff_list



    def compare_file(self, file1: str, file2: str) -> [(int,str)]:
        with open(file1, 'r') as fileA, open(file2, 'r') as fileB:
            linesA = fileA.readlines()
            linesB = fileB.readlines()
            diff_list = self._compare(linesA, linesB)

        return diff_list


    def compare_save_to_file(self, file1: str, file2: str, outputname: str):
        outputlist = self.compare_file(file1, file2)

        with open(outputname, 'w') as outputFile:
            for line in outputlist:
                outputFile.write(line)


    def compare_file_verbose(self, file1: str, file2: str):
            start = timeit.default_timer()

            diff_list = self.compare_file(file1, file2)
            print("Differences detected: ")
            # could use repr here so newlines get printed as '\n' and dont get printed as newline
            for item in diff_list:
                print("Line: ",item[0],"| Change: ", item[1])
            stop = timeit.default_timer()

            print('Comparison time: ', stop - start)
            return diff_list

    def compare_strings(self, string1:str, string2:str) -> [(int, str)]:
        linesA = string1.split("\n")
        linesB = string2.split("\n")
        diff_list = self._compare(linesA, linesB)
        return diff_list

    def compare_bytes(self, text1: bytes, text2: bytes) -> [(int, str)]:
        string1 = text1.decode("utf-8")
        string2 = text2.decode("utf-8")
        return self.compare_strings(string1,string2)

    ### CHECKSUM FUNCTIONS ###

    def checksum (self, file_name: str) -> str:
        with open(file_name, 'rb') as file_obj:
            file_contents = file_obj.read()
            md5_hash = hashlib.md5(file_contents).hexdigest()
            return md5_hash

    def checksum_compare (self, file_name_1: str, file_name_2: str) -> bool:
        return (self.checksum(file_name_1) == self.checksum(file_name_2))

    def checksum_bytes (self, text: bytes):
        return hashlib.md5(text).hexdigest()

    def checksum_compare_bytes(self, content1: bytes, content2: bytes) -> bool:
        return self.checksum_bytes(content1) == self.checksum_bytes(content2)

    def checksum_compare_bytes_checksum(self, content: bytes, checksm: str) -> bool:
        return self.checksum_bytes(content) == checksm

    ##EVERYTHING BEYOND THIS POINT IS DEPRECATED but dont delete it

    def compare_file_old(self, file1: str, file2: str) -> [str] :
        print("Old Compare file being run")
        with open(file1, 'r') as fileA, open(file2, 'r') as fileB:
            linesA = fileA.readlines()
            linesB = fileB.readlines()

            diff_list = [line_a for line_a in linesA if line_a not in linesB]
            return diff_list

    def compare_old_file_verbose(self, file1: str, file2: str):
            start = timeit.default_timer()

            diff_list = self.compare_file_old(file1, file2)

            print("Differences detected: ")
            # could use repr here so newlines get printed as '\n' and dont get printed as newline
            for item in diff_list:
                print("Change: ", item)

            stop = timeit.default_timer()
            print('Comparison time: ', stop - start)

            return diff_list
