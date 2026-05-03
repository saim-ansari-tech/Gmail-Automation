from datetime import datetime
import re

def get_rel_score(subject, body):
    keywords = ['scholarship', 'internship', 'competition', 'opportunity', 'apply', 'application', 'eligible','eligibility',
                 'fellowship', 'grant', 'funding','award', 'contest', 'program', 'deadline', 'student']
    
    full_txt = (subject + " " + body).lower()

    count = 0

    for keyword in keywords:
        if keyword in full_txt:
            count += 1


    score = min((count/5)*10,10)
    
    return round(score, 1)


def get_urgency_score(body):

    today = datetime.today()

    patterns = [
        r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',     
        r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',    
        r'(\w+ \d{1,2},? \d{4})',                   
    ]
    
    for pattern in patterns:
        match = re.search(pattern, body)
        if match:
            try:
                date_str = match.group(0)
                for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%B %d, %Y', '%B %d %Y']:
                    try:
                        deadline = datetime.strptime(date_str, fmt)
                        days_left = (deadline - today).days

                        if days_left <= 0:
                            return 0
                        elif days_left <= 7:
                            return 10
                        elif days_left <= 15:
                            return 7
                        elif days_left <= 30:
                            return 4
                        else:
                            return 2
                    except:
                        continue

            except:
                continue

    return 2


def get_authenticity_score(sender):
    sender = sender.lower()
    match = re.search(r'@([\w.]+)', sender)
    if not match:
        return 3  
    
    domain = match.group(1)
    

    if '.edu' in domain:
        return 10   
    elif '.gov' in domain:
        return 10   
    elif '.org' in domain:
        return 8   
    elif '.com' in domain:
        
        trusted_companies = [
            'google', 'microsoft', 'amazon', 
            'linkedin', 'coursera', 'openai'
        ]
        if any(company in domain for company in trusted_companies):
            return 8
        else:
            return 6  
    elif 'gmail.com' in domain:
        return 3    
    else:
        return 5    
    
def get_completeness_score(body):
   
    score = 0
    body_lower = body.lower()
    
    
    if any(word in body_lower for word in ['deadline', 'last date', 'apply by', 'due date']):
        score += 2.5
    
   
    if any(word in body_lower for word in ['http', 'www', 'apply at', 'link', 'click here']):
        score += 2.5
    
   
    if any(word in body_lower for word in ['requirement', 'documents', 'cv', 'resume', 'transcript', 'letter']):
        score += 2.5
    
    
    if any(word in body_lower for word in ['contact', 'email', 'phone', 'reach us', 'query']):
        score += 2.5
    
    return round(score, 1)

def get_final_score(relevance, urgency, authenticity, completeness):
 
    final = (relevance * 0.35 + urgency * 0.25 + authenticity * 0.20 + completeness * 0.20)
    
    return round(final, 1)

def get_recommendation(final_score):

    if final_score >= 8:
        return " HIGHLY RECOMMENDED — Apply Immediately!"
    elif final_score >= 6:
        return " RECOMMENDED — Worth Applying"
    elif final_score >= 4:
        return " MODERATE — Review Carefully"
    else:
        return " LOW PRIORITY — Likely Not Relevant"


def score_email(subject, sender, body):
  
    relevance    = get_rel_score(subject, body)
    urgency      = get_urgency_score(body)
    authenticity = get_authenticity_score(sender)
    completeness = get_completeness_score(body)
    final        = get_final_score(relevance, urgency, authenticity, completeness)
    
    return {
        'relevance'    : relevance,
        'urgency'      : urgency,
        'authenticity' : authenticity,
        'completeness' : completeness,
        'final'        : final,
        'recommendation': get_recommendation(final)
    }





