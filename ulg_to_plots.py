import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
import shutil
import sys
import math
from datetime import datetime

# Set working directory as parent of 'Working' folder
#os.chdir('..')
#sys.path.append(os.getcwd())
from plot_definitions import configuration


##############################################################################
######################## PLOT CONFIGURATION PARAMETERS #######################
##############################################################################
analogue_boolean_ratio = 3 # analogue size is 3x height of boolean
bool_height = 40 # height of boolean plot
top_margin = 50 # height of margin at top of page

##############################################################################
################################ COLOUR PALETTE ##############################
##############################################################################
colour_list = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
]

##############################################################################
################################## FUNCTIONS #################################
##############################################################################
def rad_to_deg(rad):
    return math.degrees(rad)

##############################################################################
################################# MAIN SCRIPT ################################
##############################################################################
print('')
print('######################################################################')
print('######################## ULG Plot Generation #########################')
print('######################################################################')
print('')
print(f'Current directory {os.getcwd()}')
print('')
########################### Directory configuration ##########################

if 'ULG Log Files' not in os.listdir():
    os.mkdir('ULG Log Files')

if 'Plots' not in os.listdir():
    os.mkdir('Plots')
    print('Plots folder not present, made one')
    
if 'Archive' not in os.listdir():
    os.mkdir('Archive')
    print('Archive folder not present, made one')
    
ulg_files = [x for x in os.listdir('ULG Log Files') if x.endswith('.ulg')]
if len(ulg_files) > 0:
    print(f'{len(ulg_files)} log files found!')
    for file in ulg_files:
        print(f'\t{file}')
else:
    sys.exit('No log files found! Killing execution')

######################## Find ULG files, extract CSV's #######################

ulg_config = []
for file in ulg_files:
    overwrite_check = ''
    if file[:-4] in os.listdir('Plots'):
        overwrite_check = input(f'WARNING! Plots for file named "{file}"already exist. Press enter to override otherwise type NO and rename ulg file: ')
        
    if overwrite_check.upper() != 'NO':
        current_date = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
        archive_folder = f'{file[:-4]}_{current_date}'
        os.mkdir(f'Archive/{archive_folder}')
        csv_dir = f'Archive/{archive_folder}/CSVs'
        os.mkdir(csv_dir)
        plot_dir = f'Plots/{file[:-4]}'
        if file[:-4] in os.listdir('Plots'):
            shutil.rmtree(plot_dir)
        os.mkdir(plot_dir)
        plot_archive_dir = f'Archive/{archive_folder}/Plots'
        os.mkdir(plot_archive_dir)
        shutil.copy(f'ULG Log Files/{file}',f'Archive/{archive_folder}/{file}')
        command = f'ulog2csv "ULG Log Files/{file}" -o "{csv_dir}'
        ulg_config.append(
            {'file':file, 'csv_dir':csv_dir, 'command':command,
             'archive_folder':archive_folder,
             'plot_archive_dir':plot_archive_dir, 'plot_dir':plot_dir}
            )
    

print('\nExtracting CSV data...')
for config in ulg_config:
    print(f'\tExtracting {config["file"]}...')
    os.system(config['command'])
    print(f'\tExtracted {config["file"]}!')
    
################################ Create plots ################################

