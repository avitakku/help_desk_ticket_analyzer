import time
import openai 
import config

openai.api_key = "ENTER_API_KEY_HERE"

# Set these based on the data set

worker_name_header = 'assigned_to'
short_desc_header = 'short_description'
inc_num_header = 'number'
work_notes_header = 'comments_and_work_notes'
close_notes_header = 'close_notes'
priorities_header = 'priority'

# Creating ticket codes dictionary

ticket_codes = {'AD-001':'Password resets',
'AD-002':'Shared Access Request',
'AD-003I':'Account Locked - Inactivity',
'AD-003S': 'Account locked - Failure to complete security training',
'AD-003':'Account unlock',
'AD-003U':'Unexplained Account Lockout',
'AD-004':'Shared Drives Connectivity',
'AD-005':'Active Directory information update',
'AD-005T':'Account Deactivated due to Training',
'AD-006':'New User - Account Only',
'AD-007':'Local Admin Request',
'AD-008':'Domain Not Specified due to ctrl-alt-del',
'AD-009':'Request for Account Termination',
'AD-009R':'Request for Account Reactivation',
'AD-009L':'Request for Longterm Leave',
'AD-010':'Request for Secondary Account',
'AV-001':'Speaker Request',
'AV-002':'Audio Troubleshooting',
'AV-003':'Webcam Request',
'AV-004':'Conference Room Support',
'AV-005':'Webcam Troubleshooting',
'AV-006':'Headset Request',
'K-001':'Keyboard troubleshooting \ replace',
'K-002':'Keyboard request (Special Order)',
'L-001F':'Laptop Request - New User (Fed)',
'L-001C':'Laptop Request - New User (Contractor)',
'L-001S':'Laptop Request - New User (Student)',
'L-002':'Laptop Replacement - Scheduled',
'L-003':'Laptop Replacement - Work Stoppage',
'L-004':'Laptop Reimage - Scheduled',
'L-005':'Laptop Hardware troubleshooting',
'L-005B':'Laptop Battery issue',
'L-005D':'Laptop Hardware with Dell Service',
'L-005U':'User damaged laptop',
'L-005R':'Laptop BIOS Reset',
'L-005T':'Laptop BIOS settings change',
'L-005W':'Disabled Wireless Adapter',
'L-006':'Laptop Reimage - Workstoppage',
'L-007':'Loaner Laptop/Projector Request',
'L-007I':'International Loaner',
'L-008':'COOP Secondary Laptop Request',
'L-009':'Laptop Accessories',
'L-009D':'Docking Station Install',
'L-010':'Laptop Health Check',
'L-011':'Laptop deployment - Secondary',
'L-012':'Laptop deployment - Not user assigned',
'L-013':'Computer dropped from Domain',
'L-014':'New User First Login Support',
'L-015':'Laptop External devices access',
'L-016':'Laptop Screen Damage',
'L-017':'Laptop Lost/Stolen',
'M-001':'Monitor  Request',
'M-002':'Monitor troubleshooting', 
'M-003':'Second Monitor Request',
'MS-001':'Mouse troubleshooting \ replace',
'MS-002':'Mouse request',
'N-001':'Network Connectivity Troubleshoot',
'N-001A':'AnyConnect/ISE Upgrade Issues',
'N-001N':'NAC issues',
'N-001V':'VPN Access',
'N-001R':'Remote RDP Access',
'N-001O':'Wired Connection Access',
'N-001W':'Network Connectivity - HRSA WiFi',
'N-002':'Lan Port activation',
'N-003':'Network drive mapping',
'N-004':'Data Recovery',
'N-005':'Cannot Log to system',
'PIV-001':'PIV Card Roll back',
'PIV-001E':'PIV Card Roll back Extended',
'PIV-002':'PIV Card troubleshoot',
'PIV-003':'PIV Card Certificate Updates',
'PIV-004':'PIV Card reader troubleshoot',
'PIV-005':'PIV Card Blocked',
'TW-001':'4G Activation',
'TW-002':'Mobile Device Request \ Delivery',
'TW-003':'Mobile Device Troubleshooting',
'TW-004':'International Devices Request',
'TW-005D':'Avaya Desk Phone Troubleshooting/Install',
'TW-005S':'Avaya Software Troubleshooting/Install',
'TW-006':'Headset Troubleshoot',
'HHH-001':'Humphrey Building  troubleshooting',
'ESC-001':'Ticket Escalation Code',
'WS-911':'Work Stoppage',
'NOB-001':'Assigned to NOB/DIS',
'MV-001':'Hardware Moves',
'P-001':'Printer Mapping - Network/Desktop',
'P-002':'Printer Desktop -Install',
'P-003':'Printer Network- Install',
'P-004':'Printer Troubleshooting',
'P-004S':'SecurePrint',
'P-005':'HP Toner',
'P-006':'Ricoh MFD Troubleshoot/Jam',
'P-007':'Ricoh toner',
'P-008':'Ricoh Service Call required',
'P-009':'Home Printer install assist',
'P-010':'Printer Move',
'SC-001':'Scanner Request',
'SC-002':'Scanner Troubleshooting',
'SW-001':'Basic Software troubleshooting',
'SW-001A':'BlackBerry AtHoc (Failed to create file)',
'SW-001G':'Sentry Gatekeeper',
'SW-001S':'SharePoint troubleshooting',
'SW-001E':'ePMAP Troubleshooting',
'SW-002':'Software installation request',
'SW-003':'ActiveClient Issues',
'SW-004':'AnyConnect Issues',
'SW-005':'Bitlocker key tickets',
'SW-006':'Bitlock external HD',
'SW-007':'Web based applications',
'SW-008':'Bitlocker Fix (OIT generated ticket)',
'SW-009':'Outlook Troubleshooting',
'SW-009C':'Outlook Connectivty Issues',
'SW-010':'Skype Troubleshooting',
'SW-010L':'Skype login issues',
'SW-011':'Symantec Troubleshooting',
'SW-012':'Non-Standard SW troubleshooting',
'SW-013':'Non-Standard SW Installation',
'SW-014':'Windows OS issues',
'SW-014S':'Slow Windows Startup/Login',
'SW-014UM':'Windows 10 20H2 upgrade - Manual',
'SW-014U':'Windows 10 20H2 upgrade',
'SW-014P':'Windows Temp Profile issue',
'SW-015T':'Teams Troubleshooting',
'SW-015A':'Teams Audio Issues',
'SW-015Q':'Teams How To/Question',
'SW-015S':'Teams Request for new Team site',
'SW-015P':'MS Teams Presence',
'SW-015I':'Teams desktop client install',
'SW-016':'Power BI',
'SW-017':'OneDrive Issues',
'SW-018':'MS Word Troubleshooting',
'SW-019':'Adobe Troubleshooting',
'SW-020':'Tableau install',
'SW-021':'Seft Request',
'SW-022':'SAS Request',
'SW-023':'SPSS Request',
'PR-001':'Laptop Refresh',
'PR-001B':'Contractor Refresh 2021',
'PR-001A':'Laptop Refresh Customer Callback',
'PR-003':'Group SW Deployment (i.e. Training Rooms)',
'PR-004':'Monitor Refresh',
'PR-005':'Laptop Receipt Ticket',
'PR-006':'Windows 10 Project',
'PR-007':'VIP Zoom Plugin Check',
'VR-001':'Virus/Malware scan',
'VR-002':'Reimage due to Virus/Malware',
'VR-003':'Lost/Stolen Laptop',
'VR-004':'Lost/Stolen mobile phone',
'VR-005':'Customer Phishing Report/PhishMe',
'VR-006':'Vulnerability Remediation',
'VR-007':'Encrypted drives',
'TB-001':'Tablets install',
'TB-002':'Tablets troubleshoot',
'AC-001':'Adobe Connect',
'Z-001':'Zoom',
'T-001':'Teams Conferrence Support',
'TR-001':'Individual Training',
'D-000':'Disregard Ticket',
'NS-001':'Non-Supported Item',
'RA-001':'Reasonable Accommodation',
'ESR-001':'Telecom Supply Request',
'GR-001':'Graphic Request - Poster',
'NIH-001':'Discuss with NIH',
'GR-002':'Graphic Request - Banner',
'R-001':'Return Receipt',
'CC-002':'Off Boarding',
'0-001A':'Other (Automatically Routed)',
'0-001D':'Other (NIH technician Routed ticket to us)',
'BO-001':'Onsite Badging Office incidents',
'MP-001':'Manual patching',
'~SD':'NIH Service Desk Error',
'[7420]':'Dell 7420 Hardware Issues',
'NR-001':'Non Responsive Customer 3x tries',
'OHR-001':'Install OHR scanner',
'MISS-001':'Missing Peripherals from desk',
'BG-001':'Badging Office Incidents',
'M365-001M':'Office 356 Migration Issues',
'ODM-001':'OneDrive Migration Issues',
'USB-001H':'Issue USB 4-Port Hub',
'ENC-001':'Encryption Issue',
'EHB-001':'EHB Support',
'LLR-001':'Loaner Laptop Retrival',
'21H2-002':'21H2 Deployment Issue',
'PIV-21H2':'21H2 Deployment Issue PIV issues',
'21H2-001V':'21H2 VIP Manual Deployment',
'21H2-001':'21H2 Manual Deployment',
'AC-001':'ActiveClient issue',
'IE-001':'IE11 Uninstall/Disable'}

