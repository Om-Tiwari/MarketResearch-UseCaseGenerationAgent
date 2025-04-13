extraction_schema = {
    "type": "object",
    "properties": {
        "use_case_datasets": {
            "type": "array",
            "description": "List of use cases and their relevant datasets",
            "items": {
                "type": "object",
                "properties": {
                    "use_case": {
                        "type": "string",
                        "description": "The name or description of the specific use case"
                    },
                    "datasets": {
                        "type": "array",
                        "description": "Relevant datasets for the use case",
                        "items": {
                            "type": "object",
                            "properties": {
                                "dataset_name": {
                                    "type": "string",
                                    "description": "Title or name of the dataset"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Short summary or abstract of what the dataset contains"
                                },
                                "platform": {
                                    "type": "string",
                                    "description": "The source or platform where the dataset is hosted (e.g., Kaggle, HuggingFace, GitHub)"
                                },
                                "link": {
                                    "type": "string",
                                    "description": "Direct link to access or download the dataset"
                                }
                            },
                            "required": ["dataset_name", "description", "platform", "link"]
                        }
                    }
                },
                "required": ["use_case", "datasets"]
            }
        }
    },
    "required": ["use_case_datasets"]
}
