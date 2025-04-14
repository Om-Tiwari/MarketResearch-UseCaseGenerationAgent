import gradio as gr
import asyncio
import os
from main import run_full_workflow
from dotenv import load_dotenv, set_key

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)


ENV_FILE = ".env"
if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)

async def process_topic(topic):
    """Run the full workflow for the given topic and return the results."""
    try:
        # Run the workflow
        await run_full_workflow(topic)

        # Find the generated result file
        result_files = [f for f in os.listdir(RESULTS_DIR) if f.endswith(".md")]
        if not result_files:
            return "No results found. Please try again with a different topic."

        # Read the latest result file
        latest_result = max(
            [os.path.join(RESULTS_DIR, f) for f in result_files], key=os.path.getctime
        )
        with open(latest_result, "r", encoding="utf-8") as file:
            result_content = file.read()

        return result_content
    except Exception as e:
        return f"An error occurred: {e}"


def run_workflow(topic):
    """Wrapper to run the async workflow in a synchronous Gradio interface."""
    return asyncio.run(process_topic(topic))


def save_env_variables(tavily_api_key, openai_api_key):
    """Save environment variables to a .env file."""
    set_key(ENV_FILE, "TAVILY_API_KEY", tavily_api_key)
    set_key(ENV_FILE, "OPENAI_API_KEY", openai_api_key)
    return (
        "Environment variables saved successfully!",
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
    )



with gr.Blocks() as app:
    gr.Markdown("# Market Research & Use Case Generation Agent")
    gr.Markdown(
        "Provide a topic, company, or industry to analyze. The system will generate AI/ML/GenAI use cases and relevant datasets."
    )

    with gr.Row():
        topic_input = gr.Textbox(
            label="Enter Topic",
            placeholder="e.g., Beauty Industry, Healthcare, Apple Inc., etc.",
        )
        submit_button = gr.Button("Generate Use Cases")

    output = gr.Markdown(
        label="Generated Results",
        value="The results will appear here...",
        min_height=300,
        show_copy_button=True,
    )

    submit_button.click(run_workflow, inputs=topic_input, outputs=output)

    with gr.Row():
        tavily_api_key = gr.Textbox(
            label="TAVILY API Key", placeholder="Enter your TAVILY API Key key"
        )
        openai_api_key = gr.Textbox(
            label="OPENAI API Key", placeholder="Enter your OPENAI API Key here"
        )
        save_button = gr.Button("Save Environment Variables")

    save_output = gr.Markdown(value="")

    save_button.click(
        save_env_variables,
        inputs=[tavily_api_key, openai_api_key],
        outputs=[
            save_output,
            tavily_api_key,
            openai_api_key,
            save_button,
        ],  # Update visibility of components
    )


if __name__ == "__main__":
    app.launch(share=False, pwa=True, debug=True)
