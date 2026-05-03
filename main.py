from email_automation import get_emails
from gemini import analyze_email, generate_checklist
from scorer import score_email

def main():
    print("🔄 Connecting to Gmail...")
    emails = get_emails(max_results=10)
    print(f"📬 Found {len(emails)} emails\n")

    for i, email in enumerate(emails):
        print(f"\n{'='*60}")
        print(f"📧 Email {i+1}")
        print(f"From    : {email['sender']}")
        print(f"Subject : {email['subject']}")
        #print(f"Body    : '{email['body']}'")  # ← add this
        print(f"{'='*60}")


        print("AI Analysis:")
        analysis = analyze_email(
            email['subject'],
            email['sender'],
            email['body']
        )
        print(analysis)

        
        scores = score_email(
            email['subject'],
            email['sender'],
            email['body']
        )

        print(f"\n OPPORTUNITY SCORES:")
        print(f"  Relevance    : {scores['relevance']}/10")
        print(f"  Urgency      : {scores['urgency']}/10")
        print(f"  Authenticity : {scores['authenticity']}/10")
        print(f"  Completeness : {scores['completeness']}/10")
        print(f"  {'─'*30}")
        print(f"  FINAL SCORE  : {scores['final']}/10")
        print(f"  {scores['recommendation']}")
        

        if scores['final'] >= 6:
            checklist = generate_checklist(email['subject'],email['sender'],email['body'])
            print("Action Checklist \n")
            print(checklist)
        else:
            print(f"\n CHECKLIST: Skipped — Not a relevant opportunity")
        

main()