# Getting ticket codes

# short_desc corresponds to the column in your database where technician is supposed to note down ticket code

def get_ticket_codes(short_desc):
    
    ticket_codes_exist = []
    ticket_code = []
    
    for i in short_desc:
        
        words=i.split()
        ticket_code_present = False
        ticket = ''
        
        # ticket_codes is a prebuilt dictionary containing all the ticket codes and what they mean 
        
        for word in words:
            if word in ticket_codes:
                ticket_code_present = True
                ticket=ticket+' '+word
        
        if ticket_code_present==True:
            ticket_codes_exist.append('Yes')
        
        elif ticket_code_present==False:
            ticket_codes_exist.append('No')
        ticket_code.append(ticket)
    return ticket_codes_exist, ticket_code

# ticket_codes_exist: list where each element is yes/no depending on whether or not ticket codes were present
# ticket_code: list where each element is the ticket code of the corresponding incident 

# ticket_codes is a list containing the ticket code(s) of each incident  

def get_ticket_code_def(ticket_code_list):
    ticket_code_meaning = []
    for codes in ticket_code_list:
        codes = codes.split()
        meaning = ''
        for code in codes:
            if code in ticket_codes:
                #print(code)
                if meaning == '':
                    meaning= ticket_codes[code]
                else:
                    meaning = meaning + ', ' + ticket_codes[code]
                #print(meaning)
        ticket_code_meaning.append(meaning)
    return ticket_code_meaning

