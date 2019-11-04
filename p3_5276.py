############################
#   John Fahringer         #
#   AI & Heuristics Analyis#
#   Project 3              #
############################

import os.path  # File operations

# P(C|X) = P(X|C) * P(C)  /  P(X) (which are params below)
def Bayes_Thm(XandC, rel_freq, const):
    return (XandC * rel_freq) / const

def generate_bayesian_Classifier():
    print("Enter the filename of input data consisting of attributes and training examples in ARFF (Weka) format")
    trainingEx = input()
    if os.path.exists("data/" + trainingEx) == False:
        print("Error: arff file could not be opened. Exiting...")
        exit()
    arff_file = open("data/" + trainingEx, "r")
    bin_content = ""
    class_Index = ""
    arff = {} # Will be a dictionary identified by its key "relation", and holds dicts of attribute values, which are accessed by the attribute's name
    total_data_points = 0
    read_data = False
    for line in arff_file:
        if line[0] != '%':  # These are comments in the file
            if read_data == False:
                if line[0] == '@':
                    if line.find("@RELATION") == 0 or 0 == line.find("@relation"):
                        print("Found @RELATION")
                        arff["relation"] = line[10:-1] # Slice so that only the relation name is saved
                        print(arff["relation"])

                    elif line.find("@ATTRIBUTE") == 0 or 0  == line.find("@attribute"):
                        print("Found @ATTRIBUTE!")
                        i = 11
                        while line[i] != " ":
                            i = i + 1
                        attribute = line[11:i]
                        class_Index = attribute # The class in an arff file is the last attribute. This var will catch this class the last time this elif is run
                        print("Attribute is:", attribute)
                        # Cleaning up the attribute's values
                        temp_list_string = line[i:-1]
                        print("Line of attribute's values read in is:", temp_list_string)
                        temp_list_string = temp_list_string.replace('{', "")
                        temp_list_string = temp_list_string.replace(',', " ")
                        temp_list_string = temp_list_string.replace('}', "")
                        temp_list_string = temp_list_string.strip()
                        " ".join(temp_list_string.split()) # Removes duplicated spaces
                        temp_list = temp_list_string.split() # Puts each value into a list
                        # Initialize each individual attribute value of this list into a dictionary.
                        f = 0
                        value_dict = {}  # Will be a dictionary that defines how many times a value occurs in data set. Key is that attribute's value, and definition is 0 by default.
                        for f in temp_list:
                            print("Printing temp_list[f]", f)
                            arff[f] = 0

                    elif line.find("@DATA") == 0 or 0 == line.find("@data"):
                        print("Found @DATA!")
                        read_data = True

            else: # Read data
                # From reading the data, we need to find P(p), P(n), P(xi | p) and P(xi | n)
                temp_list_string2 = line
                temp_list_string2 = temp_list_string2.replace(',', " ")
                " ".join(temp_list_string2.split())  # Removes duplicated spaces
                temp_list2 = temp_list_string2.split()  # Puts each value into a list
                print("templist:", temp_list2)
                temp_list2 = reversed(temp_list2) # Makes things easier to find  P(value | p /or/ n)
                for i in temp_list2:
                    if i == temp_list2[0]
                    arff[i] = arff[i] + 1
                total_data_points = total_data_points + 1



    arff_file.close()
    print("File contents read and organized: ", arff)
    # bin_content = Bayes_Thm()
    print("Classifier created: ", bin_content)
    print(" . Please enter a name of the file that you want to save your classifier into: ")
    filename = input()
    file = open(filename + ".bin", "x")
    file.write(bin_content)





def test_bayesian_Classifier():
    print("Enter a model file saved previously")
    model_file = input()


def apply_bayesian_Classifier():
    print("Enter values of condition attributes... ")


# This is the top menu of the program
def menu_1():
    print("1. Learn a Naive Bayesian classifierfrom data")
    print("2. Load and test accuracy of a naive Bayesian classifier.")
    print("3. Apply a naive Bayesian classifierto new cases.")
    print("4. Quit")
    selection = input()
    while selection != '1' and selection != '2' and selection != '3' and selection != '4':
        print("Please enter 1 2 or 3 only")
        selection = input()

    if selection == '1':
       generate_bayesian_Classifier()

    elif selection == '2':
        test_bayesian_Classifier()

    elif selection == '3':
        apply_bayesian_Classifier()

    else:
        exit()


# We are required to use py_nb() as the function to execute our program
def py_nb():
    menu_1()


def main():
    py_nb()


main()
