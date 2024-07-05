import os
from pathlib import Path
from openai import OpenAI



def set_api_key(client):
    # Set your OpenAI API key
    client.api_key = "#"

def get_client():
    client = OpenAI(api_key="#")

    return client


def dataset_upload(client):
    file_path = Path("dataset.jsonl")
    response = client.files.create(
        file=file_path,
        purpose='fine-tune'
    )
    print(response)
    return response.id


def tune_now(client, uploaded_file_id):
    response = client.fine_tuning.jobs.create(
        training_file=uploaded_file_id,
        model="gpt-3.5-turbo"
    )
    print(response)
    return response.id

def get_fine_tuning_status(client, fine_tune_id):
    response = client.fine_tuning.jobs.retrieve(fine_tune_id)
    print(response)
    return response

def list_fine_tuning_jobs(client):
    response = client.fine_tuning.jobs.list()
    print(response)
    return response['data']


def get_completed_model_id(client):
    jobs = list_fine_tuning_jobs(client)
    for job in jobs:
        if job['status'] == 'succeeded':
            return job['fine_tuned_model']
    return None


def chat_with_yx_model(client, model_id, user_content):
    completion = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": "This is a Westpac banking assistant."},
            {"role": "user", "content": user_content}
        ]
    )
    return completion

def extract_message(response):
    try:
        # Navigate through the object attributes to get the message content
        message = response.choices[0].message.content
        return message
    except (AttributeError, IndexError) as e:
        print(f"Error extracting message: {e}")
        return None

def test_open_file():
    file_path = "dataset.jsonl"
    try:
        with open(file_path, "rb") as file:
            content = file.read()
            print("File opened and read successfully.")
            print(f"First 100 bytes of the file: {content[:100]}")
    except FileNotFoundError:
        print("File not found. Please check the file path.")


# Main
if __name__ == '__main__':
    client = OpenAI(api_key="#")

    # Step 1: Test file opening
    #test_open_file()

    # Step 2: Upload training dataset
    #file_id = dataset_upload(client)

    # Step 3: Begin fine-tune ChatGPT model
    #fine_tune_id = tune_now(client, file_id)

    # Step 4: Check fine-tune status
    # fine_tuning_status = get_fine_tuning_status(client, fine_tune_id)
    # print(f"Fine-tuning job status: {fine_tuning_status.status}")

    # Step 5: If fine-tuning job is already completed and you don't know the model ID
    user_content = "What is the interest rate for savings accounts?"
    print(chat_with_yx_model(client, "ft:gpt-3.5-turbo-0125:personal::9dbmYZT5", user_content))
    # completed_model_id = get_completed_model_id(client)
    # print(completed_model_id)
    # if completed_model_id:
    #     print(f"Found completed model ID: {completed_model_id}")
    #     chat_with_yx_model(client, completed_model_id)
    # else:
    #     print("No completed fine-tuning job found or fine-tuning job has not completed successfully.")
