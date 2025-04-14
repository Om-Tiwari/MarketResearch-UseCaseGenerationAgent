# Market Research & Use Case Generation Agent

## Overview
The Market Research & Use Case Generation Agent is a Multi-Agent architecture system designed to generate relevant AI and Generative AI (GenAI) use cases for a given company or industry. The system conducts market research, analyzes industry trends, and provides resource assets for AI/ML solutions, focusing on enhancing operations and customer experiences.

## Architecture
The system is built using a Multi-Agent architecture with the following agents:

### 1. **Research Agent**
   - Conducts in-depth research on the industry and company.
   - Identifies key offerings, strategic focus areas, and industry trends.

### 2. **Use Case Generation Agent**
   - Analyzes research data to propose strategic AI/ML/GenAI use cases.
   - Focuses on aligning use cases with the company’s strategic goals and industry trends.

### 3. **Resource Collection Agent**
   - Searches for relevant datasets and resources to support the proposed use cases.
   - Ensures datasets are publicly available, well-documented, and domain-specific.

## Workflow
1. **Input**: Provide a topic, company, or industry to analyze.
2. **Research**: The Research Agent gathers information about the industry and company.
3. **Use Case Generation**: The Use Case Generation Agent proposes AI/ML/GenAI use cases based on the research.
4. **Resource Collection**: The Resource Collection Agent finds and saves relevant datasets for the use cases.
5. **Output**: A structured markdown file containing use cases and resource links.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Om-Tiwari/MarketResearch-UseCaseGenerationAgent.git
   cd UseCaseGenAgent
   ```
2. Install dependencies:
   ```bash
   uv sync // make sure you have uv installed already
   ```

## Usage
1. Run the main script:
   ```bash
   uv run ./main.py --topic "<TOPIC_NAME>"
   ```
2. The system will generate use cases and save the results in the `results/` directory.

OR

1. Run the app script:
   ```bash
   uv run ./app.py
   ```
2. This will open the gradio UI for interactive use

## File Structure
```
UseCaseGenAgent/
├── agent/
│   ├── researchgraph/
│   ├── resourcegraph/
│   ├── usecasegraph/
├── logs/
├── results/
├── main.py
├── README.md
├── requirements.txt
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
