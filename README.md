
# Docker Starter Projects for AI:

1. Streamlit: https://huggingface.co/spaces/DockerTemplates/streamlit-docker-example
2. Gradio: https://huggingface.co/spaces/sayakpaul/demo-docker-gradio
3. HTTP w GO: https://huggingface.co/spaces/XciD/test-docker-go?q=Adrien
4. Secrets: https://huggingface.co/spaces/DockerTemplates/secret-example
5. Fast API: https://huggingface.co/spaces/DockerTemplates/fastapi_t5


# Github Actions Deploy to ACA:

🐋 Create a Dockerfile for Gradio deployment 🐋

1️⃣ Start by specifying the base image for your container. For Python:

FROM python:3.8-slim-buster

2️⃣ Set the working directory for the container and copy the necessary files:

WORKDIR /app
COPY . /app

3️⃣ Install the necessary dependencies, including Gradio:

RUN pip install --upgrade pip && \
    pip install gradio

4️⃣ Specify the command to run when the container starts:

CMD ["python", "app.py"]

:rocket: Build and push your container image to Azure Container Registry :rocket:

:green_book: Set up a GitHub Actions workflow for deployment :green_book:

Use azure/login action for Azure authentication and azure/container-apps-deploy-action for deployment. Provide necessary inputs like container app name, Azure Container Registry name, and container image tag.

Here's an example GitHub Actions workflow:
name: Deploy to Azure Container Apps

on: push: branches: - main

env: AZURE_CONTAINER_APP_NAME: AZURE_CONTAINER_REGISTRY_NAME: IMAGE_TAG: ${{ github.sha }}

jobs: deploy: runs-on: ubuntu-latest steps: - name: Check out code uses: actions/checkout@v2

  - name: Login to Azure
    uses: azure/login@v1
    with:
      creds: ${{ secrets.AZURE_CREDENTIALS }}

  - name: Deploy to Azure Container Apps
    uses: azure/container-apps-deploy-action@v1
    with:
      containerAppName: ${{ env.AZURE_CONTAINER_APP_NAME }}
      imageName: ${{ env.AZURE_CONTAINER_REGISTRY_NAME }}.azurecr.io/myimage:${{ env.IMAGE_TAG }}
	
:arrow_forward: **After your GitHub Actions workflow is set up, follow these steps to get your app running on Azure Container Apps** :arrow_forward:

5️⃣ **Commit and push your changes** :file_folder:

Once you've made all necessary changes to your Dockerfile and GitHub Actions workflow file, commit and push them to your repository. 

```bash
git add .
git commit -m "Setup Dockerfile and GitHub Actions workflow"
git push origin main
6️⃣ Watch your GitHub Actions workflow 👀

Go to the "Actions" tab in your GitHub repository to see your workflow in action. If everything is set up correctly, you should see your workflow running and completing without errors.

7️⃣ Check your app on Azure Container Apps 🏁

Once the GitHub Actions workflow has completed, your app should be deployed to Azure Container Apps. You can check the status of your app in the Azure portal.

8️⃣ Enjoy your Gradio app running smoothly on Azure Container Apps 🎉

You've successfully deployed your Gradio app to Azure Container Apps using a Docker container and GitHub Actions!
