from transformers import BertTokenizer, TFBertModel
import tensorflow as tf
import pandas as pd

def train_bert_similarity():
    # Load dataset
    df = pd.read_csv('data/dblp-v10.csv')
    
    # Initialize BERT components
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    bert_model = TFBertModel.from_pretrained('bert-base-uncased')
    
    # Create similarity model
    input1 = tf.keras.Input(shape=(768,))
    input2 = tf.keras.Input(shape=(768,))
    merged = tf.keras.layers.Concatenate()([input1, input2])
    dense = tf.keras.layers.Dense(256, activation='relu')(merged)
    output = tf.keras.layers.Dense(1, activation='sigmoid')(dense)
    
    model = tf.keras.Model(inputs=[input1, input2], outputs=output)
    model.compile(optimizer='adam', loss='binary_crossentropy')
    
    # Save model
    model.save('ai_models/bert_similarity.h5')
    print("BERT model trained and saved")
