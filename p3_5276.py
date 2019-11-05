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
    _class = ""
    arff = {} # Will be a dictionary identified by its key "relation", and holds dicts of attribute values, which are accessed by the attribute's name
    total_data_points = 0
    read_data = False
    # The two "sets" vars below are used to help iterate through the arff dictionary for finding P(x | p /or/ n)
    attribute_values_set = set(())
    _class_set = set(())
    naive_assumption = 0
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
                temp_list2.reverse() # Makes things easier to find  P(value | p /or/ n)
                for i in temp_list2:
                    if i == temp_list2[0]:
                        _class = i
                        if (_class in _class_set) == False:
                            _class_set.add(_class)

                    else:
                        if (i in attribute_values_set) == False:
                            attribute_values_set.add(i)
                        if (i + '&' + _class) in arff:
                            arff[(i + '&' + _class)] += 1

                        else: # create new entry for X and p/n
                            # This is attribute value AND class
                            arff[(i + '&' + _class)] = 1

                    if i in arff:
                        arff[i] = arff[i] + 1

                    else: # Create a new entry for attribute value
                        arff[i] = 1
                total_data_points = total_data_points + 1
    arff_file.close()
    print("Set of attribute values created:", attribute_values_set)
    print("Set of class values created:", _class_set)
    print("File contents read and organized: ", arff)

    print("Now calculating Naive_Bayesian_Thm...")

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
