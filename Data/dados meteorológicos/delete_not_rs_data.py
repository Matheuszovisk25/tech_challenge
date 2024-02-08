import os

folder_path = r'C:\Users\alexa\Documentos\Codes\FIAP\Pós Tech\Fase 1\Tech Challenge 1\Data\dados meteorológicos'

def is_wantted_file(file_name):
    for station in ["A801","A802","A803","A804","A805"]:
        if station in file_name:
            return True
    return False

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if not is_wantted_file(file) and file[-3:].lower() == 'csv':
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                print(f'deleted {file_path}')
                os.remove(file_path)