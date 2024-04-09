from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.embeddings import FlairEmbeddings, StackedEmbeddings, WordEmbeddings
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer

# EMBEDDINGS
data_folder = "./data/flair"
corpus: Corpus = ColumnCorpus(
    data_folder, column_format={0: "text", 1: "ner"}, train_file="train_data_flair.txt"
)

# SETUP THE MODEL
tag_dictionary = corpus.make_label_dictionary(label_type="ner")

embedding_types = [WordEmbeddings("de"), FlairEmbeddings("de-forward"), FlairEmbeddings("de-backward")]
embeddings = StackedEmbeddings(embeddings=embedding_types)

tagger: SequenceTagger = SequenceTagger(
    hidden_size=256, embeddings=embeddings, tag_dictionary=tag_dictionary, tag_type="ner", use_crf=True
)

# TRAIN THE MODEL
trainer: ModelTrainer = ModelTrainer(tagger, corpus)
trainer.train("./data/flair", learning_rate=0.1, mini_batch_size=32, max_epochs=50)
