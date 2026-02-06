def generate_template(template_type, parties, start_date, duration):
    if template_type == "Non-Disclosure Agreement (NDA)":
        return f"""NON-DISCLOSURE AGREEMENT

This Non-Disclosure Agreement ("Agreement") is entered into on {start_date} between:

DISCLOSING PARTY: {parties.get('party_a', '[Party A Name]')}
RECEIVING PARTY: {parties.get('party_b', '[Party B Name]')}

1. CONFIDENTIAL INFORMATION
The Receiving Party agrees to protect the confidential information of the Disclosing Party.

2. OBLIGATIONS
The Receiving Party shall not disclose, copy, or modify any Confidential Information without prior written consent.

3. TERM
This Agreement shall remain in effect for {duration} from the date of disclosure.

4. GOVERNING LAW
This Agreement shall be governed by the laws of India. Courts at New Delhi shall have exclusive jurisdiction.

IN WITNESS WHEREOF, the parties have executed this Agreement.
"""

    elif template_type == "Employment Agreement":
        return f"""EMPLOYMENT AGREEMENT

This Employment Agreement is made on {start_date} between:

EMPLOYER: {parties.get('party_a', '[Company Name]')}
EMPLOYEE: {parties.get('party_b', '[Employee Name]')}

1. POSITION
The Employee shall serve in the position of [Role] and report to the [Manager].

2. COMPENSATION
The Employee shall receive a monthly salary as per the Offer Letter.

3. PROBATION
The Employee shall be on probation for a period of 6 months.

4. TERMINATION
Either party may terminate this agreement with 30 days' notice.

5. GOVERNING LAW
Laws of India apply.
"""

    elif template_type == "Freelance/Service Agreement":
        return f"""SERVICE AGREEMENT

Date: {start_date}

CLIENT: {parties.get('party_a', '[Client Name]')}
PROVIDER: {parties.get('party_b', '[Provider Name]')}

1. SCOPE OF WORK
The Provider agrees to deliver the services described in the Statement of Work.

2. PAYMENT
The Client agrees to pay the fees within 15 days of invoice receipt.

3. INDEPENDENT CONTRACTOR
The Provider is an independent contractor, not an employee.

4. INTELLECTUAL PROPERTY
All work created shall be the property of the Client upon full payment.
"""

    else:
        return "Template not available."
