# Finance LLM

## Introduction
Welcome to the Finance LLM project! This project aims to provide a language model specifically trained in the field of finance and cryptocurrency. The language model is fine-tuned using the Mistral-7B-Instruct-v0.3 repository from Hugging Face.

## My Struggles
When starting this project I was very ambitious about it considering how it is sort of going to be a full end to end project but then I realized that I don't have the most important part of this entire project. You may ask what is it? Skill? Knowledge? No. It is a GPU. 

Throughout this project I was trying to find different ways where I could have just got a GPU to train this model on and run it. I own a secondhand Dell Latitude 5290 with intel i5 7th gen and 8gb ram. Now you might think it is rather foolish for someone with these kind of PC specs to indulge in AI/ML but well here I am being the fool I am. So now I need a GPU so I researched everywhere I can get a GPU from. I came across multiple services such as google colab, kaggle compute engines, lightning.ai, etc. But ironically the biggest issue is "Finance".

During the training I managed to somehow use my very little knowledge of quantization and the biggest model that I can load in free tier of google colab my mind could come up with. But the problems didn't stop there. Now I wanted to find a way to make it available to other people as well and wanted to host this application or atleast make it so that people can run it locally.

So I again went out on my research on all the hosting platforms where I can host this model and naturally the first thing that came up in my mind was using streamlit or huggingface spaces, but as it turns out they don't provide free GPU either. Next idea that I came up with was using AWS for students but that doesn't provides EC2 instance with GPU.

So now here we are with ambition of an end to end project but forced to share a jupyter notebook.

## Requirements
To run this project, make sure you have the following dependencies installed:
- pyPDF2
- transformers
- dataset
- torch
- bitsandbytes
- peft
- trl
- streamlit
- python-dotenv
- langchain
- langchain_huggingface

You can install these dependencies by running `pip install -r requirements.txt`.

## Getting Started
To get started with this project, follow these steps:
1. Clone the repository: `git clone https://github.com/your-username/finance-llm.git`
2. Navigate to the project directory: `cd finance-llm`
3. Set up the environment variables by creating a `.env` file and adding the necessary API keys and access tokens.
4. Run the `get_pdfs.py` script to retrieve the PDF files for training the language model.
5. Run the `create_dataset.py` script to create the dataset for fine-tuning the language model.
6. Run the `finetuning.ipynb` notebook to fine-tune the language model using the dataset.
7. Once the fine-tuning is complete, you can use the trained language model for generating finance-related questions and answers.

## Project Structure
The project structure is as follows:
```
finance-llm/
├── get_pdfs.py
├── create_dataset.py
├── finetuning.ipynb
├── requirements.txt
├── .gitignore
├── README.md
└── pdfs/
```

## Contributing
Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or submit a pull request.
