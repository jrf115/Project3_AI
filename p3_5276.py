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
    arff = {}
    for line in arff_file:
        if line[0] != '%':  # These are comments in the file
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
                    attribute_list = ...
                    arff[attribute] = ...
                    print(arff[line[11:i]])
                elif line.find("@DATA") == 0 or 0 == line.find("@data"):
                    print("Found @DATA!")

    arff_file.close()
    print("Classifier created: ", arff ," . Please enter a name of the file that you want to save your classifier into: ")
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
