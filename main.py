from typing import Any
import uuid
from agent.researchgraph.graph import researchgraph
from agent.usecasegraph.graph import usecasegraph
from agent.resourcegraph.graph import resourcegraph
import logging
import json
import os
from langchain_core.callbacks import BaseCallbackHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("agent_workflow")

os.makedirs("logs", exist_ok=True)

# Create a proper callback handler class
class MessageLoggingHandler(BaseCallbackHandler):
    def __init__(self, message_store, agent_name):
        self.message_store = message_store
        self.agent_name = agent_name
        
    def on_chain_start(self, serialized, inputs, **kwargs):
        logger.debug(f"{self.agent_name} starting chain")
        
    def on_chain_end(self, outputs, **kwargs):
        logger.debug(f"{self.agent_name} ending chain")
        if "messages" in outputs:
            self.message_store[self.agent_name].extend(outputs["messages"])
            
    def on_agent_action(self, action, **kwargs):
        if hasattr(action, "messages") and action.messages:
            self.message_store[self.agent_name].append(action.messages)

def store_data(
    data: dict[str, Any],
    file_name: str,
) -> None:
    """Store data in a Markdown (.md) file.

    Args:
        file_name (str): Name of the file (without extension).
    """
    try:
        import os
        os.makedirs("results", exist_ok=True)
        file_name = file_name.replace(" ", "_").lower()
        file_path = f"results/{file_name}.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("#Dataset Resources\n\n")
            for use_case_entry in data.get("use_case_datasets", []):
                use_case = use_case_entry.get("use_case")
                f.write(f"## 🔹 {use_case}\n\n")
                for dataset in use_case_entry.get("datasets", []):
                    name = dataset.get("dataset_name")
                    desc = dataset.get("description")
                    platform = dataset.get("platform")
                    link = dataset.get("link")

                    f.write(f"**Dataset Name:** [{name}]({link})  \n")
                    f.write(f"**Platform:** {platform}  \n")
                    f.write(f"**Description:** {desc}\n\n")
                f.write("---\n\n")
        print(f"Data stored successfully in {file_path}")
    except Exception as e:
        print(f"Error storing data: {e}")

async def run_full_workflow(topic):
    # Dictionary to store all messages from both agents
    all_messages = {
        "research_agent": [],
        "usecase_agent": [],
        "resource_agent": [],
    }
    
    logger.info(f"Starting research workflow for topic: {topic}")
    
    # Create proper callback handler instances
    research_handler = MessageLoggingHandler(all_messages, "research_agent")
    
    # Run the research graph with proper callback handler
    research_result = await researchgraph.ainvoke(
        {"topic": topic}, 
        config={"callbacks": [research_handler]}
    )
    
    # Extract relevant info from research results
    research_info = research_result.get("info", {})
    
    # Also capture the message history from the research result if available
    if "messages" in research_result:
        all_messages["research_agent"].extend(research_result["messages"])
    
    # Log the research result summary
    logger.info(f"Research completed. Found information on topic: {topic}")
    
    # ---
    
    logger.info(f"Starting use case generation for topic: {topic}")
    
    # Create proper callback handler for usecase
    usecase_handler = MessageLoggingHandler(all_messages, "usecase_agent")
    
    # Run the usecase graph with proper callback handler
    usecase_result = await usecasegraph.ainvoke(
        {"topic": research_info},
        config={"callbacks": [usecase_handler]}
    )
    
    # Also capture the message history from the usecase result if available
    if "messages" in usecase_result:
        all_messages["usecase_agent"].extend(usecase_result["messages"])
    
    # Extract relevant info from use case results
    usecase_info = usecase_result.get("info", {})
    
    logger.info("Use Case Generation completed.")
    
    # ---
    
    logger.info("Starting to find resources for the usecases")
    
    # Create proper callback handler for usecase
    resource_handler = MessageLoggingHandler(all_messages, "resource_agent")
    
    # Run the usecase graph with proper callback handler
    resource_result = await resourcegraph.ainvoke(
        {"use_cases": usecase_info},
        config={"callbacks": [resource_handler]}
    )
    
    # Also capture the message history from the usecase result if available
    if "messages" in resource_result:
        all_messages["resource_agent"].extend(resource_result["messages"])
    
    # Extract relevant info from use case results
    resource_info = resource_result.get("info", {})
    
    store_data(resource_info, topic)
    
    logger.info("Workflow completed successfully")
    
    return {
        "topic": topic,
        "research": research_info,
        "usecases": usecase_info,
        "resources": resource_info,
        "message_history": all_messages
    }


if __name__ == "__main__":
    import asyncio

    topic = "Entertainment"
    run_id = uuid.uuid4()
    logger.info(f"Run ID: {run_id}")
    
    result = asyncio.run(run_full_workflow(topic))

    with open(f"logs/{run_id}.json", "w") as f:
        json.dump(result, f, indent=4, default=str)
    
    print(f"Message history saved to file. Total messages: Research={len(result['message_history']['research_agent'])}, Usecase={len(result['message_history']['usecase_agent'])}, Resource={len(result['message_history']['resource_agent'])}")