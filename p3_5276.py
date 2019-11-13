############################
#   John Fahringer         #
#   AI & Heuristics Analyis#
#   Project 3              #
############################

import os.path  # File operations


# P(C|X) = P(X|C) * P(C)  /  P(X) (which are params below)
def Bayes_Thm(XandC, rel_freq, const):
    return (XandC * rel_freq) / const


def read_ARFF(trainingEx):
    while not os.path.exists(trainingEx):
        print("Error: arff file could not be opened. Try again!")
        trainingEx = input()

    arff_file = open(trainingEx, "r")
    arff = {}  # Will be a dictionary identified by its key "relation", and holds dicts of attribute values, which are accessed by the attribute's name
    _class = ""
    data_points = []
    total_data_points = 0
    read_data = False
    value_and_class = False
    # The two "sets" vars below are used to help iterate through the arff dictionary for finding P(x | p /or/ n)
    _class_set = set(())
    attribute_values_set = set(())
    attribute_dict = {}
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
                            i += 1
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
                if not value_and_class:
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
                data_points.append(line[:-1])
                temp_list_string2 = line
                temp_list_string2 = temp_list_string2.replace(',', " ")
                " ".join(temp_list_string2.split())  # Removes duplicated spaces
                temp_list2 = temp_list_string2.split()  # Puts each value into a list
                temp_list2.reverse()  # Makes things easier to find  P(value | p /or/ n)
                for i in temp_list2:
                    if i == temp_list2[0]:
                        _class = i
                        if not (_class in _class_set):
                            print("ERROR!!!: Missing entry for class member: " + _class + "!")
                            #exit(1)

                    else:
                        if not (i in attribute_values_set):
                            attribute_values_set.add(i) # Subject to be removed.

                        if (i + '&' + _class) in arff:
                            arff[(i + '&' + _class)] += 1

                        else:
                            print("ERROR!!!: Missing entry for " + i + " and " + _class + "! This is attribute value AND class!")
                            #exit(1)

                    if i in arff:
                        arff[i] += 1

                    else:  # Create a new entry for attribute value
                        print("ERROR: Missing attribute value" + i +"!")
                        # exit(1)
                total_data_points = total_data_points + 1
    arff_file.close()

    print("Data points:", data_points)
    print("Data read in. Total of", total_data_points,". Arff file closed.")
    print("Set of attribute values created:", attribute_values_set)
    print("Set of class values created:", _class_set)
    print("File contents read and organized: ", arff)
    return total_data_points, data_points,_class_set, attribute_values_set, attribute_dict, arff


