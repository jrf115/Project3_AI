############################
#   John Fahringer         #
#   AI & Heuristics Analyis#
#   Project 3              #
############################


def py_nb():
    print("1. Learn a Naive Bayesian classifierfrom data")
    print("2. Load and test accuracy of a naive Bayesian classifier.")
    print("3. Apply a naive Bayesian classifierto new cases.")
    print("4. Quit")
    selection = input()
    while (selection == '1' or selection == '2' or selection == '3' or selection == '4') is false:
        print("Please enter 1 2 or 3 only")
        selection = input()
    if selection == 1:
        print("Enter the filename of input data consisting of attributes and training examples in ARFF (Weka) format")

    elif selection == 2:
        print("Enter a model file saved previously")
        modelFile = input()

    elif selection == 3:
        print()

    else:
        exit()


def main():
    py_nb()


main()
