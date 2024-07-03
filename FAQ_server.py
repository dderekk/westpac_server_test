import QA_Training as qa

client = qa.get_client()

def get_answer(question):
    model_id = "ft:gpt-3.5-turbo-0125:personal::9dbmYZT5"  # Replace with your fine-tuned model ID
    response = qa.chat_with_yx_model(client, model_id, question)
    return qa.extract_message(response)
