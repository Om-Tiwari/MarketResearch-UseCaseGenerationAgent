extraction_schema = {
    "type": "object",
    "properties": {
        "companies": {
            "type": "array",
            "description": "List of companies researched",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Full legal or brand name of the company"
                    },
                    "industry_segment": {
                        "type": "string",
                        "description": "The industry and specific segment the company operates in (e.g., FinTech within Finance, or EV within Automotive)"
                    },
                    "key_offerings": {
                        "type": "string",
                        "description": "Core products, services, and solutions offered by the company"
                    },
                    "strategic_focus": {
                        "type": "string",
                        "description": "Strategic areas of focus such as innovation, operations, sustainability, supply chain, or customer experience"
                    },
                    "vision_or_mission": {
                        "type": "string",
                        "description": "A summary of the company's vision or mission statement"
                    },
                    "technologies": {
                        "type": "string",
                        "description": "Key technologies and platforms used or developed by the company"
                    },
                    "market_share": {
                        "type": "string",
                        "description": "Overview of the company’s market position or market share (qualitative or quantitative)"
                    },
                    "future_outlook": {
                        "type": "string",
                        "description": "Insights into the company’s future prospects, product roadmap, or upcoming innovations"
                    },
                    "key_powers": {
                        "type": "string",
                        "description": "Which of the 7 Powers (Scale Economies, Network Economies, Counter Positioning, Switching Costs, Branding, Cornered Resource, Process Power) describe the company's competitive advantage"
                    },
                    "industry_ai_trends": {
                        "type": "string",
                        "description": "Overview of AI/ML/Automation trends, standards, and innovations in the company's industry"
                    },
                },
                "required": [
                    "name",
                    "industry_segment",
                    "key_offerings",
                    "strategic_focus",
                    "vision_or_mission",
                    "technologies",
                    "market_share",
                    "future_outlook",
                    "key_powers",
                    "industry_ai_trends"
                ]
            }
        }
    },
    "required": ["companies"]
}
