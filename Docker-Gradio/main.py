import gradio as gr
import torch
import requests
from torchvision import transforms

model = torch.hub.load("pytorch/vision:v0.6.0", "resnet18", pretrained=True).eval()
response = requests.get("https://git.io/JJkYN")
labels = response.text.split("\n")


def predict(inp):
    inp = transforms.ToTensor()(inp).unsqueeze(0)
    with torch.no_grad():
        prediction = torch.nn.functional.softmax(model(inp)[0], dim=0)
        confidences = {labels[i]: float(prediction[i]) for i in range(1000)}
    return confidences


def run():
    demo = gr.Interface(
        fn=predict,
        inputs=gr.inputs.Image(type="pil"),
        outputs=gr.outputs.Label(num_top_classes=3),
    )

    demo.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    run()
