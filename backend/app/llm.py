from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Use a local open-source instruction model
MODEL_NAME = "mosaicml/mpt-7b-instruct"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto")

def generate_answer(query, chunks, max_tokens=300):
    context = "\n\n".join([chunk["text"] for chunk in chunks])
    prompt = f"Using the following documents, answer the question succinctly:\n{context}\n\nQuestion: {query}\nAnswer:"
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=max_tokens)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer
