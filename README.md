


![fenrir-desktop-bg](https://user-images.githubusercontent.com/8293038/133816238-7152221b-c37d-46ca-831d-ff636178f44f.png)

# How to Train Your Llama: Lessons Learned on Training LLama 3.1 on Threat Actor Telegram messages

This repo is supplemental material for my presentation for [Bsides Philly](https://bsidesphilly.org). If you have any questions or just want to talk get in touch with me:

- [All Links](https://links.corywolff.com)
- Email me at yxakl5mae@relay.firefox.com

## Abstract
Training and fine tuning LLMs is an incredibly complex process, but thanks to different libraries and frameworks we can easily find our own data and fine tune open source models like Llama 3.1.

This talk will be the story of how I scraped Telegram channels operated by threat actors and used this data to fine tune Llama 3.1. It will give attendees an easy way to fine-tune their own models and demonstrate what steps to take and what pitfalls to avoid.

## Things to Know
I am by no means an expert in machine learning or AI. I first started my machine learning journey in 2018 when I took various courses on the topic. Back then, it was very time consuming and somewhat difficult. Back then when you wanted to load a dataset you needed to write all the code to load the file, clean it, parse it, and put it into training and test data. Nowadays you can do that just by using Huggingfaces `load_dataset` method.

The advancements in AI are due to the support of the community and the different tooling and techniques that have been created since 2018. This project was a way for me to get up to speed on the topic and start to do some fun stuff. My hope is that you can learn the basics of fine tuning a model and avoid some of the time consuming mistakes I made along the way.

## Dataset
The dataset generated during this project is available on Huggingface: [threatactor-telegram-18k](https://huggingface.co/datasets/corywolff/threatactor-telegram-18k)

## Converting to GGUF
If you followed along you should have a modelfile in merged 16bit format. To convert this you would:

Convert from merged 16 bit to GGUF with llama.cpp

`python <LLAMA_CPP_FOLDER>/convert_hf_to_gguf.py <MODEL_FOLDER_NAME>/ --outfile <YOUR_FILE_NAME>.gguf --outtype f16`

Create a Modelfile for ollama
`nano <MODELNAME-Modelfile>`

Update Modelfile
```
FROM <LOCATION_OF_YOUR_GGUF>
```

Create model from modelfile with ollama

`ollama create <YOUR_MODEL_NAME> -f <LOCATION_OF_MODELFILE>`