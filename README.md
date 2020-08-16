# Repository for Data Science Capstone Project
### COVID-19 Sentiment Analysis
### Regis University - MSDS 696
### Jason Huffman


This project was performed as a capstone requirement for the Regis University MSDS program.

The goal of this project was to perform a sentiment analysis on tweets from the Denver metro area related to the COVID-19 outbreak and CDC recommended best practices for containing the spread of COVID-19, such as practicing good hygiene, social distancing, and wearing masks. This information was used to create a sentiment score for the area that describes how positive or negative sentiments in the area were as a whole, toward a particular idea or policy each day.

Once the sentiment analysis was performed, the sentiment scores were compared to the number of COVID-19 cases per 100,000 individuals in the area and this was used to create a prediction model with the intent of predicting the infection rate.

The reason for doing this project was in hopes that sentiment changes displayed on social media might be able provide a bit of advanced notice that infection rates are about to change; this information could then be used by governments and health departments to proactively prepare for the change and adjust policies and marketing accordingly

The Python files in this repository can be used in the following order to replicate the work performed for this project:

- [Twitter Data Pull](./twitter_data_pull.py)
- [Read in Data](./read_in_data.py)
- [Sentiment Analysis](./sentiment_analysis.py)
- [Organize Data](./organize_data.py)
- [Model Creation](./model_creation.py)

A full write up of the project can be found in the Jupyter Notebook file
[here](./MSDS696_JHuffman_Write-up.ipynb)
