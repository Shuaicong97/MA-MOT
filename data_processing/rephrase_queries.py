from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from huggingface_hub import login


login(token="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")
#
# model_name = "meta-llama/Meta-Llama-3-8B"
#
# # Load the llama3:text model and tokenizer
# try:
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModelForCausalLM.from_pretrained(model_name, pad_token_id=tokenizer.pad_token_id)
#     print("Model and tokenizer loaded successfully!")
# except Exception as e:
#     print(f"An error occurred: {e}")
# # tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
# # model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B")
#
#
# # Function to generate rephrased queries
# def generate_rephrases(query, model, tokenizer, num_rephrases=5, max_length=50, temperature=0.7):
#     inputs = tokenizer(query, return_tensors="pt", truncation=True, padding=True)
#     input_ids = inputs['input_ids']
#     attention_mask = inputs['attention_mask']
#
#     pad_token_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id
#     if tokenizer.pad_token_id is None:
#         tokenizer.pad_token = tokenizer.eos_token
#     outputs = model.generate(
#         input_ids=input_ids,
#         attention_mask=attention_mask,
#         max_length=max_length,
#         num_return_sequences=num_rephrases,
#         temperature=temperature,
#         pad_token_id=pad_token_id
#     )
#
#     # rephrases = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
#     rephrases = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
#     return rephrases
#
# # Example queries
# queries = ["A person raises his hand against his face", "How do I bake a chocolate cake?", "Best places to visit in Paris?"]
#
# # Generate rephrases for each query
# all_rephrases = {}
# for query in queries:
#     rephrases = generate_rephrases(query, model, tokenizer)
#     all_rephrases[query] = rephrases
#
# # Display the results
# for query, rephrases in all_rephrases.items():
#     print(f"Original Query: {query}")
#     for i, rephrase in enumerate(rephrases):
#         print(f"Rephrased {i+1}: {rephrase}")
#     print()


def load_model_and_tokenizer(model_name):
    """
    加载模型和分词器
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return model, tokenizer


def rephrase_query(query, model, tokenizer, max_length=50):
    """
    使用给定的模型对查询进行重新表述
    """
    inputs = tokenizer.encode(query, return_tensors='pt')
    print(inputs)
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']

    outputs = model.generate(input_ids=input_ids,  attention_mask=attention_mask, max_length=max_length,
                             num_return_sequences=3, do_sample=True)
    rephrased_queries = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    return rephrased_queries


def main():
    model_name = "meta-llama/Meta-Llama-3-8B"
    model, tokenizer = load_model_and_tokenizer(model_name)

    queries = [
        "A person raises his hand against his face",
        "Elephant is walking towards the left side",
    ]

    for query in queries:
        print(f"Original Query: {query}")
        rephrased_queries = rephrase_query(query, model, tokenizer)
        print("Rephrased Queries:")
        for i, rq in enumerate(rephrased_queries):
            print(f"  {i + 1}: {rq}")
        print()


if __name__ == "__main__":
    main()
