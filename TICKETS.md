# Tech Visit @ Cloudflight - The AI powered call-center

Recently, the new capabilities of LLM's have opened up a whole new world of business applications. In todays workshop you will explore one of these applications: An AI powered call-center. The business case is the following: A wholesales company wants to improve the availability of their call-center where customers can place oders. Therefore, a new phone line is created where customers can simply leave a voicemail with their order. An AI pipeline will then analyse the voicemail and produce an order which is sent to the ordering software, where employees can check and confirm the orders before they are placed. The pipeline consists of 5 steps:

## Voice 2 Order Pipeline:
1. Retrieve new voice message (audio data) from the voicemail server.
2. Transcribe the audio data i.e. recognize the speech of the voicemail as text data.
3. Recognize the relevant words in the text data that relate to the order (products, quantities and packaging units).
4. Find which of the articles from the inventory matches with each of the products recognized in the voice message.
5. Collect the matched articles together with their quantitis and send the order to the ordering software API.

For the sake of time we will assume for today that the speech recognition has already been implemented and performed, so that our pipeline starts with text messages. Also the matching with the inventory has been implemented for you using a semantic search solution. The focus of the workshop is the third step: recognizing relevant words. In machine learning this is called named entity recognition (NER). The goal is to implement, train and evaluate a solution for the NER step.

<br/><br/>
# Ticket 1: Implementing an NER solution

Check out the `from_text()` method of the `OrderGenerationService`. The first step here is to extract products from the given text using an NER solution. This entity extraction is implemented in the `extract_products()` method of the `EntityRecognitionService`. Your goal is to create a concrete implementation for the NER algorithm. Implement a concrete version of the abstract class `EntityRecognitionService` in `vto_pipeline/serivces/entity_recognition.py`. Be aware that `extract_products()` is given a text as input and returns a list of `RecognizedProduct`. With each recognized product containing:
- `identifier` (the text that contains the product name)
- `unit` (the packaging, box, tray, bottle, etc.)
- `quantity` (how many units)

Feel free to implement it anyway you like. We recommend, however, using either Flair or ChatGPT, since we already set up the dependencies of these libraries in the virtual environment. If you have time, implement both solutions!

### Approach 1 - Generative AI for NER
You can use ChatGPT's [chat completion feature](https://platform.openai.com/docs/guides/text-generation/chat-completions-api) to perform entity recognition. Essentially, this comes down to asking chatGPT to tell you the entities needed to return the recognized products. 

### Approach 2 - Classic NER using [Flair](https://github.com/flairNLP/flair)

Their [documentation](https://flairnlp.github.io/docs/intro) should provide you with all the necessary information to implement NER using flair. Of course without training the model doesn't actually work yet, but we can pretend that 

A few tips:
- Make a `Sentence` object, then run `model.predict()` on a `Sentence` object and get its `Span` objects, these are entities. 
- Flair will not group the entities belonging to the same product. We provide you the `find_entity_groups()` method for that.


### How to make sure your solution works
Check that the unittests are green! We already prepared them for you.

> Make sure to set the right `entity_recognition_model` in the `config.yaml` file before you run the tests!

<br/><br/>
# Ticket 2: Training / Evaluating the NER solution

> Make sure to set the right `entity_recognition_model` in the `config.yaml` file before you run the evaluation!

### Generating a dataset for training and evaluation
The customer didn't provide any training data, just information about the products they have. So, we will need to fabricate our own training and testing datasets.

To do so the first thing we will do is generate a set of products from the product data, in a way they would appear in a sentence spoken by a human. Have a look at `training/generate_product_examples.py`. Run this file to generate a set of 200 products. The product names contain a lot of symbols and parts that a human wouldn't mention. Implement the `clean_product_name()` method so that the file generates sensible product names. For example, remove dimensions from the names. Humans probably don't mention them. The performance of the pipeline depends on the quality of this training data!

To get a sense of what products look like, you can inspect them with the `inspect_products.ipynb` notebook (or just open the file).
Once you feel like you got a good set of product names, generate two sets, one for training and one for testing. Maybe check the contents again and clean further if necessary.
For both of these sets, generate order examples by running the `generate_order_examples.py` file. The file takes some template sentences and substitutes the product entities into them. Run the script once with `TEST = False` and once with `TEST = True`.
The sentences will be stored in `data/order_examples_<test|train>` respectively. Feel free to optimize this file to get better results, it's just a proposal!

### Classic NER using Flair
Now you are ready to train and evaluate the Flair model.

In order for Flair to use the previously generated training data, we have to format it first. Run `training/flair_format_order_examples.py`. Make sure it is able to find your folder with training data. This script will generate a `.txt` file in the `./data/flair` folder, which can be used to train a Flair model.
Train a model by running the `training/flair_train_model.py` script. (Be aware: this requires a ~1GB download, which takes some time. If you haven't started the exercise yet you can also run the script now and let it download in the background.)

Evaluation can be done using `evaluate/evaluate_order_generation.py`. (Also requires a ~1GB download). The evaluation will only work if your `FlairNerService` implementation works!
The script will output the accuracy of the model on the data you provide. Make sure you provide the folder with the testing set of order examples. Are score of around 75% would be ok.
If you're not there yet, try improving the quality of the training data or tuning the model or training parameters.

### Generative AI for NER

Similar to the Flair model, you need to generate a test dataset to be able to evaluate the performance of the entity recogition by the `GptEntityRecognitionService`. 
Once you have a testing dataset, you can evaluate the performance of your implementation using the same approach as with Flair. 
The goal now is to optimize prompting or other parameters such that the accuracy is highest.

### Evaluating the pipeline
Of course the accuracy we got from our evaluation doesn't necessarily represent how the pipeline performs on real data, since the testing data was artificial. If you like, the data folder contains some real world examples on which you can test the pipeline to see if the results make any sense. This data has no labels, so you need to inspect by hand how good the performance is. You can adapt the `load_example_order()` method so that the `main.py` file loads a real world example. This also adds the semantic search step to the pipeline. If you like you can inspect if it works well and try to improve it, for example by using different models.

> We had to curate the dataset, so it can be that some of the products mentioned in the voice messages are not in the product data. In this case change these items to something that is in the data. 

<br/><br/>
# Ticket 3: Pipeline architecture

In this last ticket you will design a solution for the architecture of the whole solution. This AI pipeline is only a small part of the actual system! 

Make groups of 3-5 people, give your team a nice name and construct an architecture block diagram for the whole system. Think about answering the following questions: 

- Voicemails are not stored on side. How to get new messages into our pipeline?
- Where do components run: Speech recognition, entity recognition, pipeline, search
- How does the product search get it‘s data?
- (How) should we store order proposals?
- What happens with the order proposals? (To webshop)
- Make sure we don‘t violate GDPA
- Do we need user authentication? Where?
- What about training the models? Do we need extra infrastructure?


