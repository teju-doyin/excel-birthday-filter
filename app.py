import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Data Automation", layout="centered")

#  Modal for Download 
@st.dialog("Processing Complete!")
def show_success_modal(data, name, count):
    st.write(f"Successfully processed **{count}** birthday records.")
    st.download_button(
        label="📥 Download Excel File",
        data=data,
        file_name=f"{name}.xlsx" if name else "birthdays.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.title("Data Automation")
st.write("Please fill the short form below in order to process the data correctly")

birthday_column = st.text_input(
    "What's the title of the column that contains the birthday?",
    placeholder="e.g. Birthday"
)

data_format = st.selectbox(
    'Select which you prefer', 
    ["All birthdays", "A single month"],
    index=None,
    placeholder="How would you like the data?"
)

selected_month = None
if data_format == "A single month":
    selected_month = st.selectbox(
        'Please select the month',
        ["January","February","March","April","May","June","July","August","September","October","November","December"],
        index=None,
        placeholder="January"
    )

file_name = st.text_input(
    'What would you like to name the new file?',
    placeholder='October Birthday Girlies'
)

uploaded_file = st.file_uploader("Format accepted is .xlsx or .xls", type=["xlsx","xls"])

if st.button("Submit file"):
    if not uploaded_file:
        st.warning("Please upload an Excel file first.")
    elif not birthday_column:
        st.warning("Please enter the column name for birthdays.")
    elif data_format == "A single month" and not selected_month:
        st.warning("Please select a month.")
    else:
        try:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            
            df = df.dropna(how='all').dropna(axis=1, how='all')
            
            df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("/", "_")
            
            # Clean the user's input to match cleaned column names
            clean_birthday_col = birthday_column.strip().replace(" ", "_").replace("/", "_")

            if clean_birthday_col not in df.columns:
                st.error(f"Could not find column '{birthday_column}'. Available columns: {', '.join(df.columns)}")
            else:
                df[clean_birthday_col] = pd.to_datetime(df[clean_birthday_col], errors="coerce", dayfirst=True)
                
                if data_format == "A single month":
                    month_map = {
                        "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
                        "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
                    }
                    month_number = month_map[selected_month]
                    filtered_df = df[df[clean_birthday_col].dt.month == month_number].copy()
                else:
                    filtered_df = df[df[clean_birthday_col].notna()].copy()

                filtered_df["Day"] = filtered_df[clean_birthday_col].dt.day
                filtered_df = filtered_df.sort_values(by=["Day"])
                
                # Format for Export
                filtered_df[clean_birthday_col] = filtered_df[clean_birthday_col].dt.strftime("%d/%m/%Y")

                cols_to_keep = ["First_Name", "Last_Name", clean_birthday_col, "WhatsApp_Number", "Email"]
                existing_cols = [c for c in cols_to_keep if c in df.columns]
                
                result = filtered_df[existing_cols].copy()
                
                if "Email" in result.columns:
                    result = result.drop_duplicates(subset=["Email"])

                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    result.to_excel(writer, index=False)
                
                show_success_modal(output.getvalue(), file_name, len(result))

        except Exception as e:
            st.error(f"An error occurred while processing: {e}")