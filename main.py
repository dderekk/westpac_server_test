import os
import openai
def set_api_key():
    #set you openapi key
    openai.api_key = "sk-YOUR-OPENAI-KEY-HERE"
def dataset_upload():
    set_api_key()
    result = openai.File.create(
        file=open("path-to-your-local/dataset.jsonl", "rb"),
        purpose='fine-tune'
    )
    print(result)

def tune_now(uploaded_file_id):
    set_api_key()
    result = openai.FineTuningJob.create(training_file=uploaded_file_id, model="gpt-3.5-turbo")
    print(result)

def chat_with_yx_model(model_id):
    set_api_key()
    completion = openai.ChatCompletion.create(
        model=model_id,
        messages=[
            {"role": "system",
             "content": "Marv is mental healthy expert"},
            {"role": "user", "content": "Who does mental illness affect?"}
        ]
    )
    print(completion)

if __name__ == '__main__':
    #step 1 : upload training dataset
    dataset_upload()

    #step 2 : begin fine-tune ChatGPT model
    #tune_now("file-B9UjNJwHqVU1cBu1mZraLw1q")

    #step 3 : use my trained model
    #chat_with_yx_model("ft:gpt-3.5-turbo-0613:personal::84NbaCOS" )
