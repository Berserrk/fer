from llama_cpp import Llama
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import snapshot_download

# download model from huggingface 

# snapshot_download(
#     repo_id = "unsloth/gemma-3-27b-it-GGUF",
#     local_dir = "unsloth/gemma-3-27b-it-GGUF",
#     allow_patterns = ["*Q4_K_M*"], # For Q4_K_M
# )


if __name__== "__main__": 
# model_path = "/Users/firaterman/Documents/fer/models/Mistral-7B-Instruct/GGUF/Mistral-7B-Instruct-v0.3-Q6_K.gguf"
# model_path = "/Users/firaterman/Documents/fer/models/models/Mistral-7B-Instruct/GGUF/Llama-3.3-70B-Instruct-Q2_K.gguf"
    # model_path = "/Users/firaterman/.lmstudio/models/lmstudio-community/gemma-3-12b-it-GGUF/gemma-3-12b-it-Q4_K_M.gguf"
    # model_path = "/Users/firaterman/Documents/fer/models/gemma3_12b/gemma-3-12b-it-Q4_K_M.gguf"
    model_path = "/Users/firaterman/Documents/fer/models/models/google_gemma3_12b/google_gemma-3-12b-it-Q4_K_M.gguf"
    llm = Llama(model_path=model_path)

    # output = llm("What is the capital of Japan?")

    # response = output["choices"][0]["text"].strip()  # Store the response as a string
    # print(response)  # Print or use it in your code
    llm = Llama(model_path=model_path, n_ctx=2048, n_threads=8)  # Adjust threads/context as needed

    # Generate text
    response = llm("What is the capital of France?")
    print(response["choices"][0]["text"])
.



# import streamlit as st
import os

uploaded_file = st.file_uploader("Upload a file")
submit = st.button("Submit")

if submit and uploaded_file:
    # Save file to disk temporarily (optional, depends on your need)
    save_path = os.path.join("temp_uploads", uploaded_file.name)

    # Create directory if needed
    os.makedirs("temp_uploads", exist_ok=True)

    # Save file
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Store path in session_state
    st.session_state["file_path"] = save_path
    st.success(f"File saved at {save_path}")

# Later in the app
file_path = st.session_state.get("file_path")

if file_path:
    st.write("✅ Stored file path:", file_path)
    # You can now use file_path in any other function
else:
    st.warning("⚠️ File path not found. Please upload and submit a file first.")



c     