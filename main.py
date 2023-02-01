import numpy as np
import pandas as pd
import json
from sklearn.cluster import Birch
from sklearn.preprocessing import LabelEncoder

#NumPy is a library for the Python programming language that provides support for arrays and matrices, enabling efficient numerical computation and manipulation.
#Pandas is a library for the Python programming language that provides fast, flexible, and expressive data structures designed to make working with structured data as easy as possible.
#JSON (JavaScript Object Notation) is a lightweight data interchange format that is easy for humans to read and write, and easy for machines to parse and generate.
#Birch (Balanced Iterative Reducing and Clustering Using Hierarchies) is an unsupervised machine learning algorithm that is used for hierarchical clustering. 
#LabelEncoder is a utility class from the scikit-learn library that is used to encode categorical variables as numerical values.

# Read the CSV file into a DataFrame
transactions = pd.read_csv('orders.csv')

# Preprocess the "Product_Name" and "Brand" columns
le = LabelEncoder()
lp = LabelEncoder()

transactions["Product_Name"] = lp.fit_transform(transactions["Product_Name"])
transactions["Brand"] = le.fit_transform(transactions["Brand"])

# Select the "Price", "Quantity", "Product_Name", and "Brand" columns of the DataFrame
X = transactions[["Price", "Quantity", "Product_Name", "Brand"]].values

# Fit a Birch model to the data
brc = Birch(threshold=0.5, branching_factor=50, n_clusters=5, compute_labels=True)
labels = brc.fit_predict(X)

# Create a dictionary to store the segments
segments = {}

# Loop through each unique label
for label in np.unique(labels):
    # Extract the indices of the rows assigned to this label
    indices = np.where(labels == label)[0]

    # Get the count of each unique product and brand for the rows assigned to this label
    unique_product_name, unique_product_name_counts = np.unique(transactions.loc[indices, "Product_Name"], return_counts=True)
    unique_brand, unique_brand_counts = np.unique(transactions.loc[indices, "Brand"], return_counts=True)

    # Select the product and brand that appear most frequently for the rows assigned to this label
    max_product_name_index = np.argmax(unique_product_name_counts)
    max_brand_index = np.argmax(unique_brand_counts)
    max_product_name = unique_product_name[max_product_name_index]
    max_brand = unique_brand[max_brand_index]

    # Get the string representation of the product and brand values
    max_product_name = lp.inverse_transform([int(max_product_name)])[0]
    max_brand = le.inverse_transform([int(max_brand)])[0]

    # Generate the segment name
    segment_name = f"{max_product_name}_{max_brand}"

    # Extract the Customer_ID values for the rows assigned to this label
    customer_ids = transactions.loc[indices, "Customer_ID"].tolist()

    # Add a key-value pair to the segments dictionary, where the key is the segment name and the value is a list of customer IDs
    segments[segment_name] = customer_ids

# Save the segments dictionary as a JSON file
with open("segments.json", "w") as f:
    json.dump(segments, f)