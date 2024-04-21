import gradio as gr

def test(x):
    return x

iface = gr.Interface(test, "textbox", "textbox")
iface.launch(server_name="0.0.0.0", server_port=1234)