import gradio as gr
import transformers
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "meta-llama/Meta-Llama-3-8B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def rephrase_text(text_list, num_return_sequences=5):
    rephrased_texts_dict = {}

    for text in text_list:
        # Tokenize input
        inputs = tokenizer(text, return_tensors="pt")

        # Generate rephrased text
        with torch.no_grad():
            outputs = model.generate(
                inputs["input_ids"],
                num_return_sequences=num_return_sequences,
                num_beams=num_return_sequences,
                max_length=len(text.split()) + 10,  # Adjust max length as needed
                early_stopping=True
            )

        # Decode generated texts
        rephrased_texts = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
        rephrased_texts_dict[text] = rephrased_texts

    return rephrased_texts_dict


if __name__ == "__main__":
    original_expressions = [
        "Elephant is walking towards the right side",
        "Cat is going from right to left side",
        "Yacht is going towards the right side"
    ]

    rephrased_expressions_dict = rephrase_text(original_expressions)
    for original, rephrased in rephrased_expressions_dict.items():
        print(f"Original Expression: {original}")
        print("\nRephrased Expressions: ")
        for idx, expr in enumerate(rephrased, 1):
            print(f"{idx}. {expr} ")
        print()
