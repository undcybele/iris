import gradio as gr
from biometric_system import system_main

def greet(name):
    return "Hello " + name + "!"

if __name__ == '__main__':
  add = gr.Interface(fn=greet, inputs="text", outputs="text")

  delete = gr.Interface(fn=greet, inputs="text", outputs="text")
  
  identify = gr.Interface(
    system_main,
    gr.Image(source="webcam", streaming=True), 
      "image",
    live=True
  )

  

  demo = gr.TabbedInterface([add, delete, identify], ["Add user", "Delete user", "Identify"])
  demo.launch()
  #system_main('iris/114_5.jpeg')
