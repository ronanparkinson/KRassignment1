import os
import sys

from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from logic import FolKB, fol_fc_ask, fol_bc_ask, expr
import pandas as pd
import random

from learning import NaiveBayesLearner, DataSet
import networkx as nx
import matplotlib.pyplot as plt

parent_dir = os.path.dirname(os.getcwd())
sys.path.append(parent_dir)

def questionOne():
    kb = FolKB()
    #rules
    kb.tell(expr('(Parent(x,y) & HasblueEyes(x)) ==> InheritsBlueEyes(y)'))
    kb.tell(expr("Parent(x, y) ==> Ancestor(x, y)"))
    kb.tell(expr("(Parent(x, y) & Ancestor(z, x)) ==> Ancestor(z, y)"))
    kb.tell(expr("(Parent(pa, cx) & Parent(pb, cy) & Sibling(pa, pb) & NotEqual(cx, cy)) ==> Cousin(cx, cy)"))

    #facts
    kb.tell(expr("Parent(Alice, Carol)"))
    kb.tell(expr("Parent(Bob, Carol)"))
    kb.tell(expr("Parent(Alice, Dave)"))
    kb.tell(expr("Parent(Bob, Dave)"))
    kb.tell(expr("Spouse(Eve, Dave)"))
    kb.tell(expr('Parent(Carol, Frank)'))
    kb.tell(expr('HasblueEyes(Carol)'))

    def inheritsBE():
        doesInherit = random.random() < 0.5
        if doesInherit:
            kb.tell(expr('InheritsBlueEyes(y) ==> HasblueEyes(y)'))
            gotBlueEyes = fol_fc_ask(kb, expr('HasblueEyes(Frank)'))
            gotBlueEyesBC = fol_bc_ask(kb, expr('HasblueEyes(Frank)'))
            print("fc", list(gotBlueEyes))
            for checkInheritBC in gotBlueEyesBC:
                print("bc", checkInheritBC)
            ##could remove the rule from the kb here to prevent it from happening afterwards unnecessarily

    ##Inference
    inheritsBE()

    haveBlueEyes = fol_fc_ask(kb, expr('HasblueEyes(Frank)')) #[{}] is the correct result as it means no subs were needed
    print('\nDoes Frank have blue eyes?', list(haveBlueEyes))

    gotBlueEyes = fol_bc_ask(kb, expr('HasblueEyes(Frank)'))
    for Beyes in gotBlueEyes:
        print(Beyes)

    def print_clauses(kb, message="", bool_print=True):
        if bool_print:
            for clause in kb.clauses:
                print(clause)
        print("Total Clauses: ", len(kb.clauses))
    print_clauses(kb)

    ancestorWithBE = fol_bc_ask(kb, expr('Ancestor(x, Frank)'))
    for Ancestor in ancestorWithBE:
        checkIfAncestorHasBE = fol_bc_ask(kb, expr('HasblueEyes(x)'))
        for AncWithBEs in checkIfAncestorHasBE:
            if Ancestor == AncWithBEs:
                print("One of Franks ancestors with blue eyes is:", Ancestor)

    areCousins = fol_fc_ask(kb, expr("Cousin(Carol, Eve)"))
    print(("Are Carol and eve cousins?", list(areCousins)))

questionOne()

from probability import BayesNet, enumeration_ask, elimination_ask, rejection_sampling, likelihood_weighting, gibbs_ask

