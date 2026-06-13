# doc_templates.py
# Defines form fields and AI prompts for each document type

DOCUMENT_TYPES = {

    "Service Contract": {
        "icon":        "📄",
        "description": "Legal agreement between a service provider and client",
        "fields": [
            {"key": "provider_name",    "label": "Service Provider Name",    "type": "text",     "placeholder": "e.g. TechCorp India Pvt Ltd"},
            {"key": "client_name",      "label": "Client Name",              "type": "text",     "placeholder": "e.g. Acme Corporation"},
            {"key": "service_desc",     "label": "Services to be Provided",  "type": "textarea", "placeholder": "Describe the services in detail"},
            {"key": "contract_value",   "label": "Contract Value",           "type": "text",     "placeholder": "e.g. Rs. 5,00,000 per year"},
            {"key": "payment_terms",    "label": "Payment Terms",            "type": "text",     "placeholder": "e.g. Net 30 days, monthly invoicing"},
            {"key": "start_date",       "label": "Start Date",               "type": "text",     "placeholder": "e.g. July 1, 2026"},
            {"key": "duration",         "label": "Contract Duration",        "type": "text",     "placeholder": "e.g. 12 months"},
            {"key": "deliverables",     "label": "Key Deliverables",         "type": "textarea", "placeholder": "List the main deliverables"},
            {"key": "governing_law",    "label": "Governing Law",            "type": "text",     "placeholder": "e.g. Laws of India, jurisdiction Mumbai"},
        ],
        "prompt_template": """You are a legal document specialist.
Generate a professional Service Contract with the following details:

Service Provider: {provider_name}
Client: {client_name}
Services: {service_desc}
Contract Value: {contract_value}
Payment Terms: {payment_terms}
Start Date: {start_date}
Duration: {duration}
Deliverables: {deliverables}
Governing Law: {governing_law}

Generate a complete, professional service contract with these sections:
1. PARTIES (with full details)
2. SCOPE OF SERVICES
3. DELIVERABLES AND TIMELINE
4. FEES AND PAYMENT TERMS
5. INTELLECTUAL PROPERTY RIGHTS
6. CONFIDENTIALITY
7. WARRANTIES AND REPRESENTATIONS
8. LIMITATION OF LIABILITY
9. TERMINATION
10. GOVERNING LAW AND DISPUTE RESOLUTION
11. ENTIRE AGREEMENT
12. SIGNATURES

Use professional legal language. Number all clauses. Be specific with the provided details."""
    },

    "Business Proposal": {
        "icon":        "📋",
        "description": "Professional proposal to win a client or project",
        "fields": [
            {"key": "company_name",   "label": "Your Company Name",    "type": "text",     "placeholder": "e.g. TechCorp India Pvt Ltd"},
            {"key": "client_name",    "label": "Prospect/Client Name", "type": "text",     "placeholder": "e.g. Acme Corporation"},
            {"key": "project_name",   "label": "Project Name",         "type": "text",     "placeholder": "e.g. Digital Transformation Initiative"},
            {"key": "problem",        "label": "Client Problem",       "type": "textarea", "placeholder": "What problem does the client have?"},
            {"key": "solution",       "label": "Your Solution",        "type": "textarea", "placeholder": "How will you solve it?"},
            {"key": "pricing",        "label": "Pricing",              "type": "text",     "placeholder": "e.g. Rs. 12,00,000 for 6 months"},
            {"key": "timeline",       "label": "Timeline",             "type": "text",     "placeholder": "e.g. 6 months, starting August 2026"},
            {"key": "team",           "label": "Team & Expertise",     "type": "textarea", "placeholder": "Key team members and their expertise"},
            {"key": "why_us",         "label": "Why Choose Us",        "type": "textarea", "placeholder": "Your unique value proposition"},
        ],
        "prompt_template": """You are a business development expert.
Generate a compelling Business Proposal with these details:

Company: {company_name}
Client: {client_name}
Project: {project_name}
Problem: {problem}
Solution: {solution}
Pricing: {pricing}
Timeline: {timeline}
Team: {team}
Why Us: {why_us}

Generate a complete, persuasive proposal with:
1. COVER PAGE (with date and reference number)
2. EXECUTIVE SUMMARY
3. UNDERSTANDING THE PROBLEM
4. PROPOSED SOLUTION
5. METHODOLOGY AND APPROACH
6. DELIVERABLES
7. PROJECT TIMELINE
8. INVESTMENT AND PRICING
9. OUR TEAM
10. WHY CHOOSE US
11. TERMS AND CONDITIONS
12. NEXT STEPS AND CALL TO ACTION

Make it compelling and professional. Use specific details from the inputs."""
    },

    "NDA": {
        "icon":        "🔒",
        "description": "Non-Disclosure Agreement to protect confidential information",
        "fields": [
            {"key": "party_a",        "label": "Disclosing Party",         "type": "text",     "placeholder": "e.g. TechCorp India Pvt Ltd"},
            {"key": "party_b",        "label": "Receiving Party",          "type": "text",     "placeholder": "e.g. Acme Corporation"},
            {"key": "purpose",        "label": "Purpose of Disclosure",    "type": "textarea", "placeholder": "e.g. Evaluation of potential business partnership"},
            {"key": "conf_info",      "label": "Confidential Information", "type": "textarea", "placeholder": "What types of information are protected?"},
            {"key": "duration",       "label": "Duration of Agreement",    "type": "text",     "placeholder": "e.g. 2 years from signing"},
            {"key": "exclusions",     "label": "Exclusions",               "type": "textarea", "placeholder": "What is NOT considered confidential?"},
            {"key": "governing_law",  "label": "Governing Law",            "type": "text",     "placeholder": "e.g. Laws of India, Mumbai jurisdiction"},
        ],
        "prompt_template": """You are a legal document specialist.
Generate a professional Non-Disclosure Agreement (NDA):

Disclosing Party: {party_a}
Receiving Party: {party_b}
Purpose: {purpose}
Confidential Information: {conf_info}
Duration: {duration}
Exclusions: {exclusions}
Governing Law: {governing_law}

Generate a complete NDA with:
1. PARTIES
2. DEFINITION OF CONFIDENTIAL INFORMATION
3. OBLIGATIONS OF RECEIVING PARTY
4. EXCLUSIONS FROM CONFIDENTIAL INFORMATION
5. TERM AND TERMINATION
6. RETURN OF INFORMATION
7. NO LICENSE
8. REMEDIES
9. GOVERNING LAW
10. ENTIRE AGREEMENT
11. SIGNATURES

Use precise legal language. Number all clauses clearly."""
    },

    "Job Description": {
        "icon":        "💼",
        "description": "Professional job posting to attract the right candidates",
        "fields": [
            {"key": "company_name",   "label": "Company Name",          "type": "text",     "placeholder": "e.g. TechCorp India Pvt Ltd"},
            {"key": "job_title",      "label": "Job Title",             "type": "text",     "placeholder": "e.g. Senior AI Engineer"},
            {"key": "location",       "label": "Location",              "type": "text",     "placeholder": "e.g. Mumbai, Maharashtra (Hybrid)"},
            {"key": "overview",       "label": "Role Overview",         "type": "textarea", "placeholder": "Brief description of the role"},
            {"key": "responsibilities","label": "Key Responsibilities", "type": "textarea", "placeholder": "Main duties and responsibilities"},
            {"key": "requirements",   "label": "Requirements",          "type": "textarea", "placeholder": "Must-have skills and qualifications"},
            {"key": "nice_to_have",   "label": "Nice to Have",          "type": "textarea", "placeholder": "Preferred but not required skills"},
            {"key": "benefits",       "label": "Benefits & Perks",      "type": "textarea", "placeholder": "Salary, benefits, perks offered"},
            {"key": "culture",        "label": "Company Culture",       "type": "textarea", "placeholder": "What makes your company great?"},
        ],
        "prompt_template": """You are an HR specialist and talent acquisition expert.
Generate a compelling Job Description:

Company: {company_name}
Title: {job_title}
Location: {location}
Overview: {overview}
Responsibilities: {responsibilities}
Requirements: {requirements}
Nice to Have: {nice_to_have}
Benefits: {benefits}
Culture: {culture}

Generate a complete, attractive job description with:
1. JOB TITLE AND OVERVIEW
2. ABOUT THE COMPANY
3. WHAT YOU WILL DO (responsibilities as bullet points)
4. WHAT YOU NEED (requirements as bullet points)
5. BONUS POINTS (nice to have)
6. WHAT WE OFFER (benefits)
7. OUR CULTURE
8. HOW TO APPLY

Make it engaging and inclusive. Use action verbs."""
    },

    "Project Report": {
        "icon":        "📊",
        "description": "Status report for a project or initiative",
        "fields": [
            {"key": "project_name",   "label": "Project Name",          "type": "text",     "placeholder": "e.g. CloudSync Pro Launch"},
            {"key": "report_date",    "label": "Report Date",           "type": "text",     "placeholder": "e.g. June 2026"},
            {"key": "prepared_by",    "label": "Prepared By",           "type": "text",     "placeholder": "e.g. Nikhil Mulik, Project Manager"},
            {"key": "status",         "label": "Overall Status",        "type": "text",     "placeholder": "e.g. On Track / At Risk / Delayed"},
            {"key": "summary",        "label": "Executive Summary",     "type": "textarea", "placeholder": "Brief summary of project status"},
            {"key": "completed",      "label": "Completed Milestones",  "type": "textarea", "placeholder": "What has been accomplished?"},
            {"key": "in_progress",    "label": "In Progress",           "type": "textarea", "placeholder": "What is currently being worked on?"},
            {"key": "risks",          "label": "Risks & Issues",        "type": "textarea", "placeholder": "Current risks and mitigation plans"},
            {"key": "next_steps",     "label": "Next Steps",            "type": "textarea", "placeholder": "Upcoming milestones and actions"},
            {"key": "budget",         "label": "Budget Status",         "type": "text",     "placeholder": "e.g. Rs. 8,00,000 of Rs. 10,00,000 spent (80%)"},
        ],
        "prompt_template": """You are a professional project manager.
Generate a comprehensive Project Status Report:

Project: {project_name}
Date: {report_date}
Prepared By: {prepared_by}
Status: {status}
Summary: {summary}
Completed: {completed}
In Progress: {in_progress}
Risks: {risks}
Next Steps: {next_steps}
Budget: {budget}

Generate a complete project report with:
1. PROJECT OVERVIEW (name, date, status indicator)
2. EXECUTIVE SUMMARY
3. KEY METRICS (budget, timeline, scope)
4. ACCOMPLISHED THIS PERIOD
5. CURRENTLY IN PROGRESS
6. UPCOMING MILESTONES
7. RISKS AND ISSUES (with severity and mitigation)
8. BUDGET STATUS
9. RECOMMENDATIONS
10. NEXT STEPS AND ACTIONS

Be specific, professional, and structured."""
    },

    "Business Letter": {
        "icon":        "✉️",
        "description": "Formal business letter for any purpose",
        "fields": [
            {"key": "sender_name",    "label": "Sender Name",           "type": "text",     "placeholder": "e.g. Nikhil Mulik"},
            {"key": "sender_title",   "label": "Sender Title",          "type": "text",     "placeholder": "e.g. Managing Director, TechCorp"},
            {"key": "recipient_name", "label": "Recipient Name",        "type": "text",     "placeholder": "e.g. Mr. Amith Kumar"},
            {"key": "recipient_title","label": "Recipient Title",       "type": "text",     "placeholder": "e.g. CEO, Acme Corporation"},
            {"key": "subject",        "label": "Subject",               "type": "text",     "placeholder": "e.g. Partnership Proposal for Q3 2026"},
            {"key": "purpose",        "label": "Purpose of Letter",     "type": "text",     "placeholder": "e.g. proposal / complaint / request / announcement"},
            {"key": "main_content",   "label": "Main Points",           "type": "textarea", "placeholder": "Key points you want to communicate"},
            {"key": "call_to_action", "label": "Desired Action",        "type": "text",     "placeholder": "What do you want the recipient to do?"},
        ],
        "prompt_template": """You are a professional business writer.
Generate a formal Business Letter:

From: {sender_name}, {sender_title}
To: {recipient_name}, {recipient_title}
Subject: {subject}
Purpose: {purpose}
Main Content: {main_content}
Call to Action: {call_to_action}

Generate a complete, professional business letter with:
- Proper letterhead format
- Date
- Full recipient address block
- Formal salutation
- Introduction paragraph
- Main body (2-3 paragraphs covering all points)
- Conclusion with clear call to action
- Professional closing
- Signature block

Use formal business language. Be concise and clear."""
    },

    "Custom Document": {
        "icon":        "🔧",
        "description": "Describe any document and AI will generate it",
        "fields": [
            {"key": "doc_type",      "label": "Document Type",          "type": "text",     "placeholder": "e.g. Partnership Agreement, Policy Document, SOP"},
            {"key": "purpose",       "label": "Purpose",                "type": "textarea", "placeholder": "What is this document for?"},
            {"key": "parties",       "label": "Parties Involved",       "type": "text",     "placeholder": "Who are the parties or stakeholders?"},
            {"key": "key_points",    "label": "Key Points to Cover",    "type": "textarea", "placeholder": "What must be included?"},
            {"key": "tone",          "label": "Tone",                   "type": "text",     "placeholder": "e.g. formal legal / professional / friendly"},
            {"key": "length",        "label": "Approximate Length",     "type": "text",     "placeholder": "e.g. 1 page / 3-5 pages / comprehensive"},
        ],
        "prompt_template": """You are an expert document writer.
Generate a {doc_type} with these requirements:

Purpose: {purpose}
Parties: {parties}
Key Points: {key_points}
Tone: {tone}
Length: {length}

Generate a complete, professional {doc_type}.
Structure it appropriately for this document type.
Include all necessary sections, clauses, and professional formatting.
Use the specified tone throughout."""
    }
}


def get_document_types() -> list[str]:
    return list(DOCUMENT_TYPES.keys())


def get_template(doc_type: str) -> dict:
    return DOCUMENT_TYPES.get(doc_type, {})