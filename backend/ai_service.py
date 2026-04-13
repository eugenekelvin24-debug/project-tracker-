from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter(prefix="/analyze-job", tags=["Analyze Job"])

# 1. Load the UNCASED model (Better for lazy typing!)
MODEL_NAME = "elastic/distilbert-base-uncased-finetuned-conll03-english"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)

# Simple list for Job Titles (The "Nutcracker" logic)
JOB_KEYWORDS = ["developer", "engineer", "manager", "designer", "analyst", "intern", "lead", "backend", "frontend"]

def extract_entities(text: str):
    inputs = tokenizer(text, return_tensors="pt")
    
    with torch.no_grad(): # Keeps CPU cool!
        outputs = model(**inputs).logits
    
    # Picking the winning "Cards" from the "Boxes"
    predictions = torch.argmax(outputs, dim=2)
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    
    entities = []
    current_word = ""
    current_label = ""

    for token, prediction in zip(tokens, predictions[0]):
        label = model.config.id2label[prediction.item()]
        if label != "O" and token not in ["[CLS]", "[SEP]"]:
            if token.startswith("##"):
                current_word += token.replace("##", "")
            else:
                if current_word:
                    entities.append({"word": current_word, "type": current_label})
                current_word = token
                # Mapping the AI labels to readable names
                current_label = "ORGANIZATION" if "ORG" in label else "LOCATION" if "LOC" in label else label
                
    if current_word:
        entities.append({"word": current_word, "type": current_label})
        
    return entities

def find_job_title(text: str):
    """Simple keyword search for the Job Title"""
    words = text.lower().split()
    found = [w for w in words if w in JOB_KEYWORDS]
    return " ".join(found).title() if found else "New Role"

class TextRequest(BaseModel):
    content: str

@router.post("/")
async def analyze_job(request: TextRequest):
    # Run the AI
    ai_results = extract_entities(request.content)
    
    # Run the Simple Logic
    job_title = find_job_title(request.content)
    
    # Pick the first Org and Loc found (or set defaults)
    company = next((e['word'] for e in ai_results if e['type'] == 'ORGANIZATION'), "Unknown Company")
    location = next((e['word'] for e in ai_results if e['type'] == 'LOCATION'), "Remote")

    return {
        "status": "success",
        "data": {
            "company": company.title(),   # Force "amazon" -> "Amazon"
            "location": location.title(), # Force "lagos" -> "Lagos"
            "title": job_title,
            "description": request.content # Keep the full text for your DB
        }
    }