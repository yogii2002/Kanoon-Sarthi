import csv

def retrieve_matching_cases(search_term):
    prefix_length = len('https://w3id.org/def/NyOn#Case')
    if search_term.startswith('https://w3id.org/def/NyOn#Case'):
        search = search_term[prefix_length:]
    
    matching_case_ids = []
    matching_case_texts = []
    
    with open('file_Case_id_and_name.csv', 'r') as file_ids, open('case_files_53k.csv', 'r') as file_texts:
        reader_ids = csv.DictReader(file_ids)
        reader_texts = csv.DictReader(file_texts)
        
        for row_ids in reader_ids:
            if search in row_ids['Case_id']:
                matching_case_ids.append(row_ids['file_name'])
        for file_name in matching_case_ids:
            case_id=f"{file_name}"
        
        for row_texts in reader_texts:
            if case_id in row_texts['name']:
                matching_case_texts.append((row_texts['case_info'], row_texts['judgement']))
    
    return matching_case_texts