# ticket_code_meaning: list where each element is what the ticket codes of the incident correspond to

#########################################

# Checking if work notes have content

# work_notes is a list where each element is the work notes of the corresponding incident 

def get_update(work_notes):
    notes_exist = []
    for notes in work_notes:
        if(not(notes and notes.strip())):
            notes_exist.append('No')
        else:
            notes_exist.append('Yes')
    return notes_exist

# notes exist is a list where each element is yes/no depending on whether or not the work notes
# for the corresponding incidents are empty or not

##########################################

# Checking if there was contact w the customer 

# work_notes is a list where each element is the work notes of the corresponding incident 

def get_customer_contact(work_notes):
    customer_contact_exists = []
    customer_contact_rzn = []
    for note in work_notes:  
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant to a service desk ticket report analyzer. Carefully analyze the service desk ticket notes provided to you and answer all the questions asked to you in a detailed and specific manner."},
                        {"role": "user", "content": f"Ticket notes: {note}\n ====== \n According to these notes, has there been contact between the technician and the customer? Ensure the first word of your response is 'Yes', 'No', or 'Unsure', and then in around 15 words elaborate on your reasoning."}
                    ],
                    temperature=0.4
                )
                customer_contact = response['choices'][0]['message']['content']
                #print(customer_contact)
                
                # Break the loop if the code executes without encountering an exception
                break
                
            except Exception as e:
                # In case of API error, return the error message
                e = str(e)
                output = "There was an error! Here is the message: " + e
                print(output)
                # Retry after a delay (e.g., 1 second)
                time.sleep(1)

        y_n = ''.join(filter(str.isalnum, customer_contact.split()[0]))
        customer_contact_exists.append(y_n)
        customer_contact_rzn.append(customer_contact)
    return customer_contact_exists, customer_contact_rzn

