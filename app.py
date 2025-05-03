import streamlit as st
import groq
import nbformat
import io

# Set up Groq client
client = groq.Client(api_key="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")

def generate_code_with_groq(prompt):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "Generate a machine learning training script based on user preferences."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Set page config
st.set_page_config(page_title="Code Generator & Optimizer", layout="wide")

# Sidebar navigation
page = st.sidebar.selectbox("Choose a feature", ["Code Generator", "Chatbot", "Code Optimizer"])

# ---------- Code Generator ----------
if page == "Code Generator":
    st.title("🔧 ML Code Generator")

    with st.form("code_gen_form"):
        framework = st.selectbox("Framework", ["PyTorch", "TensorFlow", "Scikit-learn"])
        preprocessing = st.checkbox("Include Preprocessing")
        model = st.selectbox("Model", ["Linear Regression", "CNN", "Random Forest", "Decision Tree"])
        training = st.checkbox("Include Training Code")
        epochs = st.number_input("Epochs", min_value=1, max_value=1000, value=10)
        optimizer = st.selectbox("Optimizer", ["SGD", "Adam", "RMSprop"])
        learning_rate = st.number_input("Learning Rate", value=0.001, format="%.5f")
        visualization = st.selectbox("Visualization Library", ["Matplotlib", "Seaborn", "Plotly"])
        submitted = st.form_submit_button("Generate Code")

    if submitted:
        user_prompt = (
            f"Generate a {framework} training script with {'preprocessing' if preprocessing else 'no preprocessing'}, "
            f"a {model}, {'training' if training else 'no training'}, "
            f"{epochs} epochs using {optimizer} optimizer with a learning rate of {learning_rate}, "
            f"and visualization using {visualization}."
        )
        generated_code = generate_code_with_groq(user_prompt)
        st.code(generated_code, language="python")

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("⬇️ Download .py", generated_code, file_name="generated_code.py", mime="text/x-python")

        with col2:
            nb = nbformat.v4.new_notebook()
            nb.cells.append(nbformat.v4.new_code_cell(generated_code))
            nb_json = nbformat.writes(nb)
            st.download_button("⬇️ Download .ipynb", nb_json, file_name="generated_code.ipynb", mime="application/json")

# ---------- Chatbot ----------
elif page == "Chatbot":
    st.title("💬 ML Chatbot Assistant")
    question = st.text_input("Ask your ML-related question:")
    if question:
        response = generate_code_with_groq(f"Answer this ML-related question in simple terms: {question}")
        st.markdown("**Answer:**")
        st.write(response)

# ---------- Code Optimizer ----------
elif page == "Code Optimizer":
    st.title("🚀 Code Optimizer")
    user_code = st.text_area("Paste your ML code to get suggestions", height=300)
    if st.button("Optimize"):
        prompt = f"Here is some machine learning code:\n\n{user_code}\n\nSuggest improvements and optimizations."
        optimized = generate_code_with_groq(prompt)
        st.markdown("**Optimized Suggestions:**")
        st.write(optimized)
