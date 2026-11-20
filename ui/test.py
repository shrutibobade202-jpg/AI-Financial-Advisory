import gradio as gr
import time

def add_message_messages(history, message):
    history.append({"role": "user", "content": message})
    return history, ""

def bot_response_messages(history):
    time.sleep(1)
    image_path = "C:/Users/HP/Desktop/agentic-project/financial_advisor/generated_images/generated.png" # Replace with your actual image path or URL

    # The bot message content is a gr.Image component instance
    bot_image_message = {"role": "assistant", "content": gr.Image(image_path, show_label=False)} 
    history.append(bot_image_message)
    return history

with gr.Blocks() as demo:
    # Set type="messages" and height
    chatbot = gr.Chatbot(height=450) 
    msg = gr.Textbox(label="Your Message")
    clear = gr.ClearButton([msg, chatbot])

    msg.submit(add_message_messages, [chatbot, msg], [chatbot, msg], queue=False).then(
        bot_response_messages, chatbot, chatbot
    )

if __name__ == "__main__":
    demo.launch()
