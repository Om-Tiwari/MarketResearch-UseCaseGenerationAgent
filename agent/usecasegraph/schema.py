extraction_schema = {
    "type": "object",
    "properties": {
        "companies": {
            "type": "array",
            "description": "List of companies for which use cases and trends are identified",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Company name"
                    },
                    "proposed_use_cases": {
                        "type": "array",
                        "description": "List of relevant and practical AI/ML/GenAI/LLM use cases tailored to the company",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "Short title of the use case"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Detailed explanation of the use case, including how it works and its benefits"
                                },
                                "impact_area": {
                                    "type": "string",
                                    "description": "The strategic focus area it improves (e.g., operations, customer experience, supply chain)"
                                },
                                "technology": {
                                    "type": "string",
                                    "description": "What type of AI/ML/GenAI/LLM technology is involved"
                                }
                            },
                            "required": ["title", "description", "impact_area", "technology"]
                        }
                    }
                },
                "required": ["name", "proposed_use_cases"]
            }
        }
    },
    "required": ["companies"]
}