def questionTwo():
    env_tech_impact = BayesNet([
        ('TechInnovation', '', 0.8),  # Prior probability
        ('Urbanisation', '', 0.4),  # Prior probability
        ('JobMarket', 'TechInnovation', {
            (True,): 0.85,
            (False,): 0.3
        }),
        ('CleanEnergyAdoption', 'TechInnovation Urbanisation', {
            (True, True): 0.75,
            (True, False): 0.5,
            (False, True): 0.3,
            (False, False): 0.1
        }),
        ('CarbonEmissions', 'Urbanisation CleanEnergyAdoption', {
            (True, True): 0.4,
            (True, False): 0.55,
            (False, True): 0.7,
            (False, False): 0.95
        }),
        ('EcologicalFootprint', 'CarbonEmissions', {
            (True,): 0.6,
            (False,): 0.45
        }),
    ])

    G = nx.Graph()

    G.add_edges_from([
        ('CleanEnergyAdoption', 'Urbanisation'),
        ('CleanEnergyAdoption', 'CarbonEmissions'),
        ('CleanEnergyAdoption', 'TechInnovation'),
        ('Urbanisation', 'CarbonEmissions'),
        ('EcologicalFootprint', 'CarbonEmissions'),
        ('TechInnovation', 'JobMarket')
    ])

    pos = {

        'Urbanisation': (2, 2),
        'CarbonEmissions': (2, 1),
        'JobMarket': (0, 1),
        'TechInnovation': (0, 2),
        'CleanEnergyAdoption': (1, 1),
        'EcologicalFootprint': (2, 0)
    }

    # Draw the graph
    plt.figure(figsize=(15, 10))
    plt.title("Bayesian Network", fontsize=16)
    nx.draw(G, pos, with_labels=True, node_color='green', node_size=2500,
            font_size=14, font_weight='bold', edge_color='gray')

    plt.show()

    # Query the network
    print("P(EcologicalFootprint=True | TechInnovation=True, CleanEnergyAdoption=True):")
    print(enumeration_ask('EcologicalFootprint', {'TechInnovation': True, 'CleanEnergyAdoption': True},
                          env_tech_impact).show_approx())

    # Query the network
    print("P(EcologicalFootprint=True | TechInnovation=True, CleanEnergyAdoption=True):")
    print(elimination_ask('EcologicalFootprint', {'TechInnovation': True, 'CleanEnergyAdoption': True},
                          env_tech_impact).show_approx())
    # Query the network
    print("P(EcologicalFootprint=True | TechInnovation=True, CleanEnergyAdoption=True):")
    print(rejection_sampling('EcologicalFootprint', {'TechInnovation': True, 'CleanEnergyAdoption': True},
                          env_tech_impact).show_approx())
    # Query the network
    print("P(EcologicalFootprint=True | TechInnovation=True, CleanEnergyAdoption=True):")
    print(likelihood_weighting('EcologicalFootprint', {'TechInnovation': True, 'CleanEnergyAdoption': True},
                          env_tech_impact).show_approx())

    # Query the network
    print("P(EcologicalFootprint=True | TechInnovation=True, CleanEnergyAdoption=True):")
    print(gibbs_ask('EcologicalFootprint', {'TechInnovation': True, 'CleanEnergyAdoption': True},
                          env_tech_impact).show_approx())

    ##
    print("P(CarbonEmissions=True | Urbanisation=True, JobMarket=True):")
    print(enumeration_ask('CarbonEmissions', {'Urbanisation': True, 'JobMarket': True},
                          env_tech_impact).show_approx())

    # Query the network
    print("P(CarbonEmissions=True | Urbanisation=True, JobMarket=True):")
    print(elimination_ask('CarbonEmissions', {'Urbanisation': True, 'JobMarket': True},
                          env_tech_impact).show_approx())
    # Query the network
    print("P(CarbonEmissions=True | Urbanisation=True, JobMarket=True):")
    print(rejection_sampling('CarbonEmissions', {'Urbanisation': True, 'JobMarket': True},
                          env_tech_impact).show_approx())
    # Query the network
    print("P(CarbonEmissions=True | Urbanisation=True, JobMarket=True):")
    print(likelihood_weighting('CarbonEmissions', {'Urbanisation': True, 'JobMarket': True},
                          env_tech_impact).show_approx())

    # Query the network
    print("P(JobMarket=True | Urbanisation=True, JobMarket=True):")
    print(gibbs_ask('CarbonEmissions', {'Urbanisation': True, 'JobMarket': True},
                          env_tech_impact).show_approx())

    ##
    print("P(JobMarket=True | TechInnovation=True, Urbanisation=True):")
    print(enumeration_ask('JobMarket', {'TechInnovation': True, 'Urbanisation': True},
                          env_tech_impact).show_approx())

    # Query the network
    print("P(JobMarket=True | TechInnovation=True, Urbanisation=True):")
    print(elimination_ask('JobMarket', {'TechInnovation': True, 'Urbanisation': True},
                          env_tech_impact).show_approx())
    # Query the network
    print("P(JobMarket=True | TechInnovation=True, Urbanisation=True):")
    print(rejection_sampling('JobMarket', {'TechInnovation': True, 'Urbanisation': True},
                          env_tech_impact).show_approx())
    # Query the network
    print("P(JobMarket=True | TechInnovation=True, Urbanisation=True):")
    print(likelihood_weighting('JobMarket', {'TechInnovation': True, 'Urbanisation': True},
                          env_tech_impact).show_approx())

    # Query the network
    print("P(JobMarket=True | TechInnovation=True, Urbanisation=True):")
    print(gibbs_ask('JobMarket', {'TechInnovation': True, 'Urbanisation': True},
                          env_tech_impact).show_approx())