print('\nCreating plots....')
for config in ulg_config:
    print(f'\tCreating plots for {config["file"]}....')
    directory = config['csv_dir']
    file_prefix = f'{config["file"][:-4]}'
    for page in configuration:
        df = None
        fig = None
        params_to_plot = page['params_to_plot']
        colours = colour_list
        while len(colours) < len(params_to_plot):
            colours += colours
        for definition in page['parameter_paths']:
            # Extract data from csv's into dataframe
            fname = f'{file_prefix}_{definition["file"]}.csv'
            parameter = definition['parameter']
            try:
                temp_df = pd.read_csv(f'{directory}/{fname}',
                                      usecols = ['timestamp', parameter])
                            
                if 'rename' in definition.keys():
                    temp_df = temp_df.rename(columns={parameter : 
                                                      definition['rename']})
                
                if df is None:
                    df = temp_df
                else:
                    df = df.merge(temp_df, left_on = 'timestamp',
                                  right_on = 'timestamp',
                                  how = 'outer')
            except FileNotFoundError:
                print(f'\t\tError! File not found: {fname}')
            except ValueError:
                print(f'\t\tError! Column {parameter} not in {fname}')
            except:
                print(f'\t\tError! Error obtaining {parameter} from {fname}')
    
        # Format dataframe        
        for col in df.columns:
            df[col] = pd.to_numeric(df[col])
        
        df.timestamp = df.timestamp/1000000
        
        df = df.sort_values(by=['timestamp'])
        df = df.interpolate()
        df = df.reset_index(drop=True)
        
        if 'nav_state' in df.columns:
            df['Offboard'] = df['nav_state'] == 14
            df['Offboard'] = df['Offboard'].astype(int)
        if 'arming_state' in df.columns:
            df['Armed'] = df['arming_state'] == 2
            df['Armed'] = df['Armed'].astype(int)
        if 'Altitude' in df.columns:
            df['Altitude (m)'] = df['Altitude (m)']*(-1)
        for col in ['Pitch', 'Roll', 'Yaw']:
            if col in df.columns:
                df[col] = df[col].apply(rad_to_deg)
        
        axis_list = [x['axis'] for x in params_to_plot]
        unique_axis_list = []
        for axis in axis_list:
            if axis not in unique_axis_list:
                unique_axis_list.append(axis)
        
        boolean_count = 0
        analogue_count = 0
        for axis in unique_axis_list:
            param_type_for_axis = [x['type'] for x in params_to_plot
                                   if x['axis'] == axis]
            if 'analogue' in param_type_for_axis:
                analogue_count +=1
            else:
                boolean_count += 1
        unit_size = round(1/(boolean_count + 
                             (analogue_boolean_ratio*analogue_count)), 2)
        
        row_heights = []
        axis_types = []
        for axis in unique_axis_list:
            param_type_for_axis = [x['type'] for x in params_to_plot
                                   if x['axis'] == axis]
            if 'analogue' in param_type_for_axis:
                axis_types.append({'axis': axis, 'type': 'analogue'})
                row_heights.append(analogue_boolean_ratio*unit_size)
            else:
                row_heights.append(unit_size)
                axis_types.append({'axis': axis, 'type': 'boolean'})
        

       
        if page['page'] == 'Flight Path':
            df['Local Z'] = df['Local Z']*-1
            fig = px.scatter_3d(df, x='Local X', y='Local Y', z='Local Z',
                    color='timestamp')
        else:
            fig = make_subplots(rows = len(unique_axis_list),
                    cols = 1,
                    shared_xaxes = True,
                    row_heights  = row_heights,
                    vertical_spacing = 0.02,
                    )
            for param in params_to_plot:
                colour = colours[params_to_plot.index(param)]
                axis = param['axis']
                parameter = param['parameter']
                if parameter in df.columns:
                    fig.add_trace(
                        go.Scatter(
                            x = df.timestamp,
                            y = df[parameter],
                            name = parameter.replace('_',' '),
                            line = {'color':colour}
                            ),
                        row = axis,
                        col = 1
                        )
                    
                    if 'boolean' in [x['type'] for x in axis_types if
                                     x['axis'] == axis]:
                        fig.update_yaxes(range = [0, 1], tickvals=[0, 1], 
                                         ticktext=[0, 1], row = axis, col = 1)
                        fig.add_annotation(x = 0, y = 0.5, xref = 'paper',
                                           yref = f'y{axis}', xanchor = 'right',
                                           text = parameter.replace('_',' '),
                                           showarrow =False
                                           )
                    elif len([x for x in params_to_plot if x['axis'] == axis]) > 1:
                        max_yvalue = max([max(df[x['parameter']]) for x in
                                          params_to_plot if x['axis'] == axis])
                        param_axis_index = [x['parameter'] for x in params_to_plot
                                            if x['axis'] == axis].index(parameter)
                        x_paper_val = 0.1*(param_axis_index)
                        fig.add_annotation(x = x_paper_val, y = max_yvalue, 
                                           xref = 'paper', yref = f'y{axis}',
                                           xanchor = 'left', showarrow = False,
                                           text = parameter.replace('_',' '),
                                           font = {'color':colour}
                                           )
                    else:
                        fig.update_yaxes(title_text = 
                                             param['parameter'].replace('_',' '),
                                         row = axis, col=1)
                
            plot_height = (bool_height * boolean_count + 
                           bool_height * analogue_boolean_ratio * analogue_count +
                           top_margin)
            
            if 'boolean' in [x['type'] for x in params_to_plot]:
                annotation_lengths = [len(x['parameter']) for x in params_to_plot
                                      if x['type'] == 'boolean']
            else:
                annotation_lengths = [0]
            
            plot_title = f'{file_prefix.replace("_"," ")} - {page["page"]}'
            fig.update_layout(height = plot_height, showlegend = False,
                              title_x=0.5, title_text = plot_title,
                              margin=dict(
                                    l=7.5 * max(annotation_lengths),
                                    r=0,
                                    b=0,
                                    t=top_margin,
                                    pad=0
                                ),
                              )
            fig.update_xaxes(title_text = 'Timestamp (s)', row = max(axis_list),
                             col = 1)
            
        fig.write_html(f'{config["plot_dir"]}/{page["page"]}.html')
        fig.write_html(f'{config["plot_archive_dir"]}/{page["page"]}.html')
        
    archive_folder = config['archive_folder']    
    shutil.make_archive(f'Archive/{archive_folder}', 'zip', 
                        root_dir = 'Archive',
                        base_dir = archive_folder)
    shutil.rmtree(f'Archive/{archive_folder}')
    print(f'\tArchive saved to Archive/{archive_folder}')
    print(f'\tPlots created for {config["file"]}!')
    