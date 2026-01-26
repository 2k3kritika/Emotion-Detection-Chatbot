#!/usr/bin/env python
# coding: utf-8

# #### Import Libraries

# In[156]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from gensim.models import KeyedVectors
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, Bidirectional, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.metrics import classification_report
from tensorflow.keras.models import save_model
from wordcloud import WordCloud
import pickle
import nltk
import warnings
from nltk.corpus import stopwords

nltk.download('stopwords')

warnings.filterwarnings("ignore")

%matplotlib inline

# #### Merging the Dataset

# In[130]:


def concatenate_files(file_list, output_file):
    with open(output_file, 'w') as outfile:
        for file_name in file_list:
            with open(file_name, 'r') as infile:
                for line in infile:
                    outfile.write(line)

file_list = ['train.txt', 'test.txt', 'val.txt']
output_file = 'dataset.txt'

concatenate_files(file_list, output_file)

print("Files concatenated successfully as 'dataset.txt'")

# #### Load the Dataset

# In[131]:


df = pd.read_csv("dataset.txt", delimiter=';', header=None, names=['Sentences', 'Target'])
sentences = df['Sentences'].values
emotions = df['Target'].values

# #### Dataset Exploration

# In[79]:


print(df.head())

# In[80]:


print(df.shape)

# In[81]:


print(df.info())

# In[82]:


df.isnull().sum()

# In[83]:


print(df['Target'].unique())

# In[84]:


print((df.Target.value_counts() / df.shape[0] * 100).round(2))

# #### Distribution of Target Variable

# In[85]:


plt.figure(figsize=(8, 4))

ax = sns.countplot(x='Target', data=df, palette='Set2', order=df['Target'].value_counts().index)

for p in ax.patches:
    ax.annotate(format(p.get_height(), '.0f'),
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center', va = 'center',
                   xytext = (0, 5),
                   textcoords = 'offset points')

plt.xlabel('Emotions', fontsize=12)
plt.ylabel('Count', fontsize=10)
plt.title('Distribution of Target variable', fontsize=14)

plt.tight_layout()
plt.show()

# In[86]:


df["Sentences_length"] = [len(i) for i in df["Sentences"]]

# In[87]:


df.head(5)

# #### Max and Min Sentence length

# In[88]:


print(df['Sentences_length'].max())
print(df['Sentences_length'].min())

# In[89]:


sns.kdeplot(x=df["Sentences_length"], hue=df["Target"])

# #### Number of Stopwords by Sentences

# In[105]:


def count_stopwords(sentence):
    stop_words = set(stopwords.words('english'))
    tokens = sentence.split()
    return sum(1 for word in tokens if word.lower() in stop_words)

df['Stopword_Count'] = df['Sentences'].apply(count_stopwords)

plt.figure(figsize=(7, 4))
sns.histplot(df['Stopword_Count'], bins=15, kde=True, color='Skyblue')
plt.xlabel('Number of Stopwords')
plt.ylabel('Count of Sentences')
plt.title('Number of Stopwords by Sentences')
plt.show()

# #### Removing the Stopwords

# In[106]:


stop_words = set(stopwords.words('english'))

# In[107]:


def remove_stopwords(text):
    tokens = text.split()
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    return ' '.join(filtered_tokens)

df['Sentences'] = df['Sentences'].apply(remove_stopwords)

# #### Plot for words in Sentences after stopwords removal

# In[108]:


sns.kdeplot(data=df, x=df["Sentences"].str.len(), hue=df["Target"])

# #### Word Cloud for Different Emotions

# In[109]:


def generate_wordcloud(category_sentences, ax, title):
    wordcloud = WordCloud(width=400, height=300, background_color ='white', min_font_size = 10).generate(' '.join(category_sentences))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(title)

category_groups = df.groupby('Target')['Sentences'].apply(list)

fig, axs = plt.subplots(2, 3, figsize=(12, 7))
fig.subplots_adjust(wspace=0.1)

for i, (category, sentences) in enumerate(category_groups.items()):
    row = i // 3
    col = i % 3
    generate_wordcloud(sentences, axs[row, col], category)

plt.suptitle('Word Cloud for Different Emotions', fontsize=16)

plt.show()

# In[116]:


df.drop(["Sentences_length","Stopword_Count"],axis = 1)

# #### Downloading the Pretrained Model - GLoVe

# In[35]:


!wget https://huggingface.co/stanfordnlp/glove/resolve/main/glove.6B.zip

# In[36]:


import zipfile
zip_ref = zipfile.ZipFile("glove.6B.zip", 'r')
zip_ref.extractall(".")
zip_ref.close()

# #### Load the model

# In[37]:


