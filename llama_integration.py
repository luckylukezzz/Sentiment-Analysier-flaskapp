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
        # Debugging prints
        print("Negative Keywords:", negative_keywords)
        print("Features:", features)

        if not negative_keywords or not features:
            raise ValueError("Negative keywords or features are missing or empty.")

        prompt = """Given the negative aspects of a product and its specifications, generate improvement suggestions in the form of actionable statements.

        Input Format:

        Negative Aspects: [list of negative aspects]
        Product Specifications: {dictionary of specifications}

        Output Format:

        Negative Aspects: [list of negative aspects]
        Improvement Suggestions: [list of actionable suggestions]
        """
        try:
            result = f"{prompt}'''Negative Aspects: {negative_keywords} Product Specifications: {features}'''"
            suggestions = self.llama3_70b(result)
            return suggestions
        except Exception as e:
            print(f"Error during LLaMA model processing: {e}")
            raise

    @staticmethod
    def format_suggestions(input_text):
        lines = input_text.split('\n')
        formatted_output = []

        # Flags to identify sections
        in_negative_aspects_section = False
        in_suggestions_section = False

        for line in lines:
            # Start capturing Negative Aspects
            if line.startswith("Negative Aspects:"):
                formatted_output.append(line.strip() + "\n")
                in_negative_aspects_section = True
                in_suggestions_section = False

            # Start capturing Improvement Suggestions
            elif line.startswith("Improvement Suggestions:"):
                formatted_output.append(line.strip() + "\n")
                in_negative_aspects_section = False
                in_suggestions_section = True

            # Capture lines in Improvement Suggestions section
            elif in_suggestions_section:
                if line.startswith('[') or line.startswith(']'):
                    formatted_output.append(line.strip())
                else:
                    formatted_output.append(line.strip() + "\n")

            # End capturing if reaching the next section or end of file
            if in_negative_aspects_section and line.startswith("Improvement Suggestions:"):
                in_suggestions_section = True
                in_negative_aspects_section = False

        return ''.join(formatted_output)

        """
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
    """
