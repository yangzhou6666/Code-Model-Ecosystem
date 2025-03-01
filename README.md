# Code-Model-Ecosystem

Here is the replication package of our MSR 2024 submission, titled: "**Understanding the Ecosystem of Large Language Models of Code: An Exploratory Study on Hugging Face**"

This repository includes:

1. The data of the collected ecosystem, stored in csv files.
2. Necessary scripts and Jupyter notebooks to process the data and obtain results in the paper.


# Code Model Ecosystem Data

> It should be noted that the ecosystem is evolving. New models are added and some metrics (e.g., number of downloads) are changing as well. 

The data is stored under `./data` directory. 

1. `./data/all.csv` includes all the models we obtained using steps described in the paper. It also contains manually labeled information, including datasets, parent model, etc.
2. `./data/data-data_dependency.csv` includes the dependency information between datasets.
3. `./data/model_data_dependency.csv` includes the dependency information between datasets and models.
4. `./data/model_dependency.csv` includes the dependency information between models.

The Figure 3 and some statistical results of the ecosystem (e.g., number of models and dependencies) are obtained by imported these files into `gephi`, a network analysis tool.

# Replication for each research question

## RQ1. 

The jupyter notebook `RQ1.ipynb` contains the steps to replicate RQ1.

## RQ2.

RQ2 is largely based on manual annotation of the model reuse type and we count the distribution manually.

## RQ3. 

The jupyter notebook `RQ3.ipynb` contains the steps to replicate RQ3.


## Automatically Build LLM4Code ecosystem

The prompts and the scripts for calling OpenAI models in under `automation` folder.