questionTwo()

def questionThree():
    dataset = pd.read_csv('bank-full.csv', delimiter=';', nrows=2500)

    print("Column names in the dataset:", dataset.columns)

    # Separate features (X) and target (y)
    X = dataset.drop(columns=['y'])  # Drop the target column to get features
    y = dataset['y']  # Extract the target column

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=15)

    # Create DataFrames for easy handling
    feature_columns = dataset.columns[:-1]  # Feature column names
    print("Feature Columns:", X)

    test_df = pd.DataFrame(X_test, columns=feature_columns)
    test_df['y'] = y_test
    test_class_priors = test_df['y'].value_counts(normalize=True)  # Class distribution for testing set

    train_df = pd.DataFrame(X_train, columns=feature_columns)
    train_df['y'] = y_train
    test_class_priors = train_df['y'].value_counts(normalize=True)  # Class distribution for testing set

    print("\nTesting Set Prior Probabilities (P(C)):")
    print(test_class_priors)

    print("\nEstimating Evidence Probabilities:")
    evidence_probabilities = {}
    for column in feature_columns:
        if test_df[column].dtype == 'object':  # Categorical feature
            evidence_probabilities[column] = test_df[column].value_counts(normalize=True)
        else:  # Numerical feature
            evidence_probabilities[column] = test_df[column].describe()

    print("\nEvidence Probabilities (P(E)) for each feature:")
    for feature, prob in evidence_probabilities.items():
        print(f"Feature: {feature}")
        print(prob)
        print()
    dataset['y'] = dataset['y'].map({'yes': 1, 'no': 0})

    # Prepare features (X) and target (y)
    X = dataset.drop('y', axis=1)  # Drop the target column to get features
    y = dataset['y']  # Target column (binary: 1 for 'yes', 0 for 'no')

    # Split the data into two subsets: y = 1 (yes) and y = 0 (no)
    X_class_1 = X[y == 1]
    X_class_0 = X[y == 0]

    # Check the shapes to ensure proper data separation
    print("Class 1 data shape:", X_class_1.shape)
    print("Class 0 data shape:", X_class_0.shape)
    dataset['y'] = dataset['y'].map({'yes': 1, 'no': 0})

    def calculate_likelihood(X_class, feature_column):
        feature_prob = X_class[feature_column].value_counts(normalize=True)
        return feature_prob

    # Calculate likelihood for each feature in both classes (y = 1 and y = 0)
    feature_likelihoods_class_1 = {}
    feature_likelihoods_class_0 = {}

    # Iterate over each feature column in the dataset
    for feature in X.columns:
        feature_likelihoods_class_1[feature] = calculate_likelihood(X_class_1, feature)
        feature_likelihoods_class_0[feature] = calculate_likelihood(X_class_0, feature)


    test_data = X.iloc[0]  # Let's take the first observation in the dataset

    # Initialize likelihoods for each class (y = 1 and y = 0)
    likelihood_class_1 = 1
    likelihood_class_0 = 1

    # Calculate the likelihood for each class by multiplying the probabilities of each feature
    for feature in X.columns:
        feature_value = test_data[feature]  # Get the feature value for the test data sample

        # Multiply the likelihoods for each class (handle missing feature values gracefully)
        likelihood_class_1 *= feature_likelihoods_class_1[feature].get(feature_value,
                                                                       0)  # Default to 0 if feature value not seen
        likelihood_class_0 *= feature_likelihoods_class_0[feature].get(feature_value,
                                                                       0)  # Default to 0 if feature value not seen

    print("\nLikelihood for class y=1 (yes):", likelihood_class_1)
    print("Likelihood for class y=0 (no):", likelihood_class_0)

    ##Second dataset
    dataset = pd.read_csv('diabetes_data_upload.csv')

    print("Column names in the dataset:", dataset.columns)

    # Separate features (X) and target (y)
    X = dataset.drop(columns=['class'])  # Drop the target column to get features
    y = dataset['class']  # Extract the target column

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=15)

    # Create DataFrames for easy handling
    feature_columns = dataset.columns[:-1]  # Feature column names
    print("Feature Columns:", X)

    test_df = pd.DataFrame(X_test, columns=feature_columns)
    test_df['class'] = y_test
    test_class_priors = test_df['class'].value_counts(normalize=True)  # Class distribution for testing set

    train_df = pd.DataFrame(X_train, columns=feature_columns)
    train_df['class'] = y_train
    test_class_priors = train_df['class'].value_counts(normalize=True)  # Class distribution for testing set

    print("\nTesting Set Prior Probabilities (P(C)):")
    print(test_class_priors)

    print("\nEstimating Evidence Probabilities:")
    evidence_probabilities = {}
    for column in feature_columns:
        if test_df[column].dtype == 'object':  # Categorical feature
            evidence_probabilities[column] = test_df[column].value_counts(normalize=True)
        else:  # Numerical feature
            evidence_probabilities[column] = test_df[column].describe()

    print("\nEvidence Probabilities (P(E)) for each feature:")
    for feature, prob in evidence_probabilities.items():
        print(f"Feature: {feature}")
        print(prob)
        print()
    dataset['class'] = dataset['class'].map({'Positive': 1, 'Negative': 0})

    # Prepare features (X) and target (y)
    X = dataset.drop('class', axis=1)  # Drop the target column to get features
    y = dataset['class']  # Target column (binary: 1 for 'yes', 0 for 'no')

    # Split the data into two subsets: y = 1 (yes) and y = 0 (no)
    X_class_1 = X[y == 1]
    X_class_0 = X[y == 0]

    # Check the shapes to ensure proper data separation
    print("Class 1 data shape:", X_class_1.shape)
    print("Class 0 data shape:", X_class_0.shape)
    dataset['class'] = dataset['class'].map({'Positive': 1, 'Negative': 0})

    def calculate_likelihood_two(X_class, feature_column):
        feature_prob = X_class[feature_column].value_counts(normalize=True)
        return feature_prob

    # Calculate likelihood for each feature in both classes (y = 1 and y = 0)
    feature_likelihoods_class_1 = {}
    feature_likelihoods_class_0 = {}

    # Iterate over each feature column in the dataset
    for feature in X.columns:
        feature_likelihoods_class_1[feature] = calculate_likelihood_two(X_class_1, feature)
        feature_likelihoods_class_0[feature] = calculate_likelihood_two(X_class_0, feature)

    test_data = X.iloc[0]  # Let's take the first observation in the dataset

    # Initialize likelihoods for each class (y = 1 and y = 0)
    likelihood_class_1 = 1
    likelihood_class_0 = 1

    # Calculate the likelihood for each class by multiplying the probabilities of each feature
    for feature in X.columns:
        feature_value = test_data[feature]  # Get the feature value for the test data sample

        # Multiply the likelihoods for each class (handle missing feature values gracefully)
        likelihood_class_1 *= feature_likelihoods_class_1[feature].get(feature_value,
                                                                       0)  # Default to 0 if feature value not seen
        likelihood_class_0 *= feature_likelihoods_class_0[feature].get(feature_value,
                                                                       0)  # Default to 0 if feature value not seen

    print("\nLikelihood for class y=1 (yes):", likelihood_class_1)
    print("Likelihood for class y=0 (no):", likelihood_class_0)

#1.3.2 NAIVE BAYES CLASSIFICATION

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

    train_data = [list(row) for row in train_df.values]
    test_data = [list(row) for row in test_df.values]

    # Filter rows with the correct number of features (4 features + 1 target)
    expected_length = 5
    train_data = [row for row in train_data if len(row) == expected_length]
    test_data = [row for row in test_data if len(row) == expected_length]

    # Print number of valid training and testing examples
    print(f"Filtered training examples: {len(train_data)}")
    print(f"Filtered testing examples: {len(test_data)}")

    # Instantiate Naive Bayes Learner using the AIMA library
    # nb_learner = NaiveBayesLearner(DataSet(examples=train_data, target=-1))
    #
    # # Predict class for test examples
    # predictions = [nb_learner(row[:-1]) for row in test_data]
    # actuals = [row[-1] for row in test_data]  # Actual class labels
    #
    # # Calculate evaluation metrics (accuracy, precision, recall, etc.)
    # print("\nEvaluation Metrics\n")
    # accuracy = accuracy_score(actuals, predictions)  # Accuracy of the model
    # report = classification_report(actuals, predictions, target_names='y')  # Detailed metrics
    # print(f"Accuracy: {accuracy}")
    # print("Classification Report:\n", report)
questionThree()