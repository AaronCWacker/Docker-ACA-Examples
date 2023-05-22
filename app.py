import gradio as gr
import os 
import json 
import requests

#Streaming endpoint 
API_URL = "https://api.openai.com/v1/chat/completions" #os.getenv("API_URL") + "/generate_stream"
OPENAI_API_KEY= os.environ["HF_TOKEN"] # Add a token to this space .  Then copy it to the repository secret in this spaces settings panel.  os.environ reads from there.
# Keys for Open AI ChatGPT API usage are created from here: https://platform.openai.com/account/api-keys

def predict(inputs, top_p, temperature, chat_counter, chatbot=[], history=[]):  #repetition_penalty, top_k

    # 1. Set up a payload
    payload = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": f"{inputs}"}],
    "temperature" : 1.0,
    "top_p":1.0,
    "n" : 1,
    "stream": True,
    "presence_penalty":0,
    "frequency_penalty":0,
    }

    # 2. Define your headers and add a key from https://platform.openai.com/account/api-keys
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    # 3. Create a chat counter loop that feeds [Predict next best anything based on last input and attention with memory defined by introspective attention over time]
    print(f"chat_counter - {chat_counter}")
    if chat_counter != 0 :
        messages=[]
        for data in chatbot:
          temp1 = {}
          temp1["role"] = "user" 
          temp1["content"] = data[0] 
          temp2 = {}
          temp2["role"] = "assistant" 
          temp2["content"] = data[1]
          messages.append(temp1)
          messages.append(temp2)
        temp3 = {}
        temp3["role"] = "user" 
        temp3["content"] = inputs
        messages.append(temp3)
        payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages, #[{"role": "user", "content": f"{inputs}"}],
        "temperature" : temperature, #1.0,
        "top_p": top_p, #1.0,
        "n" : 1,
        "stream": True,
        "presence_penalty":0,
        "frequency_penalty":0,
        }
    chat_counter+=1

    # 4. POST it to OPENAI API
    history.append(inputs)
    print(f"payload is - {payload}")
    response = requests.post(API_URL, headers=headers, json=payload, stream=True)
    token_counter = 0 
    partial_words = "" 

    # 5. Iterate through response lines and structure readable response
    counter=0
    for chunk in response.iter_lines():
        if counter == 0:
          counter+=1
          continue
        if chunk.decode() :
          chunk = chunk.decode()
          if len(chunk) > 12 and "content" in json.loads(chunk[6:])['choices'][0]['delta']:
              partial_words = partial_words + json.loads(chunk[6:])['choices'][0]["delta"]["content"]
              if token_counter == 0:
                history.append(" " + partial_words)
              else:
                history[-1] = partial_words
              chat = [(history[i], history[i + 1]) for i in range(0, len(history) - 1, 2) ]  # convert to tuples of list
              token_counter+=1
              yield chat, history, chat_counter 
                   

def reset_textbox():
    return gr.update(value='')


    

# Episodic and Semantic IO
def list_files(file_path):
    import os
    icon_csv = "📄 "
    icon_txt = "📑 "
    current_directory = os.getcwd()
    file_list = []
    for filename in os.listdir(current_directory):
        if filename.endswith(".csv"):
            file_list.append(icon_csv + filename)
        elif filename.endswith(".txt"):
            file_list.append(icon_txt + filename)
    if file_list:
        return "\n".join(file_list)
    else:
        return "No .csv or .txt files found in the current directory."

# Function to read a file
def read_file(file_path):
    try:
        with open(file_path, "r") as file:
            contents = file.read()
            return f"{contents}"
            #return f"Contents of {file_path}:\n{contents}"
    except FileNotFoundError:
        return "File not found."

# Function to delete a file
def delete_file(file_path):
    try:
        import os
        os.remove(file_path)
        return f"{file_path} has been deleted."
    except FileNotFoundError:
        return "File not found."

# Function to write to a file
def write_file(file_path, content):
    try:
        with open(file_path, "w") as file:
            file.write(content)
        return f"Successfully written to {file_path}."
    except:
        return "Error occurred while writing to file."

# Function to append to a file
def append_file(file_path, content):
    try:
        with open(file_path, "a") as file:
            file.write(content)
        return f"Successfully appended to {file_path}."
    except:
        return "Error occurred while appending to file."


