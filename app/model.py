from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def prediction(file_paths,uploaded_text):
    sentences = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            text = file.read()
            sentences.append(text)

    sentences.append(uploaded_text)
            
            # Load the pre-trained BERT-based model
    model_name = 'sentence-transformers/bert-base-nli-mean-tokens'
    model = SentenceTransformer(model_name)
    
    # Use the model to encode the sentences
    sentence_embeddings = model.encode(sentences)
    
    # Calculate cosine similarity between the uploaded text and the rest of the sentence embeddings
    query_embedding = sentence_embeddings[-1]  # Uploaded text embedding
    candidate_embeddings = sentence_embeddings[:-1]  # Embeddings of other files
    cosine_similarities = cosine_similarity([query_embedding], candidate_embeddings)[0]
    
    # Combine the candidate sentences with their corresponding cosine similarities
    predictions = list(zip(file_paths, cosine_similarities))
    
    # Sort the predictions based on cosine similarity (highest to lowest)
    predictions.sort(key=lambda x: x[1], reverse=True)

    return predictions
        