from fitz import fitz as f


def sorted_lines(filename):  # returns sorted text lines
    lines = []  # the result
    doc = f.open(filename)
    for page in doc:
        page_lines = []  # lines on this page
        all_text = page.get_text("dict", flags=f.TEXTFLAGS_TEXT)
        for block in all_text["blocks"]:
            for line in block["lines"]:
                text = "".join([span["text"] for span in line["spans"]])
                bbox = f.Rect(line["bbox"])  # the wrapping rectangle
                # append line text and its top-left coord
                page_lines.append((bbox.y0, bbox.x0, text))
        # sort the page lines by vertical, then by horizontal coord
        page_lines.sort(key=lambda l: (l[0], l[1]))
        lines.append(page_lines)  # append to lines of the document
    return lines


def find_differences(f1_lines, f2_lines):
    differences = []

    # Ensure both files have the same number of pages
    # if len(f1_lines) != len(f2_lines):
    #     differences.append("The number of pages differ.")
    #     return differences

    for i, (page1_lines, page2_lines) in enumerate(zip(f1_lines, f2_lines)):
        # Ensure both pages have the same number of lines
        # if len(page1_lines) != len(page2_lines):
        #     differences.append(f"Page {i + 1}: Number of lines differ.")
        #     continue

        for j, (line1, line2) in enumerate(zip(page1_lines, page2_lines)):
            y1, x1, text1 = line1
            y2, x2, text2 = line2

            if text1 != text2:
                differences.append(f"Page {i + 1}, Line {j + 1}: Text differs. File1: '{text1}', File2: '{text2}'")
            elif y1 != y2 or x1 != x2:
                differences.append(
                    f"Page {i + 1}, Line {j + 1}: Position differs. File1: (y={y1}, x={x1}), File2: (y={y2}, x={x2})")

    return differences


f1 = sorted_lines("files/Appendix_1_Global_English_20231205.pdf")
f2 = sorted_lines('files/Appendix_1_Global_English_20231205.pdf')
differences = find_differences(f1, f2)

print(differences)
