# 🤖 Devoxx2025 – Azure AI Agents Workshop

Learn how to design, orchestrate, and deploy intelligent multi-agent systems using **Semantic Kernel** and **AutoGen**, powered by **Azure’s cutting-edge AI stack**.



## 📂 Repo Structure

### 📓 Semantic Kernel Orchestration 

Test out different agent capabilities interactively using Jupyter Notebooks.

- `SemanticKernel/sk-main.ipynb`  
  ➤ Create an agent using **function calling** in Semantic Kernel  
- `SemanticKernel/Plugins`  
  ➤ Contains:
  - `KnowledgeBasePlugin` 📚: Connects to your documents using Azure AI Search  
  - `LightPlugin` 💡: A basic example plugin  
  🔧 _Create your own plugin and add it to `sk-main.ipynb`!_

> ℹ️ Use the credentials in the `variables.env` file to run notebooks.



### 🧠 Python Agents

Run agent orchestration directly via scripts:

- `AIAgents/sk-agend.py`  
  ➤ Work with the **Azure AI Agent SDK** and a custom Semantic Kernel Plugin  
- `AIAgents/agents-group.py`  
  ➤ Multi-agent orchestration demo with Azure AI Agents + Semantic Kernel  

> ℹ️ Requires Azure subscription. 


## 🔗 Resources

### 🧰 Semantic Kernel
- [Getting Started with Semantic Kernel (Python)](https://github.com/microsoft/semantic-kernel/tree/main/python/samples/getting_started)
- [Multi-Agent-Custom-Automation-Engine – Solution Accelerator](https://github.com/microsoft/Multi-Agent-Custom-Automation-Engine-Solution-Accelerator/tree/main)



