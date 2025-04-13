"""Tools for data enrichment.

This module contains functions that are directly exposed to the LLM as tools.
These tools can be used for tasks such as web searching and scraping.
Users can edit and extend these tools as needed.
"""

import json
from typing import Any, List, Optional, cast

import aiohttp
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg
from langgraph.prebuilt import InjectedState
from typing_extensions import Annotated

from agent.researchgraph.configuration import Configuration
from agent.researchgraph.state import State
from agent.researchgraph.utils import init_model


async def search(
    query: str, *, config: Annotated[RunnableConfig, InjectedToolArg]
) -> Optional[list[dict[str, Any]]]:
    """Query a search engine.

    This function queries the web to fetch comprehensive, accurate, and trusted results. It's particularly useful
    for answering questions about current events. Provide as much context in the query as needed to ensure high recall.
    """
    configuration = Configuration.from_runnable_config(config)
    wrapped = TavilySearchResults(max_results=configuration.max_search_results)
    result = await wrapped.ainvoke({"query": query})
    return cast(list[dict[str, Any]], result)


_INFO_PROMPT = """You are doing web research on behalf of a user. You are trying to find out this information:

<info>
{info}
</info>

You just scraped the following website: {url}

Based on the website content below, jot down some notes about the website.

<Website content>
{content}
</Website content>"""


async def scrape_website(
    url: str,
    *,
    config: Annotated[RunnableConfig, InjectedToolArg],
) -> str:
    """Scrape and summarize content from a given URL.

    Returns:
        str: A summary of the scraped content, tailored to the extraction schema.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.text()
    configuration = Configuration.from_runnable_config(config)
    p = _INFO_PROMPT.format(
        info=json.dumps(configuration.extraction_schema, indent=2),
        url=url,
        content=content[:40_000],
    )
    raw_model = init_model(config)
    result = await raw_model.ainvoke(p)
    return str(result.content)

async def store_data(
    state: Annotated[State, InjectedState],
    file_name: str,
) -> str:
    """Store data in a Markdown (.md) file.

    Args:
        file_name (str): Name of the file (without extension).
    """
    try:
        import os
        os.mkdir("results", exist_ok=True)
        data = state.info
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
        return f"Data stored successfully in {file_path}"
    except Exception as e:
        return f"Error storing data: {e}"
    