def generate_bayesian_Classifier():
    print("Enter the filename of input data consisting of attributes and training examples in ARFF (Weka) format. (You might use the existing arffs in the data folder)")
    trainingEx = input()
    total_data_points, data_points, _class_set, attribute_values_set, attribute_dict, arff = read_ARFF(trainingEx)

    print("\n\n")

    # Bin Format:
    """                                                                 Tennis example
    P(p),someNumber                                                     no,5/14
    P(n),someNumber                                                     yes,9/14
    .
    .
    .... to how many class 'n" values the arff file has                     # 'yes' is the last class for Tennis example
    P(X1|n),someNumber                                                  sunny&no,3/5
    P(X2|n),someNumber                                                  overcast&no,0
    # P(C|X) = P(X|C) * P(C)  /  P(X) #                                .
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
    filename = trainingEx[:-5]
    file = open(filename + ".bin", "x")
    bin_content = arff["relation"] + '\n'
    for c in _class_set:
        bin_content += c + ',' + str(arff[c] / total_data_points) + '\n'

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
    while not os.path.exists(model_file) or model_file[-4:] != ".bin":
        print("Either the file doesn't exist, or the file is not in bin format")
        model_file = input()
    print("Now enter a testing data file in ARFF format:")
    testing_file = input()
    while not os.path.exists(testing_file):
        print("Can't find the file, try again.")
        testing_file = input()
    bin_file = open(model_file, 'r')
    relation = ""
    classes = dict()
    a_posteris = dict()
    line_number = 1

    # Reading in Classifier
    for line in bin_file:
        if line_number == 1:
            relation = line[:-1]

        else:
            apost_index = line.find(',')
            # print("apost_index", apost_index)
            if line.find('&') == -1:
                class_str = line[:apost_index]
                chance_str = line[apost_index + 1:-1]
                classes[class_str] = float(chance_str)
                print("Class:", class_str, "line", chance_str)
            else:
                a_post_str = line[:apost_index]
                chance_str = line[apost_index + 1:]
                a_posteris[a_post_str] = float(chance_str)
        line_number += 1

    bin_file.close()

    # Reading in sample testing arffFile
    total_data_points, data_points, _class_set, attribute_values_set, attribute_dict, arff = read_ARFF(testing_file)

    if arff["relation"] != relation:
        raise Exception("Relations between classifier and data test file are not the same:", relation, "and", line[-1:])
        return


    # Formulating and Printing Confusion Matrix
    ''' Finding total for each "actual class" count (What you see in the right most column)'''
    print('\n\nNow formulating Confusion Matrix...\n')
    matrix_actual_class_totals = dict()
    for c in _class_set:
        print("Class", c, arff[c])
        matrix_actual_class_totals[c] = arff[c]
    print()
    ''' Finding total for each "Predicted class" count (what you se in the bottom most column)'''
    # Initialize prediction totals
    matrix_predict_class_totals = dict()
    for c in _class_set:
        matrix_predict_class_totals[c] = 0

    # Initialize main table "body"
    matrix_main = dict()
    for actual_c in _class_set:
        row = "actual:" + actual_c
        for predict_c in _class_set:
            column = "predicted:" + predict_c
            matrix_main[row + ',' + column] = 0

    # To find the prediction, you must compare the sample data point,ignoring its class, with all class posteri combinations.
    # THe class posteri combination that has the highest percentage is the prediction for the set. (Look at pp slide 38)
    for d in data_points:
        temp_string = d.replace(',', ' ')
        points_attributes_list = temp_string.split()
        print("Finding prediction of datapoint:", d)
        classify_dict = {}
        for c in _class_set:
            classify = 1
            for p_a in points_attributes_list:
                if p_a != points_attributes_list[-1]:
                        if (p_a + '&' + c) in a_posteris:
                            classify *= a_posteris[p_a + '&' + c]
                        else:
                            print("ERROR: an a_posteris could not be found:", p_a + '&' + c)
            classify *= classes[c] # Grab the probability of the current class and multiply it to P(X|p)
            classify_dict[c] = classify # We are comparing which class probability "version" is higher.

        # Compare the class probabilities
        classifier = int()
        predicted = str()
        for c in classify_dict:
            if classify_dict[c] >= classifier:
                classifier = classify_dict[c]
                predicted = c

        matrix_predict_class_totals[predicted] += 1

        row = "actual:" + points_attributes_list[-1]
        column = "predicted:" + predicted
        matrix_main[row + ',' + column] += 1

        print("Classify_Dict for datapoint:", classify_dict)
        print("Resulting Prediciton: ", predicted)

    ###################################################################
    # Printing Confusion Matrix
    print("\n\nPrinting Confusion Matrix of:", testing_file, "\n===================================================")

    print("n = ", total_data_points, "\t\t\t\t", sep = '', end='')
    # The column headers
    for predicted in _class_set:
        print("Predicted:", predicted, "\t\t\t\t", sep = '',end='')
    print()
    for actual in _class_set:
        print("Actual:", actual, "\t\t\t\t\t", sep = '', end='')
        row = "actual:" + actual
        for predicts in _class_set:
            column = "predicted:" + predicts
            print(matrix_main[row + ',' + column], "\t\t\t\t\t", sep = '', end='')
        print(matrix_actual_class_totals[actual])
        print()
    print("\t\t\t\t\t\t\t", sep = '', end = '')
    for predicts in _class_set:
        print(matrix_predict_class_totals[predicts], "\t\t\t\t\t", sep = '', end='')
    print("\n\n")


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
    while True:
        menu_1()


def main():
    py_nb()


main()