title = """<h1 align="center">Generative AI Intelligence Amplifier - GAIA</h1>"""
description = """
## GAIA Dataset References: 📚
- **WebText:** A dataset of web pages crawled from domains on the Alexa top 5,000 list. This dataset was used to pretrain GPT-2.
  - [WebText: A Large-Scale Unsupervised Text Corpus by Radford et al.](https://paperswithcode.com/dataset/webtext)
- **Common Crawl:** A dataset of web pages from a variety of domains, which is updated regularly. This dataset was used to pretrain GPT-3.
  - [Language Models are Few-Shot Learners](https://paperswithcode.com/dataset/common-crawl) by Brown et al.
- **BooksCorpus:** A dataset of over 11,000 books from a variety of genres.
  - [Scalable Methods for 8 Billion Token Language Modeling](https://paperswithcode.com/dataset/bookcorpus) by Zhu et al.
- **English Wikipedia:** A dump of the English-language Wikipedia as of 2018, with articles from 2001-2017.
  - [Improving Language Understanding by Generative Pre-Training](https://huggingface.co/spaces/awacke1/WikipediaUltimateAISearch?logs=build) Space for Wikipedia Search
- **Toronto Books Corpus:** A dataset of over 7,000 books from a variety of genres, collected by the University of Toronto.
  - [Massively Multilingual Sentence Embeddings for Zero-Shot Cross-Lingual Transfer and Beyond](https://paperswithcode.com/dataset/bookcorpus) by Schwenk and Douze.
- **OpenWebText:** A dataset of web pages that were filtered to remove content that was likely to be low-quality or spammy. This dataset was used to pretrain GPT-3.
  - [Language Models are Few-Shot Learners](https://paperswithcode.com/dataset/openwebtext) by Brown et al.  
  """

# 6. Use Gradio to pull it all together
with gr.Blocks(css = """#col_container {width: 100%; margin-left: auto; margin-right: auto;} #chatbot {height: 400px; overflow: auto;}""") as demo:
    gr.HTML(title)
    with gr.Column(elem_id = "col_container"):
        inputs = gr.Textbox(placeholder= "Paste Prompt with Context Data Here", label= "Type an input and press Enter")
        chatbot = gr.Chatbot(elem_id='chatbot')
        state = gr.State([])
        b1 = gr.Button()
        with gr.Accordion("Parameters", open=False):
            top_p = gr.Slider( minimum=-0, maximum=1.0, value=1.0, step=0.05, interactive=True, label="Top-p (nucleus sampling)",)
            temperature = gr.Slider( minimum=-0, maximum=5.0, value=1.0, step=0.1, interactive=True, label="Temperature",)
            chat_counter = gr.Number(value=0, visible=True, precision=0)

            
    # Episodic/Semantic IO
    fileName = gr.Textbox(label="Filename")
    fileContent = gr.TextArea(label="File Content")
    completedMessage = gr.Textbox(label="Completed")
    label = gr.Label()
    with gr.Row():
        listFiles = gr.Button("📄 List File(s)")
        readFile = gr.Button("📖 Read File")
        saveFile = gr.Button("💾 Save File")
        deleteFile = gr.Button("🗑️ Delete File")
        appendFile = gr.Button("➕ Append File")
    listFiles.click(list_files, inputs=fileName, outputs=fileContent)
    readFile.click(read_file, inputs=fileName, outputs=fileContent)
    saveFile.click(write_file, inputs=[fileName, fileContent], outputs=completedMessage)
    deleteFile.click(delete_file, inputs=fileName, outputs=completedMessage)
    appendFile.click(append_file, inputs=[fileName, fileContent], outputs=completedMessage )

    
    inputs.submit(predict, [inputs, top_p, temperature,chat_counter, chatbot, state], [chatbot, state, chat_counter])
    b1.click(predict, [inputs, top_p, temperature, chat_counter, chatbot, state], [chatbot, state, chat_counter])
    b1.click(reset_textbox, [], [inputs])
    inputs.submit(reset_textbox, [], [inputs])
    gr.Markdown(description)
    
    demo.queue().launch(debug=True)
