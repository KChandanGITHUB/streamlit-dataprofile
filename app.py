from csv import field_size_limit
from distutils.command.upload import upload
from enum import Flag
from platform import python_branch
import streamlit as st 
import pandas as pd
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import numpy as np
import sys
import os
# if you dont se the page_confi the charts will be one below the other ( charts will be very narrow), so you need to scroll down to see each charts, 
# instead we can set the page configuration to have it wide.
# the layout shoud be wide
st.set_page_config(page_title='Data Profiler', layout='wide')

# we have to set the limit of importing the file. import file should not be greater than 10mb.
def get_filesize(file):
    size_bytes = sys.getsizeof(file)
    size_mb = size_bytes / (1024 * 1024) # or (1024 **2)
    return size_mb

# Below validation is for the user, if user imports other than csv or excel file it should throw up a message.
def validate_file(file):
    filename = file.name
    name, ext= os.path.splitext(filename)
    # let apply validation here.
    if ext  in ('.csv', '.xlsx'):
        return ext
    else:
        return False
    

# create side bar to upload file, or to import file or drag and drop option.
with st.sidebar:
    uploaded_file = st.file_uploader('upload.csv, .xlsx files not exceeding 10 MB')
    # now we wil put some validation whether file is uploaded or not.
    if uploaded_file is not None:
        st.write('Mode of Operation')
        # lets create objects, so that user can select what kind of view they want to see. (minimal report, dark mode, orange mode)
        minimal = st.checkbox('Do you want minimal report ?')
        display_mode = st.radio('Display mode:', 
                                options = ('Primary', 'Dark', 'Orange'))
        
        # adding validation for user selection in the radio button
        if display_mode == 'Dark':
            dark_mode = True
            orange_mode = False
        elif display_mode == 'Orange':
            dark_mode = False
            orange_mode = True
        else:
            dark_mode = False
            orange_mode = False

# file upload, drag and drop option, browse files.
# below will also you give you an option to maximize or minime the size bar for file upload option.    
if uploaded_file is not None:
# we are using above condition here, if user imports other than csv or excel.

    ext = validate_file(uploaded_file)
    if ext:
# validation for  file size upload.

        filesize = get_filesize(uploaded_file)
        if filesize <= 10:
            if ext == '.csv':
                # time being let load csv
                df = pd.read_csv(uploaded_file)
            else:
                xl_file = pd.ExcelFile(uploaded_file)

                sheet_tuple = tuple(xl_file.sheet_names)
# now we are giving the option for user, if they are importing excel file, which sheet they want to import

                sheet_name = st.sidebar.selectbox('Select the sheet',sheet_tuple)
                df = xl_file.parse(sheet_name)
                     # to generate profiling report: Spinner is a round widget for loading. In the below when file is getting uploaded to the streamlit
                    # a round widget will appear as loading to generate pandas profile_report. 

                
                
            with st.spinner('Generating Report'):
 # in the below we are setting the how the users how to see the reports (appearence or looks, what kind of appearence users wants to view)

                pr = ProfileReport(df,
                                minimal=minimal,
                                dark_mode=dark_mode,
                                orange_mode=orange_mode
                                )
                
            st_profile_report(pr)
        else:
            st.error(f'Maximum allowed filesize is 10 MB. But received {filesize} MB')
            
    else:
        st.error('Kindly upload only .csv or .xlsx file')
        
else:
    st.title('Data Profiler')
    st.info('Upload your data in the left sidebar to generate profiling')

