from functions_file import *
import pandas as pd

from flask import Flask, request, jsonify, render_template, session, send_file

from io import BytesIO
#from flask_session import Session

# Generate report for one particular technician

# dataframe: pandas dataframe with all the ticketing data
# worker: name of the worker for whom we want to get a report
# size: length of number of tickets we want to include by worker

app = Flask(__name__)

#app.config['SESSION_TYPE'] = 'filesystem'
#Session(app)

@app.route('/')
def home():
    #session.clear()
    return render_template('index.html')

def get_all_unique_workers(dataframe):
    worker_list = dataframe[worker_name_header].tolist()
    unique_worker_list = list(set(worker_list))
    unique_worker_list.sort()
    return unique_worker_list

def get_report(dataframe, worker, size):
    
    worker_list, short_desc, inc_nums, work_notes, close_notes, priorities = get_lists(dataframe, worker, size)
    
    worker_name = [worker] * size

    report = pd.DataFrame(inc_nums, columns=['Incident Number'])
    report['Technician'] = worker_name

    # ticket_codes_exist: list where each element is yes/no depending on whether or not ticket codes 
    # were present
    # ticket_code: list where each element is the ticket code of the corresponding incident 

    ticket_codes_exist, ticket_code = get_ticket_codes(short_desc)
    
    report['Are ticket codes present?'] = ticket_codes_exist
    report['Ticket Codes'] = ticket_code

    # ticket_code_meaning: list where each element is what the ticket codes of the incident correspond to

    ticket_code_meaning = get_ticket_code_def(ticket_code)

    report['Ticket Code Meaning'] = ticket_code_meaning

    # notes exist is a list where each element is yes/no depending on whether or not the work notes
    # for the corresponding incidents are empty or not
    
    notes_exist = get_update(work_notes)

    report['Updates']=notes_exist

    # customer_contact_exists: a list where each element is yes/no/unsure depending on whether 
    # or not GPT thinks there was customer contact
    # customer_contact_rzn: GPT's reasoning behind its above answer

    customer_contact_exists, customer_contact_rzn = get_customer_contact(work_notes)

    report['Customer contact'] = customer_contact_exists
    report['Customer contact reasoning'] = customer_contact_rzn

    print('Customer contact \n')

    # troubleshooting: a list where each element is yes/no/unsure depending on whether 
    # or not GPT thinks the technician clearly included troubleshooting steps
    # troubleshooting_rzn: GPT's reasoning behind its above answer

    troubleshooting, troubleshooting_rzn = get_troubleshooting_steps(work_notes)

    report['Troubleshooting Steps'] = troubleshooting
    report['Troubleshooting Steps Reasoning'] = troubleshooting_rzn

    print('troubleshooting steps \n')

    # ts_results: a list where each element is yes/no/unsure depending on whether 
    # or not GPT thinks the technician clearly included the results of each troubleshooting step
    # ts_results_rzn: GPT's reasoning behind its above answer

    ts_results, ts_results_rzn = get_ts_results(work_notes)

    report['Troubleshooting Results'] = ts_results
    report['Troubleshooting Results Reasoning'] = ts_results_rzn

    print('troubleshooting results \n')

    # meaningful_updates: a list where each element is yes/no/unsure depending on whether 
    # or not GPT thinks the technician's work notes contained meaningful updates
    # meaningful_updates_rzn: GPT's reasoning behind its above answer

    meaningful_updates, meaningful_updates_rzn = get_meaningful_updates(work_notes)

    report['Meaningful Updates'] = meaningful_updates
    report['Meaningful Updates Reasoning'] = meaningful_updates_rzn

    print('meaningful updates \n')

    # timely_updates: a list where each element is yes/no/unsure depending on whether 
    # or not GPT thinks the technician's work notes contained timely updates
    # timely_updates_rzn: GPT's reasoning behind its above answer

    timely_updates, timely_updates_rzn = get_timely_updates(work_notes, priorities)

    report['Timely Updates'] = timely_updates
    report['Timely Updates Reasoning'] = timely_updates_rzn

    print('timely updates \n')

    # escalated: list where each element is yes/no depending on whether or not the incident was escalated
    # escalated_nums: list containing the index numbers of the columns of the incidents that were escalated

    escalated, escalated_nums = check_escalation(work_notes)
    
    report['Escalated'] = escalated

    # proper_esc: list where each element is N/A if the corresponding ticket was NOT escalated or mentions whether
    # or not the notes mentions who the ticket was escalated to if the ticket was escalated

    proper_esc = escalated_to_who(escalated_nums, work_notes)

    report['Escalated to who'] = proper_esc

    print('escalated to who \n')

    # proper_esc_notes_yn: list where each element is N/A if the corresponding ticket was NOT escalated
    # or is yes/no/unsure if the ticket was escalated based on whether or not GPT thinks the escalation notes
    # were clear 
    # proper_esc_notes: list where each element is N/A if the corresponding ticket was NOT escalated
    # or contains the reason for why GPT gave the above answer if the ticket was escalated
    
    proper_esc_notes_yn, proper_esc_notes = get_esc_notes(escalated_nums, work_notes)

    report['Proper Escalation Notes']=proper_esc_notes_yn
    report['Proper Escalation Notes Reasoning'] = proper_esc_notes

    print('proper esc notes \n')

    # close_notes_yn: list where each element is yes/no/unsure if the ticket was escalated based on 
    # whether or not GPT thinks the closure notes were clear 

    # closure_notes_rzn: list where each element is the reason for why GPT gave the above answer 

    close_notes_yn, close_notes_rzn = get_close_notes(close_notes)

    report['Close Notes'] = close_notes_yn
    report['Close Notes Reasoning'] = close_notes_rzn

    print('close notes \n')

    return report, work_notes, close_notes

@app.route('/getWorkers', methods=['GET'])
def get_workers():
    file = request.files['input_form']
    workers = get_all_unique_workers(file)  
    return {'workers': workers}

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        file = request.files['input_form']
        df = pd.read_excel(file)
        #session['df'] = df.to_dict()
        global data
        data = df
        unique_worker_list = get_all_unique_workers(df)
        return jsonify(unique_worker_list)
    except KeyError as err:
        error_message = 'Your input file is in the incorrect format! Please navigate to the instructions tab for more information!'
        return jsonify({'error': error_message})

@app.route('/generate', methods=['POST'])
def generate_report():
    #df = pd.DataFrame(session['df'])  # Retrieve dataframe from session
    df = data
    worker = request.form['worker_input']
    size = int(request.form['size_input'])
    report, work_notes, close_notes = get_report(df, worker, size)
    excel_file = BytesIO()
    report.to_excel(excel_file, index=False)
    excel_file.seek(0)
    return send_file(
        excel_file,
        download_name=f'{worker}_Report.xlsx',
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)