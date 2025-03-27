# AIDEL Hackathon: AI Entity and Risk Analysis Solution

Welcome to our submission for the AIDEL Hackathon! We are Team Chatgplt, and this project is our AI Entity and Risk Analysis Solution.

<img width="1256" alt="Image" src="https://github.com/user-attachments/assets/8b503ae0-bf94-4cc0-bd26-94089e1fc318" />

[Watch the Demo Video on YouTube](https://youtu.be/Ayy3oX778Nk)

## Project Overview

This project is designed to process transaction data, analyze risks, and identify entities of interest using AI techniques. The solution includes a Flask application for backend processing and a UI located in the `HACK UI` folder.

## Features

- **Flask Backend**: Processes transaction data and performs risk analysis.
- **UI**: Located in the `HACK UI` folder, providing a user-friendly interface.
- **Python Notebook**: Used to find the person of interest, located in the `notebooks` directory.
- **LLM Models**: OpenAI GPT-4-mini (entity extrcation and research agent), Gemini-2.0-flash (RAG search), llama-3.3-70b-versatile (Risk Reasoning)

[Sample research output](artifacts\research_output_by_agent\output1.md)

## Getting Started

### Prerequisites

- Python 3.x
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```

4. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Download the spaCy model**
   ```bash
   python -m spacy download en_core_web_lg
   ```

6. **Set up the environment variables**
   - Copy `sample.env` to `.env` and update the values as needed.
   - Ensure you have an ngrok authtoken to allow the Flask app to access the Colab notebook.

### Running the Flask App

1. **Start the Flask application** (Working dir: src)
   ```bash
   python app.py
   ```

2. **Access the application**
   - Open your web browser and go to `http://localhost:8002`

### UI

- The UI is located in the `HACK UI` folder. Follow the instructions in the folder to start the UI.

### Python Notebook

- The notebook for finding the person of interest is located in the `notebooks` directory. Open it with Jupyter Notebook or any compatible environment.
- The Colab notebook is used for resource-intensive code and is preferred for headless scraping.
- Run all the cells in the os_scrape.ipynb in Google Colab , which is a flask app, copy the url from there and replace the url in persons_norm() and entities_norm()<br><br>
(Inorder to improve the performance of the application, we leveraged Google collab and its compute power and that is why a separate flask app here)

## Team

- Team Chatgplt
   * [Arnav Banerjee](https://www.linkedin.com/in/arnav-banerjee-66b0b5197)
   * [Sai Pranav Baratam](https://www.linkedin.com/in/sai-pranav-baratam-1325971b3)
   * [Mounvi Podapati](https://www.linkedin.com/in/mounvi-podapati-900a841a0)
   * [Madhumitha JR](https://www.linkedin.com/in/madhumithajr)
   * [Gerosh Shibu George](https://www.linkedin.com/in/gerosh-shibu-george)

We hope you enjoy exploring our solution! If you have any questions or feedback, feel free to reach out. 
