from google import genai

# Read API key from file
with open("api_key.txt", "r") as file:
    api_key = file.read().strip()

# Initialize client
client = genai.Client(api_key=api_key)


# ─── ANALYZE EMAIL ──────────────────────────────────────────
def analyze_email(subject, sender, body):
    
    # Add this instead — assign first, then check
    content = "No body content"
    if body:
        content = body

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=f"""
You are an AI assistant that analyzes emails for students.

Analyze this email and extract the following:

1. What is this email about? (one line)
2. Type: Scholarship / Internship / Competition / Other
3. Is it relevant for a university student? (Yes/No and why)
4. Deadline: (if mentioned, else say Not mentioned)
5. Required documents: (list them, else say Not mentioned)
6. Apply link: (if mentioned, else say Not mentioned)

Email:
From: {sender}
Subject: {subject}
Body: {content[:1000]}
"""
    )

    return response.text

def generate_checklist(subject, sender, body):
    content = "No body content"
    if body:
        content = body
    
    response = client.models.generate_content(
        model = 'gemini-3.1-flash-lite-preview',
        contents=f"""You are an AI assitance helping a university student to take action on an opportuinity email
                    based on this email, generate a clear step by step action checklist the student should follow
                    
                    Rules:
                    - be specific to this email, not generic
                    - Order steps logically (check eligibility first, submit last)
                    - Include document prepation steps if needed
                    - Include deadline reminder if mentioned
                    - Maximum 8 steps
                    - Format each step as: Step X -> [Action]

                    Email:
                    From: {sender}
                    Subject: {subject}
                    Body: {content[:1000]}
                    """
    )

    return response.text