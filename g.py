import streamlit as st
import pandas as pd
import time
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
st.set_page_config(page_title="Streamlit Speedometer Gauges", layout="wide")
# Constants
CORRECT_PASSWORD = "6081ca"
API_KEY = "6081"
A1 = 5
A2 = 2.3
A3 = 4.9492
B1 = 9.6
B2 = 0.9
if 'lists' not in st.session_state:
    st.session_state.lists = {'list1': [], 'list2': []}
if 'entered_strings' not in st.session_state:
    st.session_state.entered_strings = set()
# Additional session_state variable to store the selected index
if 'selected_index' not in st.session_state:
    st.session_state.selected_index = 0
def simulate_scanner_input(scanner_input):
    try:
           # If it's a double input, add to list2 if not exceeding the limit
            float_value = float(scanner_input)
            if float_value < 2000 and len(st.session_state.lists['list2']) < 30:
                st.session_state.lists['list2'].append(float_value)
                show_success_message("Pallet weight registered successfully.")
            elif float_value >= 2000:
                st.error("Pallet weight error.")
            else:
                st.error("Error: Trailer already contains 30 pallets.")
    except ValueError:
        st.error("Error: Invalid input.")

                
def show_success_message(message):
    success_placeholder = st.empty()
    success_placeholder.success(message)
    time.sleep(2)  # Display success message for 2 seconds
    success_placeholder.empty()

def delete_last_value():
        last_value_list2 = st.session_state.lists['list2'].pop()
        st.session_state.entered_strings.discard(last_value_list2)

        st.success("Last loaded pallet  unloaded successfully.")
    

def clear_all_values():
    
    st.session_state.lists['list2'].clear()
    st.session_state.entered_strings.clear()
    st.success("All pallets unloaded successfully.") 
def update_list2_value(value_to_add):
    # Add the number to the original value in List 2 at the specified index
    if 1 <= st.session_state.selected_index <= len(st.session_state.lists['list2']):
        st.session_state.lists['list2'][st.session_state.selected_index - 1] += value_to_add
        st.success(f"Pallet {st.session_state.selected_index} combined successfully. Pallet weight increased by: {value_to_add}")
    else:
        st.error("Error: pallet does not exist.")
        
def speedometer_gauge(fig, row, col, value, min_value, max_value, title, domain, gauge_dict):
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font':{'size': 18}},
        domain=domain,
        number={'font': {'size': 16}},  # Adjusted font size for the displayed value
        gauge=gauge_dict
    ), row=row, col=col)        
# Authenticate function
def authenticate():
    
    # Password input box in the sidebar
    password_input = st.sidebar.text_input("Enter password:", "", type="password")

    # Check if the entered password is correct
    if password_input == CORRECT_PASSWORD:
        # Authentication successful
        st.sidebar.success("Authentication successful!")
        time.sleep(2)  # Display success message for 2 seconds
        st.sidebar.empty()  # Clear the success message
        return True
    else:
        # Authentication failed
        st.sidebar.error("Authentication failed. Please enter the correct password.")
        return False

# Add a heading to the sidebar
st.sidebar.title("Control Panel")

# Define a mapping for shunt truck options
ShuntTruck_mapping = {'AB1001': 8000, 'AB2001': 9000}
# Define Shunt Truck with options A and B
ShuntTruck_options = list(ShuntTruck_mapping.keys())
ShuntTruck = st.sidebar.selectbox('Select ShuntTruck:', ShuntTruck_options, format_func=lambda x: x)

# Define a mapping for trailer class options
TrailerClass_mapping = {'Class1': 6500, 'Class2': 7500}
# Define trailer class with options C and D
TrailerClass_options = list(TrailerClass_mapping.keys())
TrailerClass = st.sidebar.selectbox('Select TrailerClass:', TrailerClass_options, format_func=lambda x: x)

# Define axle position with options 38, 39, 40, 41, and 42
AxlePosition_options = [38, 39, 40, 41, 42]
AxlePosition = st.sidebar.selectbox('Select AxlePosition:', AxlePosition_options)

# Multiply values of variable3 by a factor of 0.3048 for calculation purposes
variable3_factor = 0.3048 * AxlePosition

# Create variable l as a list of 30 values starting from 0.52 with increments of 1.03, each value repeating two times
l = [0.52 + i * 1.03 for i in range(30) for _ in range(2)][:30]  # limit to 30 values
# Create variable M from list 2 barcode scanned
N = st.session_state.lists['list2']
M = [0.0] * 30

# Update values in M based on values from N
for i in range(min(len(M), len(N))):
    M[i] = N[i]

