Excel Birthday Filter
A simple web automation tool to filter and sort birthday records from Excel files. Designed for quick administrative tasks without needing to write code or use a terminal.

Live App
https://birthday-filter.streamlit.app/

How to Use
1. Upload: Select your .xlsx or .xls member list.
2. Configure: - Enter the column name that contains the birthdays.
3. Choose to filter for a single month or all birthdays.
4. Download: Click Submit to process and download your cleaned, chronologically sorted Excel file.

Tech Stack
Language: Python
Framework: Streamlit
Processing: Pandas
Excel Engine: openpyxl / xlsxwriter

Local Setup
Clone the repo: git clone https://github.com/teju-doyin/excel-birthday-filter.git

Install dependencies: pip install -r requirements.txt

Run the app: streamlit run app.py