# customer_contact_exists: a list where each element is yes/no/unsure depending on whether 
# or not GPT thinks there was customer contact
# customer_contact_rzn: GPT's reasoning behind its above answer

#####################################################

# Checking whether technician adequately documented troubleshooting steps

# work_notes is a list where each element is the work notes of the corresponding incident 

def get_troubleshooting_steps(work_notes):
    troubleshooting = []
    troubleshooting_rzn = []
    for note in work_notes:  
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant to a service desk ticket report analyzer. Carefully analyze the service desk ticket notes provided to you and answer all the questions asked to you in a detailed and specific manner."},
                        {"role": "user", "content": f"Ticket notes: {note}\n ====== \n According to these notes, did the technician document the steps they took to identify the root cause / source of the incident/issue? Ensure the first word of your response is 'Yes', 'No', or 'Unsure', and then in around 15 words elaborate on your reasoning."}
                    ],
                    temperature=0.4
                )
                trouble_shooting = response['choices'][0]['message']['content']
                #print(customer_contact)
                
                # Break the loop if the code executes without encountering an exception
                break
                
            except Exception as e:
                # In case of API error, return the error message
                e = str(e)
                output = "There was an error! Here is the message: " + e
                print(output)
                # Retry after a delay (e.g., 1 second)
                time.sleep(1)

        y_n = ''.join(filter(str.isalnum, trouble_shooting.split()[0]))
        troubleshooting.append(y_n)
        troubleshooting_rzn.append(trouble_shooting)
    return troubleshooting, troubleshooting_rzn

# troubleshooting: a list where each element is yes/no/unsure depending on whether 
# or not GPT thinks the technician clearly included troubleshooting steps
# troubleshooting_rzn: GPT's reasoning behind its above answer

#################################################

# Checking whether technician clearly notes the results of each troubleshooting step

# work_notes is a list where each element is the work notes of the corresponding incident 

def get_ts_results(work_notes):
    ts_results = []
    ts_results_rzn = []
    for note in work_notes:  
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant to a service desk ticket report analyzer. Carefully analyze the service desk ticket notes provided to you and answer all the questions asked to you in a detailed and specific manner."},
                        {"role": "user", "content": f"Ticket notes: {note}\n ====== \n According to these notes, if the technician documented the steps they took to identify the root cause / source of the incident/issue, did they capture what happened as a result of each step? Ensure the first word of your response is 'Yes', 'No', or 'Unsure', and then in around 15 words elaborate on your reasoning."}
                    ],
                    temperature=0.4
                )
                ts = response['choices'][0]['message']['content']
                #print(customer_contact)
                
                # Break the loop if the code executes without encountering an exception
                break
                
            except Exception as e:
                # In case of API error, return the error message
                e = str(e)
                output = "There was an error! Here is the message: " + e
                print(output)
                # Retry after a delay (e.g., 1 second)
                time.sleep(1)

        y_n = ''.join(filter(str.isalnum, ts.split()[0]))
        ts_results.append(y_n)
        ts_results_rzn.append(ts)
    return ts_results, ts_results_rzn

