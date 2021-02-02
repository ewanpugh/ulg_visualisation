import os

print('')
print('######################################################################')
print('######################## ULG Plot Generation #########################')
print('###################### Workspace Initialisation ######################')
print('######################################################################')
print('')

# Set working directory as parent of 'Working' folder
os.chdir(os.path.dirname(os.path.dirname( __file__ )))

folders_to_create = ['Archive', 'Plots', 'ULG Log Files']

for folder in folders_to_create:
    if folder not in os.listdir():
        os.mkdir(folder)
        print(f'Created {folder} folder')
print('')

install_check = input('''WARNING! Required packages will now be installed using pip. 
Press enter to install otherwise type NO to exit: ''')
        
if install_check.upper() != 'NO':
    os.system('pip install -r Working/requirements.txt')