# Calculate variable x1 as the product of M and l
x1 = [M[i] * l[i] for i in range(len(M))]


# Calculate variable x2 as the cumulative sum of values of x1 plus the product of variable2 and B1
x2 = [sum(x1[:i]) + TrailerClass_mapping[TrailerClass] * B1 for i in range(1, len(x1) + 1)]


# Calculate variable CM as the cumulative sum of values of M plus the value of variable2
CM = [sum(M[:i]) + TrailerClass_mapping[TrailerClass] for i in range(1, len(M) + 1)]


# Calculate variable x3 as the element-wise division of x2 by CM
x3 = [x2[i] / CM[i] for i in range(len(x2))]


# Calculate variable CG1 as the element-wise subtraction of B2 from x3
CG1 = [x3_value - B2 for x3_value in x3]


# Calculate variable x4 as the element-wise expression (variable3_factor - CG1) * (CM) / variable3_factor
x4 = [(variable3_factor - CG1_value) * CM_value / variable3_factor for CG1_value, CM_value in zip(CG1, CM)]


# Calculate variable x5 as the element-wise expression (variable1 * A2 + x4 * A3) / (variable1 + x4)
x5 = [(ShuntTruck_mapping[ShuntTruck] * A2 + x4_value * A3) / (ShuntTruck_mapping[ShuntTruck] + x4_value) for x4_value in x4]


# Calculate variable x6 as the element-wise expression (variable1 + x4) * (A1 - x5) / A1
x6 = [(ShuntTruck_mapping[ShuntTruck] + x4_value) * (A1 - x5_value) / A1 for x4_value, x5_value in zip(x4, x5)]


# Calculate variable x7 as the element-wise expression (variable1 + x4) / A1 * x5
x7 = [(ShuntTruck_mapping[ShuntTruck] + x4_value) / A1 * x5_value for x4_value, x5_value in zip(x4, x5)]


# Calculate variable x8 as the element-wise expression CM * CG1 / variable3_factor
x8 = [CM_value * CG1 / variable3_factor for CM_value, CG1 in zip(CM, CG1)]


# Calculate variable S as the maximum value from x6 list
S = max(x6)

# Calculate variable D as the maximum value from x7 list
D = max(x7)

# Calculate variable T as the maximum value from x8 list
T = max(x8)

# Calculate variable G as the sum of S, D, and T
G1 = S + D + T
# Calculate variable G2 
G2 = G1 - TrailerClass_mapping[TrailerClass] - ShuntTruck_mapping[ShuntTruck]
# Calculate Loading Efficiency
L1 = (G2/(37500 - TrailerClass_mapping[TrailerClass] - ShuntTruck_mapping[ShuntTruck]))*100

G3=  round(G1, 2)
G4=  round(G2, 2)
S1=  round(S, 2)
D1=  round(D, 2)
T1=  round(T, 2)
L2 = round(L1, 2)
# Combine lists to create a 15x2 table
combined_lists = [f" {val2}" for val2 in zip( N)]

