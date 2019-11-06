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
    arff = {}  # Will be a dictionary identified by its key "relation", and holds dicts of attribute values, which are accessed by the attribute's name
    total_data_points = 0
    read_data = False
    value_and_class = False
    # The two "sets" vars below are used to help iterate through the arff dictionary for finding P(x | p /or/ n)
    attribute_values_set = set(())
    attribute_dict = {}
    _class_set = set(())
    for line in arff_file:
        if line[0] != '%':  # These are comments in the file
            if not read_data:
                if line[0] == '@':
                    if line.find("@RELATION") == 0 or 0 == line.find("@relation"):
                        print("Found @RELATION")
                        arff["relation"] = line[10:-1]  # Slice so that only the relation name is saved
                        print(arff["relation"])

                    elif line.find("@ATTRIBUTE") == 0 or 0 == line.find("@attribute"):
                        print("Found @ATTRIBUTE!")
                        i = 11
                        while line[i] != " ":
                            i = i + 1
                        attribute = line[11:i]
                        print("Attribute is:", attribute)
                        attribute_dict[attribute] = set(())

                        # Cleaning up the attribute's values eventually into a list
                        temp_list_string = line[i:-1]
                        temp_list_string = temp_list_string.replace('{', "")
                        temp_list_string = temp_list_string.replace(',', " ")
                        temp_list_string = temp_list_string.replace('}', "")
                        temp_list_string = temp_list_string.strip()
                        " ".join(temp_list_string.split())  # Removes duplicated spaces
                        temp_list = temp_list_string.split()  # Puts each value into a list
                        # Initialize each individual attribute value of this list into a dictionary.

                        for v in temp_list:
                            arff[v] = 0 # Will be a dictionary, where one function it has, is that defines how many times a value occurs in data set. Key is that attribute's value, and definition is 0 by default.
                            attribute_dict[attribute].add(v)

                        # The last time these 2 lines is run it should capture the class attributes
                        _class = attribute
                        _class_set = attribute_dict[_class]

                        print("Printing attribute", attribute, "contents:", attribute_dict[attribute])

                    elif line.find("@DATA") == 0 or 0 == line.find("@data"):
                        print("Found @DATA!")
                        read_data = True

            else:  # Read data
                # After the attributes are read, we need to add create new entries for X and p/n.
                # This 'if' block only needs run once
                if not(value_and_class):
                    # create new entrys for X and p/n
                    # This is attribute value AND class
                    for c in _class_set:
                        for a in attribute_dict:
                            for v in attribute_dict[a]:
                                if not (v in _class_set): # We don't want a class and class entry
                                    arff[(v + '&' + c)] = 0
                    value_and_class = True

                # From reading the data, we need to find P(p), P(n), P(xi | p) and P(xi | n)
                # So we will add a number for each P(xi | p) and P(xi | n) we find
                temp_list_string2 = line
                temp_list_string2 = temp_list_string2.replace(',', " ")
                " ".join(temp_list_string2.split())  # Removes duplicated spaces
                temp_list2 = temp_list_string2.split()  # Puts each value into a list
                temp_list2.reverse()  # Makes things easier to find  P(value | p /or/ n)
                for i in temp_list2:
                    f = 0
                    if i == temp_list2[0]:
                        _class = i
                        if not (_class in _class_set):
                            _class_set.add(_class)

                    else:
                        if not (i in attribute_values_set):
                            attribute_values_set.add(i)

                        if (i + '&' + _class) in arff:
                            arff[(i + '&' + _class)] += 1

                        else:
                            print("ERROR!!!: Missing entry for X and p/n! This is attribute value AND class!")
                            exit(1)

                    if i in arff:
                        arff[i] = arff[i] + 1

                    else:  # Create a new entry for attribute value
                        arff[i] = 1
                total_data_points = total_data_points + 1
    arff_file.close()

    if not "overcast&no" in arff:
        print("MISSING overcast&no")

    print("Data read in. Total of", total_data_points,". Arff file closed.")
    print("Set of attribute values created:", attribute_values_set)
    print("Set of class values created:", _class_set)
    print("File contents read and organized: ", arff)

    print("\n\nPlease enter a name of the file that you want to save your classifier into: ")
    filename = input()

    # Bin Format:
    """                                                                 Tennis example
    P(p),someNumber                                                     no,5/14
    P(n),someNumber                                                     yes,9/14
    .
    .
    .... to how many class 'n" values the arff file has                     # 'yes' is the last class for Tennis example
    P(X1|n),someNumber                                                  sunny&no,3/5
    P(X2|n),someNumber                                                  overcast&no,0
    .                                                                   .
    .                                                                   .   
    .... to the very last generic attribute value                       strong&no,2/5
    P(X1|p),someNumber                                                  sunny&yes,2/9
    P(X2|p),someNumber                                                  overcast&yes,4/9
    .                                                                   .
    .                                                                   .
    .... to the very last generic attribute value                       sunny&yes,6/9
    ........ to how many class "n/p/.." values there are.                   # 'yes' is the last class for Tennis example
    """
    print("Now calculating Naive_Bayesian_Classifier...")
    file = open(filename + ".bin", "x")
    for c in _class_set:
        bin_content = bin_content + c + ',' + str(arff[c] / total_data_points) + '\n'

    for c in _class_set:
        print('class', c)
        for a in attribute_dict:
            print('attribute', a)
            for v in attribute_dict[a]:
                relative_freq = str(v + '&' + c)
                print('attr_value:', v,'and',c)
                if relative_freq in arff:  # If the P(Xi | C) is in this dict...
                    p = str(arff[relative_freq] / arff[c]) # Function P(Xi|C)
                    bin_content = bin_content + (relative_freq + ',') + p + '\n'
                    print((a + '&' + c + ',') + p)
    print("bin_content is ", bin_content)
    file.write(bin_content)
    print("Naive_Bayesian_Classifier written to ", filename, ".bin", sep="")
    file.close()

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
