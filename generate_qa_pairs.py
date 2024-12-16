import base64
import requests
import jsonlines
from progressbar import progressbar, Percentage, GranularBar

messages_filename = "telegram_messages.txt" # Text file containing our base64 encoded messages
output_filename = "telegram_qa_pairs.jsonl" # Output file to store our Q&A pairs
qa_model = "neural-chat:latest" # Model to use in ollama API calls
ollama_api = "http://127.0.0.1:11434/api/generate" # URL for ollama api on localhost

def get_instruction(output):

    # location of ollama api
    url = ollama_api
    # Our base user prompt
    user = "Act as an AI engineer and generate an input from this chat message to be used in finetuning an LLM. Your response should be succinct. Your response should only include one corresponding question and nothing else."
 
    # Build post body
    data = {
        "model": qa_model,
        "options":{
            "temperature":0.6,
            "num_ctx":3000, # Number of context tokens
            "top_k":30, # I dunno. Look at the ollama api. Has to do with how creative the responses are
            "top_p": 0.5 # Still dunno. Has to do with how precise the responses are
        },
        # Our base user prompt plus the output (telegram message) that we want to get a question for
        "prompt": user + "\n" + output,
        # System prompt
        "system": "You are a master at generating inputs for fine-tuning large language models. You are provided a chat message and your job is to generate an input for that chat message. You must obey the following rules at all times:\n1. You must reply with only your provided input. Do not say anything before your response and do not provide any supporting information.\n2.Your responses must be applicable to the input field of a dataset using the Alpaca format",
        # If we wanted to be fancy like ChatGPT we can stream the tokens one by one, but we don't care here. We just want the full response
        "stream": False
    }

    response = requests.post(url, json=data)
    d = response.json()

    #print(d['response'] + "\n")
    #print("----------------------------------------------------------------")

    return d['response']

'''

Start of main file.

'''


data = [] # List to store our lines for training (in alpaca format)

# Open our file with our base64 encoded messages and 
with open(messages_filename, 'r', newline='') as file:

    lines = file.readlines()
    num_lines = int(len(lines))

    for line in progressbar(lines, widgets=[Percentage(), " Generating Q&A Pairs", GranularBar()], max_value=num_lines):

        message = base64.b64decode(line)
        message = message.decode("ascii")
        instruction = get_instruction(message) # This is calling the above function which calls the ollama api to get a response
        # We now have our response from our ollama call. Build the appropriate format (alpaca format) and add to our list
        data.append({
            "instruction": instruction, # AKA our generated question
            "input": "",
            "output": message[103:] # The first 104 characters is the "On XYZ date in the XYZ channel the following message was sent:". We wanted that to generate the questions, but we don't want it for training
        })

# Write Alpaca formatted JSONL file
with jsonlines.open(output_filename, 'w') as writer:
    writer.write_all(data)

# We're fancy so let's print some stats
print("QA Pairs Complete")
print(f"Number of generated pairs: {len(data)}")