# Main content sections
def Barcode_input():
    
      # Display alternating instructions based on the current input type
    instruction =  "Scan pallet weight"
    st.write(instruction)
    # Simulate scanner input using a text input field
    scanner_input = st.text_input("Scan Label", key="scanner_input")

    # Custom JavaScript to automatically trigger a click on the "Simulate Scan" button
    js_code = """
        <script>
        const inputField = document.getElementById("Simulated Scanner Input");
        inputField.addEventListener("input", function() {
            document.getElementById("Simulate Scan").click();
        });
        </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)

    # Event handling for automatic registration
    if scanner_input:
        simulate_scanner_input(scanner_input)

         
           
        # Buttons to delete and clear registered values
    if st.button("Unload last pallet"):
        delete_last_value()

    if st.button("Unload all pallets"):
        clear_all_values()
    

      
    
def Pallet_layout(combined_lists):

        # Determine the number of rows and columns for the table
    num_rows = min(15, len(combined_lists) // 2 + len(combined_lists) % 2)
    num_columns = 2

    # Create a 2x15 table from combined_lists
    table_data = []
    for row in range(num_rows):
        col1_index = row * num_columns
        col2_index = col1_index + 1
        col1_value = combined_lists[col1_index] if col1_index < len(combined_lists) else ""
        col2_value = combined_lists[col2_index] if col2_index < len(combined_lists) else ""
        table_data.append([col1_value,col2_value])
    # Display the table with markdown for headers and row indices
    headers = ["Left", "Right"]
    table_md = f"| {' | '.join(['Row'] + headers)} |\n"
    table_md += f"| {' | '.join(['---'] * (len(headers) + 1))} |\n"

    for i, row_data in enumerate(table_data):
        row_index = i + 1
        table_md += f"| {row_index} | {' | '.join(map(str, row_data))} |\n"

    st.markdown(table_md)
     


def info_load():
          st.write('Gross Weight:', G3)
          st.write('Payload:', G4)


def Display_table():
# Display Updated DataFrame in a vertical layout
    st.write("Trailer Load Plan")
    for key, value in st.session_state.user_data.items():
        st.text(f"{key}: {value}")     

# Check if the value is more than the critical value
if S > 5500:
    # Add image thumbnail before the warning message
    st.image("Stop.png", width=50)  # Replace with the path to your image

    # Display the warning message
    st.warning(f"The  Steer Axle Weight is above the legal weight limit.")
if D > 15000:
    # Add image thumbnail before the warning message
    st.image("Stop.png", width=50)  # Replace with the path to your image

    # Display the warning message
    st.warning(f"The Drive Axle Weight is above the legal weight limit.")
if T > 17000:
    # Add image thumbnail before the warning message
    st.image("Stop.png", width=50)  # Replace with the path to your image
    # Display the warning message
    st.warning(f"The Tandem Axle Weight  is above the legal weight limit.") 
def Speedometer_guage():
     # Set the min and max values for each gauge
    min_value1, max_value1 = 3000, 8000
    min_value2, max_value2 = 5000, 25000
    min_value3, max_value3 = 4000, 30000

    # Set the values and color criteria manually for each gauge
    value1, steps1 = S, [{'range': [min_value1, 5500], 'color': "green"}, {'range': [5500, 8000], 'color': "red"}]
    value2, steps2 = D, [{'range': [min_value2, 13500], 'color': "yellow"}, {'range': [13500, 15000], 'color': "green"}, {'range': [15000, max_value2], 'color': "red"}]
    value3, steps3 = T, [{'range': [min_value3, 15500], 'color': "yellow"}, {'range': [15500, 17000], 'color': "green"}, {'range': [17000, max_value3], 'color': "red"}]
# Define individual gauge dictionaries
    gauge_dict1 = {
        'axis': {'range': [min_value1, max_value1], 'tickvals': list(range(min_value1, max_value1 + 1, 1000)), 'tickfont': {'size': 12}},
        'bar': {'color': "black"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "black",
        'steps': steps1
    }

    gauge_dict2 = {
        'axis': {'range': [min_value2, max_value2], 'tickvals': list(range(min_value2, max_value2 + 1, 5000)), 'tickfont': {'size': 12}},
        'bar': {'color': "black"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "black",
        'steps': steps2
    }

    gauge_dict3 = {
        'axis': {'range': [min_value3, max_value3], 'tickvals': list(range(min_value3, max_value3 + 1, 5000)), 'tickfont': {'size': 12}},
        'bar': {'color': "black"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "black",
        'steps': steps3
    }

    # Create a subplot with three gauges
    fig = make_subplots(rows=1, cols=3, specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}]],
                        row_width=[0.1], column_width=[0.1,0.1,0.1], horizontal_spacing=0.15)
    # Add each gauge to the subplot
    speedometer_gauge(fig, 1, 1, value1, min_value1, max_value1, "Steer Axle", {'x': [0, 0.33], 'y': [0, 1]}, gauge_dict1)
    speedometer_gauge(fig, 1, 2, value2, min_value2, max_value2, "Drive Axle", {'x': [0.34, 0.67], 'y': [0, 1]}, gauge_dict2)
    speedometer_gauge(fig, 1, 3, value3, min_value3, max_value3, "Trailer Axle", {'x': [0.68, 1], 'y': [0, 1]}, gauge_dict3)
    st.write('Gross Weight',G3, 'Payload',G4,'Loading Efficiency',L2, '%' )
    # Customize layout
    fig.update_layout(height=600, width=650, showlegend=False, margin=dict(l=25, r=25, b=400, t=0))  # Adjusted margins
   # Show the subplot
    st.plotly_chart(fig)
    
def main():
  

    # Authenticate the user
    authenticated = authenticate()
    if authenticated:
        # Your authenticated content goes here
        
        # Create three columns at the top
        col1, col2, col3 = st.columns([0.2, 0.6 ,0.2], gap="large")

        # Add content to the first row
        with col1:
            Barcode_input()    
                       
        # Add content to the second row
        with col2:
            Pallet_layout(combined_lists)  
            
           
        with col3:
            Speedometer_guage()           
   
        
            
if __name__ == "__main__":
    main()
       
     
