############## LLaMA Integration to generate improvement suggestions ##############

import os
from groq import Groq

class LLaMAIntegration:
    def __init__(self, api_token):
        os.environ["GROQ_API_KEY"] = api_token
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def llama3_70b(self, prompt, temperature=0.0):
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192",
            temperature=temperature,
        )
        return chat_completion.choices[0].message.content

    def generate_suggestions(self, negative_keywords, features):
        prompt = """Given the negative aspects of a product and its specifications, generate improvement suggestions in the form of actionable statements.

        Input Format:

        Negative Aspects: [list of negative aspects]
        Product Specifications: {dictionary of specifications}

        Output Format:

        Negative Aspects: [list of negative aspects]
        Improvement Suggestions: [list of actionable suggestions]
        """
        result = f"{prompt}'''Negative Aspects: {negative_keywords} Product Specifications: {features}'''"
        suggestions = self.llama3_70b(result)
        return suggestions

    @staticmethod
    def format_suggestions(input_text):
        lines = input_text.split('\n')
        formatted_output = []

        in_suggestions_section = False

        for line in lines:
            if line.startswith("**Negative Aspects:**"):
                formatted_output.append("Improvement Suggestions\n")
                formatted_output.append("Negative Aspects Identified:\n")
                in_suggestions_section = False

            elif line.startswith("* "):
                formatted_output.append(f"- {line[2:]}\n")

            elif line.startswith("Product Specifications:"):
                formatted_output.append("\nProduct Specifications:\n")
                in_suggestions_section = False

            elif line[0].isdigit() and line[1] == '.':
                if not in_suggestions_section:
                    formatted_output.append("\nSuggestions for Improvement:\n")
                    in_suggestions_section = True
                formatted_output.append(f"{line}\n")

            else:
                formatted_output.append(line.strip() + "\n")

        return ''.join(formatted_output)
