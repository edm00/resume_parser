# Import necessary libraries
import os
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify, render_template
import PyPDF2

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

# Initialize Flask app
app = Flask(__name__)

# Function to extract text from a PDF resume
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text

# Function to preprocess text (cleaning and tokenization)
def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

# Function to compute similarity between resume and job descriptions
def compute_similarity(resume_text, job_descriptions):
    # Preprocess resume text
    resume_processed = preprocess_text(resume_text)
    
    # Preprocess job descriptions
    job_processed = [preprocess_text(job) for job in job_descriptions]
    
    # Combine resume and job descriptions for TF-IDF vectorization
    all_texts = [resume_processed] + job_processed
    
    # Compute TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # Compute cosine similarity between resume and job descriptions
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    return similarities

# Sample job descriptions (replace with scraped or real data)
job_descriptions = [
    "We are looking for a data scientist with experience in Python, machine learning, and NLP.",
    "Our company needs a software engineer proficient in Java, Spring Boot, and microservices.",
    "Seeking a marketing specialist with expertise in digital marketing and SEO.",
    "Hiring a financial analyst with strong Excel skills and knowledge of financial modeling."
]

# Flask route for home page
@app.route("/")
def home():
    return render_template("./index.html")

# Flask route to handle resume upload and matching
@app.route("/match", methods=["POST"])
def match_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400
    
    # Save the uploaded resume
    resume_file = request.files["resume"]
    resume_path = os.path.join("uploads", resume_file.filename)
    resume_file.save(resume_path)
    
    # Extract text from the resume
    resume_text = extract_text_from_pdf(resume_path)
    
    # Compute similarity with job descriptions
    similarities = compute_similarity(resume_text, job_descriptions)
    
    # Prepare results
    results = []
    for i, similarity in enumerate(similarities):
        results.append({
            "job_description": job_descriptions[i],
            "similarity_score": round(similarity, 2)
        })
    
    # Sort results by similarity score (descending order)
    results.sort(key=lambda x: x["similarity_score"], reverse=True)
    
    return jsonify({"results": results})

# Run the Flask app
if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)