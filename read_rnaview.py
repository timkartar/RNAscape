from config import *
import sys
import re


def readRnaview(filepath):
    base_pair_list= []

    with open(filepath, 'r') as out_file:
        lines = out_file.readlines()

    in_base_pair = False
    for line in lines:
        if line.startswith("BEGIN_base-pair"):
            print(line)
            in_base_pair = True
            continue
        if line.startswith("END_base-pair"):
            print(line)
            in_base_pair = False
            break
        # Logic to add to dict
        if in_base_pair:
            line_dict = {}
            line = re.sub(r'\s+', ' ', line).strip() # parse spaces
            line_split = line.split(" ")

            # Column 1: RNAView base numbers
            rnaview_base_nums = [int(element.split(",")[0].strip()) for element in line_split[0].split("_")]
            line_dict["col1"] = rnaview_base_nums

            #Column 2: CHAIN ID
            chain = line_split[1].split(":")[0].strip()
            line_dict["ch_id"] = chain

            #Column 3: Residue Number
            residue_num = int(line_split[2])
            line_dict["res_id"] = residue_num

            #Column 4: Base Pairs
            base_pairs = [element for element in line_split[3].split("-")]
            line_dict["col4"] = base_pairs

            #Column 5: Residue Number
            line_dict["res_id2"] = line_split[4]

            #Column 6: Chain ID
            chain_2 = line_split[5].split(":")[0].strip()
            line_dict["ch_id2"] = chain_2

            #Column 7: BP Annotation
            line_dict["bp_type"] = line_split[6]

            #Column 8:
            line_dict["orient"] = line_split[7]

            final_line_split = 8

            if line_split[8] == "syn" or line_split[8] == "stack":
                line_dict[line_split[8]] = line_split[8]
                final_line_split += 1
                if line_split[9] == "syn" or line_split[9] == "stack":
                    line_dict[line_split[9]] = line_split[9]
                    final_line_split += 1

            line_dict["col9"] = line_split[final_line_split]
            base_pair_list.append(line_dict)
    return base_pair_list


# print(base_pair_list)