# ts_results: a list where each element is yes/no/unsure depending on whether 
# or not GPT thinks the technician clearly included the results of each troubleshooting step
# ts_results_rzn: GPT's reasoning behind its above answer

#######################################################

# Checking whether the technicians notes contain meaningful updates

# work_notes is a list where each element is the work notes of the corresponding incident 

def get_meaningful_updates(work_notes):
    meaningful_updates = []
    meaningful_updates_rzn = []
    for note in work_notes:  
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant to a service desk ticket report analyzer. Carefully analyze the service desk ticket notes provided to you and answer all the questions asked to you in a detailed and specific manner."},
                        {"role": "user", "content": f"Ticket notes: {note}\n ====== \n Do these notes contain meaningful updates? According to these notes, can someone else figure out what happened and what is going on?  Ensure the first word of your response is 'Yes', 'No', or 'Unsure', and then in around 15 words elaborate on your reasoning."}
                    ],
                    temperature=0
                )
                mu = response['choices'][0]['message']['content']
                
                # Break the loop if the code executes without encountering an exception
                break
                
            except Exception as e:
                # In case of API error, return the error message
                e = str(e)
                output = "There was an error! Here is the message: " + e
                print(output)
                # Retry after a delay (e.g., 1 second)
                time.sleep(1)

        y_n = ''.join(filter(str.isalnum, mu.split()[0]))
        meaningful_updates.append(y_n)
        meaningful_updates_rzn.append(mu)
    return meaningful_updates, meaningful_updates_rzn

# meaningful_updates: a list where each element is yes/no/unsure depending on whether 
# or not GPT thinks the technician's work notes contained meaningful updates
# meaningful_updates_rzn: GPT's reasoning behind its above answer

#####################################################################

# Determining whether the technician's updates were timely based on the priority of the incident

# work_notes is a list where each element is the work notes of the corresponding incident 
# priorities is a list where each element is the priority of the corresponding incident 

def get_timely_updates(work_notes, priorities):
    timely_updates = []
    timely_updates_rzn = []
    for i in range(len(work_notes)):
        note = work_notes[i]
        priority = priorities[i]
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant to a service desk ticket report analyzer. Carefully analyze the service desk ticket notes provided to you and answer all the questions asked to you in a detailed and specific manner."},
                        {"role": "user", "content": f"Ticket notes: {note}\n ====== \n Priority: {priority}\n ====== \n Tech's are supposed to work on new tickets within 1 business day. If there is contact between the technician and the customer, then, if the ticket priority is critical/high, the tech is supposed to respond within an hour, if it is medium, within 1 business day, and if it is low, within a couple business days. According to this note, were there timely updates by the technician? Ensure the first word of your response is 'Yes', 'No', or 'Unsure', and then in around 15 words elaborate on your reasoning."}
                    ],
                    temperature=0.1
                )
                customer_contact = response['choices'][0]['message']['content']
                #print(customer_contact)
                
                # Break the loop if the code executes without encountering an exception
                break
                
            except Exception as e:
                # In case of API error, return the error message
                e = str(e)
                output = "There was an error! Here is the message: " + e
                print(output)
                # Retry after a delay (e.g., 1 second)
                time.sleep(1)

        y_n = ''.join(filter(str.isalnum, customer_contact.split()[0]))
        timely_updates.append(y_n)
        timely_updates_rzn.append(customer_contact)

    return timely_updates, timely_updates_rzn

# timely_updates: a list where each element is yes/no/unsure depending on whether 
# or not GPT thinks the technician's work notes contained timely updates
# timely_updates_rzn: GPT's reasoning behind its above answer

