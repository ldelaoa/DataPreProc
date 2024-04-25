import csv
import shutil
import os

# Define your source folder and destination folders
root = "//zkh/appdata/RTDicom/Projectline_modelling_lung_cancer/Users/Luis/"
source_folder = root+"CT_ITV_GTV_XBP_NII_Processed/"
tranining_folder = root+"CT_ITV_GTV_XBP_NII_Processed_Select/Training"
test_folder = root+"CT_ITV_GTV_XBP_NII_Processed_Select/Test"

# Read the CSV file
with open(root+'ListsOfPatients/TrainAndTest_FullList.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  
    for row in reader:
        id, to_folder_train, to_folder_test = row
        currSourceFolder = os.path.join(source_folder,id)        
        if to_folder_train.lower() == 'true':
            print("To Train")
            currDestFolder  = os.path.join(tranining_folder, id)
            if not(os.path.exists(currDestFolder)):
                shutil.copytree(currSourceFolder,currDestFolder)
        elif to_folder_test.lower() == 'true':
            print("ToTest")
            currDestFolder  = os.path.join(test_folder, id)
            if not(os.path.exists(currDestFolder)):
                shutil.copytree(currSourceFolder,currDestFolder)
        else:
            print("NotUsed")
print("done")
