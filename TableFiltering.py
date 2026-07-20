from Messages import messages

def clean_and_classify(messages):
    """
    Clean user messages and assigns each valid message a category.
    
    Messages without a user_id or with empty text are skipped.
    Keyword matching is case-insensitive, and when multiple categories match, the category whose keyword 
    appears first in the message is selected.

    Args:
        messages: list of dictionaries containing user messages.

        Returns:
            A list of valid message dictionaries with cleaned message text and an added category field.
    """

    keywords = {
    "grant_search": ["grant", "funding", "deadline", "scholarship"],
    "report_request": ["report", "file", "send again", "document"],
    "general_question": ["how", "what", "can you", "where", "why"],
    }

    result = []

    for msg in messages:
        user_id = msg.get("user_id", "").strip()
        text = msg.get("message", "").strip()

        if not user_id or not text:
            continue

        category = find_category(text, keywords)

        result.append({**msg, "message": text, "category": category})

    return result

def find_category(text, keywords):
    """
    Find the category whose keyword appears first in the message.

    Args:
        text: The message text to classify.
        keywords: A dictionary mapping category names to keyword lists.

    Returns:
        The matching category name, or "unknown" if no keyword matches.
    """

    text_lower = text.lower() # Convert the message text to lowercase to match keywords
    matches = []

    for category, words in keywords.items():
        for word in words:
            position = text_lower.find(word)

            if position != -1:
                matches.append((position, category))

    if matches:
        first_match = min(matches)
        return first_match[1]

    return "unknown"

output = clean_and_classify(messages)

for message in output:
    print(f"    {message}")
