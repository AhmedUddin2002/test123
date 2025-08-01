import streamlit as st
import pandas as pd
import openai

st.set_page_config(page_title="Chat with Dataset", layout="wide")
st.title("💬 Chat with Your Dataset")

if "uploaded_df" not in st.session_state:
    st.warning("Please upload a dataset from the main dashboard page first.")
else:
    df = st.session_state["uploaded_df"]

    with st.expander("Preview Dataset"):
        st.dataframe(df.head(10))

    openai.api_key = "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"

    user_query = st.text_area("Ask a question about your dataset:", placeholder="e.g., Top 5 institutes by attendance")

    if st.button("Ask"):
        if user_query.strip():
            # Step 1: Send query to GPT to generate pandas code
            prompt = f"""
            You are a senior Python data analyst. 
            Convert the following question into Python pandas code.
            Use ONLY the dataframe 'df'. 
            The final line of your code MUST assign the result to a variable named 'result'.
            Do NOT include explanations or print statements.
            Columns available: {list(df.columns)}

            User query: {user_query}

            Example:
            # Good:
            result = df[['institute_name','attendance']].sort_values('attendance', ascending=False).head(5)

            # Bad:
            print(df)
            return df
            """

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "system", "content": "You are an expert data analyst and Python programmer."},
                              {"role": "user", "content": prompt}],
                    max_tokens=400,
                    temperature=0
                )

                python_code = response["choices"][0]["message"]["content"]

                # Debug view
                st.code(python_code, language="python")

                local_vars = {"df": df}

                # Execute safely
                exec(python_code, {}, local_vars)

                if "result" in local_vars:
                    result = local_vars["result"]

                    # Check if GPT returned full dataset (incorrect behavior)
                    if isinstance(result, pd.DataFrame) and len(result) == len(df):
                        st.warning("The query returned the full dataset. Please refine your question.")
                    else:
                        if isinstance(result, pd.DataFrame) or isinstance(result, pd.Series):
                            st.success("Result:")
                            st.dataframe(result)
                        else:
                            st.write(result)
                else:
                    st.warning("No result variable generated. Try a clearer question.")

            except Exception as e:
                st.error(f"Error: {e}")

        else:
            st.warning("Please enter a valid question.")