######################################################

# Checking which incidents were escalated

# ticket_code is a list of ticket code generated from get_ticket_codes() function defined above

def check_escalation(ticket_code):
    escalated = []
    escalated_nums = []
    for i in range(len(ticket_code)):
        codes = ticket_code[i]
        esc = False
        for code in codes.split():
            if code == 'ESC-001':
                esc = True
                escalated_nums.append(i)
        if esc == True:
            escalated.append('Yes')
        else:
            escalated.append('No')
    return escalated, escalated_nums

# escalated: list where each element is yes/no depending on whether or not the incident was escalated
# escalated_nums: list containing the index numbers of the columns of the incidents that were escalated

########################################################

# Checking whether the ticket notes of escalated incidents mention to whom the escalated incidents were escalated

# escalated_nums: list containing the index numbers of the columns of the incidents that were escalated
# obtained from function check_escalation()

# work_notes is a list where each element is the work notes of the corresponding incident 

def escalated_to_who(escalated_nums, work_notes):
    proper_esc = []
    for i in range(len(work_notes)):
        if i in escalated_nums:
            note = work_notes[i]
            while True:
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo-16k",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant to a service desk ticket report analyzer. Carefully analyze the service desk ticket notes provided to you and answer all the questions asked to you in a detailed and specific manner."},
                            {"role": "user", "content": f"Ticket notes: {note}\n ====== \n It has been noted that this ticket is being escalated to another technician. Do the work notes mention to which person or department it is being escalated to for assistance?"}
                        ],
                        temperature=0.4
                    )
                    customer_contact = response['choices'][0]['message']['content']
                    #print(customer_contact)
                    
                    # Break the loop if the code executes without encountering an exception
                    break
                    
                except Exception as e:
                    # In case of API error, return the error message
                    e = str(e)
                    output = "There was an error! Here is the message: " + e
                    print(output)
                    # Retry after a delay (e.g., 1 second)
                    time.sleep(1) 
            proper_esc.append(customer_contact)  
        else:
            proper_esc.append('N/A')
    return proper_esc

# proper_esc: list where each element is N/A if the corresponding ticket was NOT escalated or mentions whether
# or not the notes mentions who the ticket was escalated to if the ticket was escalated

######################################################

# Checking if the ticket notes for the escalated tickets contain appropriate escalation notes 

# escalated_nums: list containing the index numbers of the columns of the incidents that were escalated
# obtained from function check_escalation()

# work_notes is a list where each element is the work notes of the corresponding incident 

def get_esc_notes(escalated_nums, work_notes):

    proper_esc_notes = []
    proper_esc_notes_yn = []
    for i in range(len(work_notes)):
        if i in escalated_nums:
            note = work_notes[i]
            while True:
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo-16k",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant to a service desk ticket report analyzer. Carefully analyze the service desk ticket notes provided to you and answer all the questions asked to you in a detailed and specific manner."},
                            {"role": "user", "content": f"Ticket notes: {note}\n ====== \n It has been noted that this ticket is being escalated to another technician. Do the work notes have a good explanation of why it's being escalated? The next level tech should be able to take it forward and not have to re-work. There should be clear direction on what has happened and what is needed. Ensure the first word of your response is 'Yes', 'No', or 'Unsure', and then in around 15 words elaborate on your reasoning."}
                        ],
                        temperature=0.3
                    )
                    customer_contact = response['choices'][0]['message']['content']
                    #print(customer_contact)
                    
                    # Break the loop if the code executes without encountering an exception
                    break
                    
                except Exception as e:
                    # In case of API error, return the error message
                    e = str(e)
                    output = "There was an error! Here is the message: " + e
                    print(output)
                    # Retry after a delay (e.g., 1 second)
                    time.sleep(1) 
            proper_esc_notes.append(customer_contact)  
            y_n = ''.join(filter(str.isalnum, customer_contact.split()[0]))
            proper_esc_notes_yn.append(y_n)
            print(y_n)
        else:
            proper_esc_notes.append('N/A')
            proper_esc_notes_yn.append('N/A')
    
    return proper_esc_notes_yn, proper_esc_notes

