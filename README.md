# World Bank Research Assistant
## Project Overview
For this project, I built an AI agent that retrieves and analyzes World Bank data. I used Ollama and Qwen3 to understand questions, create plans, and use different tools to answer them.
## Features
- Retrieve World Bank data
- Compare data between countries
- Calculate percentage changes
- Remember previous questions
- Use offline data when needed
- Structured planning with Pydantic
- Error handling
- MCP integration
- Track the agent's actions
## Installation
Install the requirements:
```bash
pip install -r requirements.txt
```
Download the model:
```bash
ollama pull qwen3:4b
```
## Running the Agent
```bash
python agent.py
```
## Example Questions
- What was the population of the United States in 2022?
- Compare the population of the United States and Canada in 2022.
- How did the population of the United States change between 2010 and 2022?
- What about Canada?
## Evaluation
```bash
python evaluate.py
```
My first evaluation passed 4 out of 5 tests with an 80% success rate. The model failed one test because it returned an incorrect year. After making changes to the prompt, I ran the evaluation again and passed all 5 tests with a 100% success rate.
## MCP Integration
I created an MCP server that allows a client to access four different tools. These tools search for indicators, retrieve data, compare values, and calculate percentage changes.
To test the connection:
```bash
python test_mcp.py
```
## Engineering Decisions
I decided to use a local model so I wouldn't need to pay for an AI API. I used Pydantic to organize the agent's plans and separate Python functions to retrieve data and perform calculations.
I also disabled thinking mode because the model was taking too long to respond on my CPU.
## Limitations
The model can still make mistakes when generating plans. The offline data can also be different from the live World Bank data. Although my final evaluation passed all five tests, more testing would be needed to determine how reliable the agent is.
## Conclusion
This project helped me understand how AI agents use tools, remember information, and complete tasks. I also learned how important testing and improving prompts are when building an AI agent.
## AI Assistance
I used ChatGPT to help improve Python code, troubleshoot errors, evaluate the evaluation tests. It also helped me set up MCP.
I ran the application and tests on my computer, reviewed the results, and made changes when errors occurred. Using AI helped me better understand how the agent works and how to troubleshoot problems.