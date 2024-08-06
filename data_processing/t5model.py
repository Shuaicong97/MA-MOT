import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load the model and tokenizer
model_name = "t5-base"  # You can also use "t5-small", "t5-large", etc.
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)


def rephrase_text(text_list, num_return_sequences=5):
    rephrased_texts_dict = {}

    for text in text_list:
        # Prepare the input text with the task prefix
        input_text = f"paraphrase: {text} </s>"
        inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=len(text)+10, truncation=True)

        # Generate paraphrased text
        outputs = model.generate(
            inputs,
            max_length=len(text)+10,
            num_beams=num_return_sequences,
            num_return_sequences=num_return_sequences,
            early_stopping=True
        )

        # Decode generated texts
        rephrased_texts = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
        rephrased_texts_dict[text] = rephrased_texts

    return rephrased_texts_dict


# Example usage
if __name__ == "__main__":
    original_expressions = [
        "rephrase: The cat sat on the mat",
        "rephrase: Yacht is going towards the right side",
        "rephrase: The dog barked loudly at the stranger"
    ]

    rephrased_expressions_dict = rephrase_text(original_expressions)

    for original, rephrased in rephrased_expressions_dict.items():
        print(f"Original Expression: {original}")
        print("Rephrased Expressions:")
        for idx, expr in enumerate(rephrased, 1):
            print(f"  {idx}. {expr}")
        print()