# proper_esc_notes_yn: list where each element is N/A if the corresponding ticket was NOT escalated
# or is yes/no/unsure if the ticket was escalated based on whether or not GPT thinks the escalation notes
# were clear 

# proper_esc_notes: list where each element is N/A if the corresponding ticket was NOT escalated
# or contains the reason for why GPT gave the above answer if the ticket was escalated

###################################################

# Determining whether the closure notes were appropriate

# close_notes is a list where each element is the closure notes of the corresponding incident 

def get_close_notes(close_notes):
    close_notes_yn = []
    close_notes_rzn = []
    for i in range(len(close_notes)):
        note = close_notes[i]
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant to a service desk ticket report analyzer. Carefully analyze the service desk ticket notes provided to you and answer all the questions asked to you in a detailed and specific manner."},
                        {"role": "user", "content": f"Ticket notes: {note}\n ====== \n These are the close notes of the ticket. Would someone unfamiliar with the incident be able to determine what happened and how it was resolved based on the notes? Ensure the first word of your response is 'Yes', 'No', or 'Unsure', and then in around 15 words elaborate on your reasoning."}
                    ],
                    temperature=0
                )
                customer_contact = response['choices'][0]['message']['content']
                #print(customer_contact)
                
                # Break the loop if the code executes without encountering an exception
                break
                
            except Exception as e:
                # In case of API error, return the error message
                e = str(e)
                output = "There was an error! Here is the message: " + e
                print(output)
                # Retry after a delay (e.g., 1 second)
                time.sleep(1)

        y_n = ''.join(filter(str.isalnum, customer_contact.split()[0]))
        close_notes_yn.append(y_n)
        close_notes_rzn.append(customer_contact)
    return close_notes_yn, close_notes_rzn

# close_notes_yn: list where each element is yes/no/unsure if the ticket was escalated based on 
# whether or not GPT thinks the closure notes were clear 
# closure_notes_rzn: list where each element is the reason for why GPT gave the above answer 

#######################################################

# Getting the indices of worker so that we can call other functions

# worker_list is a list containing the names of the workers from the dataset
# worker is a string that is the name of the specific worker

def get_worker_indices(worker_list, worker):
    indices = []
    for i in range(len(worker_list)):
        if worker_list[i]==worker:
            indices.append(i)
    return indices

# indices is a list containing the indices of the tickets done by that particular worker

#############################################################

# Getting all the lists used to generate final report for one particular worker

# dataframe: pandas dataframe with all the ticketing data
# worker: name of the worker for whom we want to get a report
# size: length of number of tickets we want to include by worker

def get_lists(dataframe, worker, size):

    worker_list = dataframe[worker_name_header].tolist()
    short_desc = dataframe[short_desc_header].tolist()
    inc_nums = dataframe[inc_num_header].tolist()
    work_notes = dataframe[work_notes_header].tolist()
    close_notes = dataframe[close_notes_header].tolist()
    priorities = dataframe[priorities_header].tolist()

    test_worker_list = []
    test_short_desc = []
    test_inc_nums = []
    test_work_notes = []
    test_close_notes = []
    test_priorities = []

    worker_indices = get_worker_indices(worker_list, worker)
    test_set = worker_indices[:size]

    for i in test_set:
        test_worker_list.append(worker_list[i])
        test_short_desc.append(short_desc[i])
        test_inc_nums.append(inc_nums[i])
        test_work_notes.append(work_notes[i])
        test_close_notes.append(close_notes[i])
        test_priorities.append(priorities[i])

    return test_worker_list, test_short_desc, test_inc_nums, test_work_notes, test_close_notes, test_priorities
