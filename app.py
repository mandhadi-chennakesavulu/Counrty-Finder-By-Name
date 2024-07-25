import pandas as pd
import openai
import streamlit as st

def get_origin_country(name, api_key):
    prompt = f"Determine the country of origin for the name: {name}. Provide only the country name where this name is most commonly used."
    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # You can use "gpt-4" if "gpt-4-turbo" is not available
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50
        )
        origin_country = response.choices[0].message['content'].strip()
        return origin_country if origin_country else 'Unknown'
    except Exception as e:
        st.error(f"Error fetching origin for {name}: {e}")
        return 'Error'

def main():
    st.title('Name Origin Finder')
    
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    
    if api_key:
        uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
        
        if uploaded_file:
            df = pd.read_excel(uploaded_file)
            
            if 'First Name' in df.columns and 'Last Name' in df.columns:
                st.write("Processing your file...")
                
                df['Full Name'] = df['First Name'] + ' ' + df['Last Name']
                df['Origin Country'] = df['Full Name'].apply(lambda name: get_origin_country(name, api_key))
                df = df.drop(columns=['Full Name'])
                
                output_file_path = 'output_file.xlsx'
                df.to_excel(output_file_path, index=False)
                
                st.success("Processing complete! You can download the processed file below.")
                st.download_button(
                    label="Download Processed File",
                    data=open(output_file_path, 'rb').read(),
                    file_name='processed_names.xlsx'
                )
            else:
                st.error("The uploaded file must contain 'First Name' and 'Last Name' columns.")
    else:
        st.warning("Please enter your OpenAI API Key to proceed.")

if __name__ == "__main__":
    main()
