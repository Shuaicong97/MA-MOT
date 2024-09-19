# Given JSON-like content, we will process it to compare rephrased_content and original_content
data = [
    {
        "line_number": 389,
        "rephrased_content": "The person walking on the street moves towards the shop from the street.",
        "original_content": "The person walking on the street is going towards the Shop from street"
    },
    {
        "line_number": 390,
        "rephrased_content": "The person inside the electronics showroom.",
        "original_content": "The person who is inside Electronics showroom"
    },
    {
        "line_number": 391,
        "rephrased_content": "People standing against the walls.",
        "original_content": "The people who are standing against the walls"
    }
]


# Function to compare rephrased and original content
def compare_rephrased_and_original(data):
    for entry in data:
        rephrased = entry["rephrased_content"].strip()
        original = entry["original_content"].strip()

        # Check if the two contents are essentially the same in expression
        if original == rephrased:
            entry["rephrased_content"] = ""

    return data


# Process the data
output_data = compare_rephrased_and_original(data)
print(output_data)
