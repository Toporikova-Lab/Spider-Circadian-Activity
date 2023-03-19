# How Can We Tell if a Spider Has Died?

@ Author [Jack Bosco](https://GitHub.com/JackBosco)

### Check out the idea pitch for a basic outline to the problem. 

### What I have are three .csv files where spider activity is tallied at each minute (row). Some friendly Pre-Meds in the Neuroscience department marked off points where the spider died, I can use that to __train__ the models.

### I want to try three different approaches here:

1. A simple multilayered perceptron (MLP) with nothing but NumPy

2. A more complicated and powerful MLP model with PyTorch

3. Something called an LSTM. I will cross that bridge when I get to it

### But before I can do any of that, I need to somehow parse this data into something we can use to train these suckers.

* First, define a *target* output for each spider by saving the row where it died
  * this is what makes the data useable for training the models
* Then pad all empty rows with 0s so the training data *looks like* the testing data
* Lastly, the dataset might be too large to train without using something like Amazon Web Services
  * I can crunch the thousands of rows in the files to a few hundred to make the input and output spaces less complex
    * This means converting minutes to hours or even days
  * I then flatten the data to 0s and 1s (0 for no activity, 1 for more than no activity) in each interval, again for complexity

## Using a simple MLP Classifier

## Using a DEEP MLP Classifier

## Using an LSTM Classifier
