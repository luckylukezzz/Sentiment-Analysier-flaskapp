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

        if not negative_keywords or not features:
            raise ValueError("Negative keywords or features are missing or empty.")

        # Updated prompt
        prompt = f"""
        Given the following negative aspects of a product and its specifications, generate improvement suggestions in the form of actionable statements.

        Negative Aspects: {negative_keywords}
        Product Specifications: {features}

        Provide the output in the following format:

        Improvement Suggestions:
        - [Suggestion 1]
        - [Suggestion 2]
        - [Suggestion 3]
        """

        try:
            # Generate the suggestions using LLaMA
            result = self.llama3_70b(prompt)

            # Process the result to extract suggestions
            suggestions = self.extract_suggestions(result)
            return suggestions

        except Exception as e:
            print(f"Error during LLaMA model processing: {e}")
            raise

    def extract_suggestions(self, model_output):
        suggestions = []
        lines = model_output.split('\n')

        for line in lines:
            if line.startswith('-'):
                suggestions.append(line.strip())

        return suggestions


    # @staticmethod
    # def format_suggestions(input_text):
    #     lines = input_text.split('\n')
    #     formatted_output = []
        
    #     # Flags to identify sections
    #     in_negative_aspects_section = False
    #     in_suggestions_section = False

    #     for line in lines:
    #         # Start capturing Negative Aspects
    #         if line.startswith("Negative Aspects:"):
    #             formatted_output.append(line.strip() + "\n")
    #             in_negative_aspects_section = True
    #             in_suggestions_section = False

    #         # Start capturing Improvement Suggestions
    #         elif line.startswith("Improvement Suggestions:"):
    #             formatted_output.append(line.strip() + "\n")
    #             in_negative_aspects_section = False
    #             in_suggestions_section = True

    #         # Capture lines in Improvement Suggestions section
    #         elif in_suggestions_section:
    #             if line.startswith('[') or line.startswith(']'):
    #                 formatted_output.append(line.strip())
    #             else:
    #                 formatted_output.append(line.strip() + "\n")
            
    #         # End capturing if reaching the next section or end of file
    #         if in_negative_aspects_section and line.startswith("Improvement Suggestions:"):
    #             in_suggestions_section = True
    #             in_negative_aspects_section = False

    #     return ''.join(formatted_output)

    def format_suggestions(input_text):
        lines = input_text.split('\n')
        print(lines)
        suggestions = []
        
        # Flag to identify the Improvement Suggestions section
        in_suggestions_section = False

        for line in lines:
            # Start capturing Improvement Suggestions
            if line.startswith('Improvement Suggestions:'):
                in_suggestions_section = True
                continue  # Skip the header itself
            
            # Capture lines in the Improvement Suggestions section
            if in_suggestions_section:
                print(line)
                if line.startswith('-'):  # Each suggestion starts with '-'
                    suggestions.append(line.strip())

        return suggestions


