import streamlit as st
import numpy as np
import pandas as pd
# Constants
CORRECT_PASSWORD = "6081ca"
API_KEY = "6081"
A = 8500
B = 6900
A1 = 5
A2 = 2.425
A3 = 4.95
B1 = 9.816
B2 = 0.9

# Add a heading to the sidebar
st.sidebar.title("")
# Define variable 3 with options 39, 40, 41, and 42
variable3_options = [39, 40, 41, 42]
variable3 = st.sidebar.selectbox('Tandem Position:', variable3_options)

# Multiply values of variable3 by a factor of 0.3048 for calculation purposes
variable3_factor = 0.3048 * variable3

# Authenticate function
def authenticate():
    # Password input box
    password_input = st.text_input("Enter password:", "", type="password")

    # Check if the entered password is correct
    if password_input == CORRECT_PASSWORD:
        # Authentication successful
        return True
    else:
        # Authentication failed
        st.error("Authentication failed. Please enter the correct password.")
        return False
def main1():
    st.title("J Special Lite")

    # Initialize N and M
    if 'N' not in st.session_state:
        st.session_state.N = []
    if 'M' not in st.session_state:
        st.session_state.M = [0.0] * 30

    # Input widget to get user input
    new_value = st.text_input("Enter a Pallet weight:", key="input", on_change=append_value)

        # Check if the list has reached 30 values
    if len(st.session_state.N) >= 30:
        st.error("Trailer has already 30 pallets loaded! .")
    
def append_value():
    new_value = st.session_state.input
    N = st.session_state.N
    M = st.session_state.M

    try:
        float_value = float(new_value)
    except ValueError:
        st.error("Error: Please enter a valid float value.")
        return

    if len(N) < 30:
        N.append(float_value)
        M[len(N) - 1] = float_value  # Replace the corresponding value in M
        st.session_state.input = ""  # Clear the input value

def update_value(index, edited_value):
    N = st.session_state.N
    M = st.session_state.M

    try:
        float_value = float(edited_value)
    except ValueError:
        st.error("Error: Please enter a valid float value.")
        return

    if N and 0 <= index < len(N):
        N[index] = float_value
        M[index] = float_value

def generate_table():
    M = st.session_state.M

    # Initialize a 2x15 table
    table_data = [[0.0] * 15 for _ in range(2)]

    # Fill the table with values from M
    index = 0
    for col in range(15):
        for row in range(1, -1, -1):  # Populate from bottom to top
            table_data[row][col] = M[index]
            index += 1

    # Display the table
    st.table(table_data)
    
def main():
    # Authenticate the user
    authenticated = authenticate()

    if authenticated:
        # Your authenticated content goes here
        st.write("Authentication successful!")

        # Choose which sections to display based on your app logic
        main1()
        
        # Add more sections as needed

if __name__ == "__main__":
    main()


# Create variable l as a list of 30 values starting from 0.52 with increments of 1.03, each value repeating two times
I = [0.52 + i * 1.03 for i in range(30) for _ in range(2)][:30]  # limit to 30 values

M = st.session_state.M
# Create variable l as a list of 30 values starting from 0.52 with increments of 1.03, each value repeating two times
l = [0.52 + i * 1.03 for i in range(30) for _ in range(2)][:30]  # limit to 30 values

 
       # Calculate variable x1 as the product of M and l
x1 = [I * M for I, M in zip(I, M)]       

# Calculate variable x2 as the cumulative sum of values of x1 plus the product of B and B1
x2 = [sum(x1[:i]) + B * B1 for i in range(1, len(x1) + 1)]

# Calculate variable CM as the cumulative sum of values of M plus the value of variable2
CM = [sum(M[:i]) + B for i in range(1, len(M) + 1)]

# Calculate variable x3 as the element-wise division of x2 by CM (CX Tra)
x3 = [x2[i] / CM[i] for i in range(len(x2))]

# Calculate variable CG1 as the element-wise subtraction of B2 from x3
CG1 = [x3_value - B2 for x3_value in x3]

# Calculate variable x4 as the element-wise expression (variable3_factor - CG1) * (CM) / variable3_factor (5th W)
x4 = [(variable3_factor - CG1_value) * CM_value / variable3_factor for CG1_value, CM_value in zip(CG1, CM)]

# Calculate variable x5 as the element-wise expression (A * A2 + x4 * A3) / (A + x4) (CxTT)
x5 = [(A * A2 + x4_value * A3) / (A + x4_value) for x4_value in x4]

# Calculate variable x6 as the element-wise expression (A + x4) * (A1 - x5) / A1 (S)
x6 = [(A + x4_value) * (A1 - x5_value) / A1 for x4_value, x5_value in zip(x4, x5)]

# Calculate variable x7 as the element-wise expression (A + x4) / A1 * x5 (D)
x7 = [(A + x4_value) / A1 * x5_value for x4_value, x5_value in zip(x4, x5)]

# Calculate variable x8 as the element-wise expression CM * CG1  / variable3_factor (T)                                 
x8 = [CM_value * CG1 / variable3_factor for CM_value, CG1 in zip(CM, CG1)]

# Calculate variable S as the maximum value from x6 list
S = max(x6)
st.write('Steer Axle:', S)

# Calculate variable D as the maximum value from x7 list
D = max(x7)
st.write('Drive Axle:', D)

# Calculate variable T as the maximum value from x8 list
T = max(x8)
st.write('Tandem Axle', T)
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

# Calculate variable G as the sum of S, D, and T
G = S + D + T
st.write('Gross Weight:', G)
G1 = G - A - B
st.write('Payload:', G1)

# Display the table after editing
st.header("Pallet Layout")
generate_table()
# Edit value section
st.header("Change the Loaded Pallet Weight")

# Select a value to edit
selected_index = st.selectbox("Select a pallet:", list(range(len(st.session_state.N))))

# Input widget to edit the selected value
edited_value = st.text_input("Enter new weight:", value=st.session_state.N[selected_index] if st.session_state.N else "")

# Button to update the value
if st.button("Update weight"):
    update_value(selected_index, edited_value)

