# Duplication Detection

Data: [`training_ground_truth.csv`](https://drive.google.com/file/d/0BzIp01PoYYptdzNmQmp5WGU1WjQ/view?usp=sharing), [`training_data.csv`](https://drive.google.com/file/d/0BzIp01PoYYptSXQ1UUxGNXhNUzg/view?usp=sharing)

Platform: Python 2.7

## Abstract

As health care systems evolve through mergers, acquisitions, and partnerships, there is a large problem identifying and recognizing duplicate and erroneous information on entities such as doctors, practices, and clinics when the data from various sources is combined. As the number and frequency of these mergers increases, there is a growing need to establish a single "source of truth," using data from key business domains. In this project, the key business domains are `Name`, `Address` and `Taxonomies`. In a short, this project aim to reconcile inconsistencies and eliminate redundancies of a given dataset with proficiency and accuracy.

## Preprocessing

The main goal of this question is how to get as small training data as possible. Therefore, we first build up a similarity function that takes two entries as input and produce the similarity score (soft function) or a boolean variable (hard function). Then we use this to find some interesting pairs.

We first parse the raw data into a list of dictionary (or features). Then we sort the list based on one of the features (like `fullname` or `state`). For each element of this sorted list, we check the below elements if they fit our similarity function. The benefit of this is that we do not need to check all pairs because once the pair does not meet the requirement (i.e. similarity function return 0 for not likely redundant.), we will stop checking for the below element will also not meet the requirement. Another benefit of this is that it can be run parallel easily. In this problem, we first use this method twice (one is sorting by `state` and one is sorting by `name`.). And then combine the result of this two methods.

## Feature Extraction
Here are the features constructed from dataset. In ideal situation, only non-redundant features are used. In case several features provide the same information/clues, it's usually best to use the one that provides the most gain. Keep in mind that the intuition behind most of features is just a wild guess.

```python
'''''
Feature 0: 0 reserved
Feature 1: a.Country=b.Country
Feature 2: a.name=b.name (hash)
Feature 3: a.street=b.street (hash)
Feature 4: a.firstname=b.firstname (hash)
Feature 5: a.lastname=b.lastname (hash)
Feature 6: minimum number of words in name, assume "names" is a list of string without prefixes & suffixes
Feature 7: maximum number of words in name, assume "names" is a list of string without prefixes & suffixes
Feature 8: proportion of characters in shared words --todo
Feature 9: proportion of shared words               --todo
Feature 10: name similarity, close to LCS
Feature 11: Similar to 10, but with prefixes and suffixes
Feature 12: Proportion of shared suffixes
Feature 13: Proportion of shared prefixes
Feature 14: Common Char of firstname
Feature 15: Common Char of lastname
Feature 16: LCS of firstname, similar to F14
Feature 17: LCS of lastname, similar to F15
Feature 18: Common Char of skills
Feature 19,20: Similar to F6,7, but with whole name(pre and suffixes)
Feature 21: Common Char in street
Feature 22: Common Char in name
Feature 23: State similarity: just the length of shared prefix in two strings
Feature 24: Count Common of skill words
'''''
```

## T-SNE

To test the performance of this feature extractor, we use [T-SNE](https://lvdmaaten.github.io/tsne/) technique. Here is the graph of the 2D embedding:
![alt text](https://raw.githubusercontent.com/zw1074/Duplication_Detection/master/Figures/T-SNE.png)

## Model Training

We feed the data into these models: ```['RandomForest_small', 'RandomForest_big', 'Gradientboost_small', 'Gradientboost_big', 'LogisticRegression_l1', 'LogisticRegression_l2']```

## Error Results
![alt text](https://github.com/zw1074/Duplication_Detection/blob/master/Figures/error.png)
