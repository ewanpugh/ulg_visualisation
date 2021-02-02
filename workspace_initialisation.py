import os

print('')
print('######################################################################')
print('######################## ULG Plot Generation #########################')
print('###################### Workspace Initialisation ######################')
print('######################################################################')
print('')

# Set working directory as parent of 'Working' folder
os.chdir('..')

folders_to_create = ['Archive', 'Plots', 'ULG Log Files']

for folder in folders_to_create:
    if folder not in os.listdir():
        os.mkdir(folder)
        print(f'Created {folder} folder')