import streamlit as st
from email_automation import get_emails
from gemini import analyze_email, generate_checklist
from scorer import score_email

st.set_page_config(page_title='Gmail Automation',layout='wide')

st.title('Gmail Automation - Smart Opportunity Finder')
st.markdown('Automatically finds Scholarships, internships, and Competitions in your inbox')
st.divider()

st.sidebar.title('Settings')
max_emails = st.sidebar.slider('How many mails to scan',min_value=1,max_value=30,value=5)
min_score=6
st.divider()

if st.button('Scan my inbox', use_container_width=True):
    with st.spinner('Connecting to Gmail....'):
        emails = get_emails(max_emails)
    
    st.success(f'Found {len(emails)} emails')
    st.success('AI Analyzing...')
    st.divider()

    high_priority = 0
    medium_priority = 0
    low_priority   = 0

    for i, email in enumerate(emails):
        scores = score_email(email['subject'],email['sender'],email['body'])

        if scores['final'] >= 7:
            high_priority += 1
        elif scores['final'] >= 5:
            medium_priority += 1
        else:
            low_priority += 1

        
        with st.expander(f'{email['subject']} - Scores {scores["final"]}/10'):
            st.markdown(f' From: {email['sender']}')
            st.divider()

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(label='Relevence', value=f'{scores['relevance']}/10')
            with col2:
                st.metric(label='Urgency', value=f'{scores['urgency']}/10')
            with col3:
                st.metric(label='Authenticity', value=f'{scores['authenticity']}/10')
            with col4:
                st.metric(label='Completeness', value=f'{scores['completeness']}/10')
            st.divider()

            st.markdown(f'### {scores['recommendation']}')

            if scores['final'] >= min_score:
                with st.spinner('AI Analyzing....'):
                    analysis = analyze_email(email['subject'],email['sender'],email['body'])
                
                st.markdown('AI Analysis: ')
                st.markdown(analysis)

                with st.spinner('Generating Checklist...'):
                    checklist = generate_checklist(email['subject'],email['sender'],email['body'])
                
                st.markdown('Action Checklist: ')
                st.markdown(checklist)

            else:
                st.info("⏭️ Skipped — Score too low")

    st.divider()


    st.markdown("## Inbox Summary")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label=" High Priority",
            value=high_priority
        )
    with col2:
        st.metric(
            label=" Medium Priority",
            value=medium_priority
        )
    with col3:
        st.metric(
            label=" Low Priority",
            value=low_priority
        )






