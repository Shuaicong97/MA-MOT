from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load the llama3:text model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B")


# Function to generate rephrased queries
def generate_rephrases(query, model, tokenizer, num_rephrases=3, max_length=30, temperature=0.7):
    input_ids = tokenizer.encode(query, return_tensors="pt")
    print(f"Input IDs: {input_ids}")
    outputs = model.generate(input_ids, max_length=max_length, num_return_sequences=num_rephrases,
                             temperature=temperature)
    print(f"Outputs: {outputs}")
    rephrases = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    return rephrases


# Example queries
queries = ["A person raises his hand against his face", "I bake a chocolate cake.",
           "Best places to visit in Paris?"]

# Generate rephrases for each query
all_rephrases = {}
for query in queries:
    rephrases = generate_rephrases(query, model, tokenizer)
    all_rephrases[query] = rephrases

# Display the results
for query, rephrases in all_rephrases.items():
    print(f"Original Query: {query}")
    for i, rephrase in enumerate(rephrases):
        print(f"Rephrased {i + 1}: {rephrase}")
    print()
