import gradio as gr
from biometric_system import system_main
from users.user_utils import create_user
from users.user_utils import delete_user

if __name__ == '__main__':
  add = gr.Interface(fn=create_user, inputs=["text", "text"], outputs="text")

  delete = gr.Interface(fn=delete_user, inputs="text", outputs="text")
  
  identify = gr.Interface(
    system_main,
    gr.Image(type="filepath"),
    "text"
  )

  demo = gr.TabbedInterface([add, delete, identify], ["Add user", "Delete user", "Identify"])
  demo.launch(share=True)
  #system_main('iris/114_5.jpeg')