def load_glove_model(File):
    print("Loading Glove Model")
    glove_model = {}
    with open('glove.6B.300d.txt','r') as f:
        for line in f:
            split_line = line.split()
            word = split_line[0]
            embedding = np.array(split_line[1:], dtype=np.float64)
            glove_model[word] = embedding
    print(f"{len(glove_model)} words loaded!")
    return glove_model

# In[38]:


glove_model = load_glove_model('glove.6B.300d.txt')

# #### Tokenize the sentences and create word-to-index mapping

# In[161]:


word_to_index = {}
index = 1  # Start index from 1, leaving 0 for padding
for sentence in sentences:
    for word in sentence.split():
        if word not in word_to_index:
            word_to_index[word] = index
            index += 1

# #### Creating an embedding matrix

# In[136]:


embedding_matrix = np.zeros((len(word_to_index) + 1, len(glove_model['the'])))  # Add 1 to include padding token
for word, index in word_to_index.items():
    if word in glove_model:
        embedding_matrix[index] = glove_model[word]

# #### Performing label encoding on the target labels

# In[137]:


label_encoder = LabelEncoder()
encoded_emotions = label_encoder.fit_transform(emotions)

# #### Split the dataset into training, validation, and testing sets

# In[138]:


X_train, X_test, y_train, y_test = train_test_split(sentences, encoded_emotions, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.1, random_state=42)

# #### Converting sentences to sequences of indices

# In[139]:


X_train_sequences = [[word_to_index[word] for word in sentence.split() if word in word_to_index] for sentence in X_train]
X_val_sequences = [[word_to_index[word] for word in sentence.split() if word in word_to_index] for sentence in X_val]
X_test_sequences = [[word_to_index[word] for word in sentence.split() if word in word_to_index] for sentence in X_test]

# #### Padding sequences to make them of equal length

# In[140]:


max_sequence_length = max(len(sequence) for sequence in X_train_sequences + X_val_sequences + X_test_sequences)
X_train_padded = pad_sequences(X_train_sequences, maxlen=max_sequence_length, padding='post')
X_val_padded = pad_sequences(X_val_sequences, maxlen=max_sequence_length, padding='post')
X_test_padded = pad_sequences(X_test_sequences, maxlen=max_sequence_length, padding='post')

# #### Train the Model

# In[141]:


bilstm_model = Sequential([
    Embedding(input_dim=len(word_to_index) + 1, output_dim=len(glove_model['the']), weights=[embedding_matrix], input_length=max_sequence_length, trainable=False),
    Bidirectional(LSTM(64, dropout=0.2, recurrent_dropout=0.2)),
    Dropout(0.2),  # Dropout layer added after the Bidirectional LSTM layer
    Dense(len(label_encoder.classes_), activation='softmax')
])
bilstm_model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Early stopping criteria
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# In[159]:


bilstm_model.summary()

# In[142]:


bilstm_history = bilstm_model.fit(X_train_padded, y_train, epochs=25, batch_size=32, validation_data=(X_val_padded, y_val), callbacks=[early_stopping])

# #### Evaluating the model

# In[143]:


loss, accuracy = bilstm_model.evaluate(X_test_padded, y_test)
print("BiLSTM Accuracy:", accuracy)

# In[145]:


y_pred_prob = bilstm_model.predict(X_test_padded)
y_pred = np.argmax(y_pred_prob, axis=1)

print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# #### Plot for training and validation loss

# In[146]:


plt.plot(bilstm_history.history['loss'], label='Training Loss')
plt.plot(bilstm_history.history['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# #### Plot for training and validation accuracy

# In[147]:


plt.plot(bilstm_history.history['accuracy'], label='Training Accuracy')
plt.plot(bilstm_history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# #### Predicting New Sentences

# In[154]:


new_sentences = [
    "I feel excited about the upcoming project",
    "This situation makes me anxious",
    "I am calm and relaxed right now"
]

tokenizer = lambda x: [[word_to_index[word] for word in sentence.split() if word in word_to_index] for sentence in x]

new_sequences = tokenizer(new_sentences)
new_sequences_padded = pad_sequences(new_sequences, maxlen=max_sequence_length, padding='post')

predictions = bilstm_model.predict(new_sequences_padded)

predicted_emotions = label_encoder.inverse_transform(np.argmax(predictions, axis=1))

print("Predicted Emotions for New Sentences:")
for sentence, emotion in zip(new_sentences, predicted_emotions):
    print(f"Sentence: {sentence} | Predicted Emotion: {emotion}")

# #### Save Model

# In[157]:


bilstm_model.save('bilstm_model.h5')

with open('bilstm_model.pkl', 'wb') as f:
    pickle.dump(bilstm_model, f)

print("Model saved successfully!")
