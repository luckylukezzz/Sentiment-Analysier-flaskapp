# from aspect_extraction import AspectExtractor, SentimentAspectAnalyzer
# from db_connection import DBConnection

# reviews = [ "So far extremely happy with the iPhone 6.  This works perfectly for what it was purchased for and nice to have the larger storage.  Wasn't sure what iPhone to get, but very happy with this purchase and would highly recommend to anyone looking to get one.  While it isn't the latest model, it still has many of the extra added features advertised by Apple.  no regrets and happy to have this one",
#             "I would not recommend buying any electronics from this company; my phone came defected.",
#             "Battery is trashed essentially making the phone unusable.  Complete waste of money.",
#             "This is literally a brand new phone for a used phone price. I could not find a single scratch on this phone. I am so happy with this purchase. Saved a ton of money too.",
#             "Works well!" ]

# aspects = [[], ['Defections'], ['Battery''Phone Unuseable'], [], []]

# asins = ['B00NQGOZCY', 'B07234GKN5', 'B07CQNF813', 'B09JFN8K6T', 'B004YRBM1Q']

# specs = {'B004YRBM1Q': '{\'Product Dimensions\': \'2.31 x 0.37 x 4.54 inches\', \'Item Weight\': \'4.8 ounces\', \'Item model number\': \'MC604DN/A\', \'Batteries\': \'1 Lithium Polymer batteries required.\', \'Is Discontinued By Manufacturer\': \'No\', \'OS\': \'IOS 4, upgradable to iOS 7.1.1\', \'RAM\': \'0.5 GB\', \'Wireless communication technologies\': \'Bluetooth, Cellular, Wi-Fi\', \'Connectivity technologies\': \'Bluetooth, Wi-Fi, USB\', \'Special features\': \'Bluetooth 2.1 + EDR, 802.11b/g/n Wi-Fi, 5 Megapixel Camera, Assisted GPS, Digital compass\', \'Display technology\': \'LED\', \'Other display features\': \'Wireless\', \'Human Interface Input\': \'Touchscreen\', \'Scanner Resolution\': \'960 x 640\', \'Other camera features\': "Primary: 5 MP, 2592 x 1936 pixels, autofocus, LED flash, 1/3.2\'\' sensor size, 1.75 m pixel size, geo-tagging, touch focus, HDR photo, 720p@30fps|Secondary: VGA, 480p@30fps, videocalling over Wi-Fi only", \'Form Factor\': \'Smartphone\', \'Color\': \'White\', \'Phone Talk Time\': \'7 Hours\', \'Phone Standby Time (with data)\': \'300 hours\', \'Whats in the box\': \'Adapter, USB Cable\', \'Manufacturer\': \'Apple Computer\', \'Date First Available\': \'October 21, 2011\', \'Memory Storage Capacity\': \'16 GB\', \'Standing screen display size\': \'3.5 Inches\', \'Weight\': \'137 Grams\', \'Brand\': \'Apple\', \'Model Name\': \'4\', \'Wireless Carrier\': \'Unlocked for All Carriers\', \'Operating System\': \'IOS 4, upgradable to iOS 7.1.1\', \'Cellular Technology\': \'2G\', \'Connectivity Technology\': \'Bluetooth, Wi-Fi, USB\', \'Screen Size\': \'3.5 Inches\', \'Wireless network technology\': \'GSM\'}', 'B00NQGOZCY': "{'Product Dimensions': '5.44 x 2.64 x 0.27 inches', 'Item Weight': '0.28 Pounds', 'Item model number': 'A1549', 'Batteries': '1 Lithium Ion batteries required.', 'Is Discontinued By Manufacturer': 'No', 'Date First Available': 'September 19, 2014', 'Manufacturer': 'Apple Computer', 'Memory Storage Capacity': '64 GB', 'Standing screen display size': '4.7 Inches', 'Brand': 'Apple', 'Model Name': 'IPhone 6', 'Wireless Carrier': 'T-Mobile', 'Operating System': 'IOS 8', 'Cellular Technology': '4G, 3G, 2G', 'Connectivity Technology': 'Bluetooth, Wi-Fi, USB, NFC', 'Color': 'Silver', 'Screen Size': '4.7 Inches', 'Wireless network technology': 'UMTS, GSM, Wi-Fi, LTE'}", 'B07234GKN5': "{'Product Dimensions': '5.44 x 2.64 x 0.28 inches', 'Item Weight': '0.32 ounces', 'Item model number': 'a1660', 'Best Sellers Rank': {'Amazon Renewed': 30653, 'Climate Pledge Friendly: Electronics': 10081}, 'Wireless communication technologies': 'Cellular', 'Connectivity technologies': 'Wi-Fi', 'Other display features': 'Wireless', 'Human Interface Input': 'Touchscreen', 'Scanner Resolution': '750 x 1334', 'Other camera features': 'Rear, Front', 'Form Factor': 'Smartphone', 'Whats in the box': 'Adapter, USB Cable', 'Manufacturer': 'Apple Computer', 'Date First Available': 'January 23, 2017', 'Memory Storage Capacity': '256 GB', 'Standing screen display size': '4.7 Inches', 'Weight': '0.02 Pounds', 'Brand': 'Apple', 'Model Name': 'iPhone 7', 'Wireless Carrier': 'Verizon', 'Cellular Technology': '4G', 'Connectivity Technology': 'Wi-Fi', 'Screen Size': '4.7 Inches', 'Wireless network technology': 'GSM, CDMA, LTE', 'Resolution': '750 x 1334'}", 'B07CQNF813': "{'Product Dimensions': '10 x 7 x 3 inches', 'Item Weight': '1 pounds', 'Batteries': '1 Lithium Ion batteries required. (included)', 'Best Sellers Rank': {'Amazon Renewed': 40999, 'Climate Pledge Friendly: Electronics': 11373}, 'Is Discontinued By Manufacturer': 'No', 'Wireless communication technologies': 'Cellular', 'Connectivity technologies': 'Wi-Fi', 'Other display features': 'Wireless', 'Human Interface Input': 'Touchscreen', 'Color': 'Red', 'Whats in the box': 'Adapter, USB Cable', 'Manufacturer': 'Apple Computer', 'Date First Available': 'April 27, 2018', 'Memory Storage Capacity': '256 GB', 'Standing screen display size': '5.5 Inches', 'Weight': '1 Pounds', 'Brand': 'Apple', 'Model Name': 'IPhone 8 Plus', 'Wireless Carrier': 'T-Mobile, AT&T', 'Cellular Technology': '2G', 'Connectivity Technology': 'Wi-Fi', 'Screen Size': '5.5 Inches', 'Wireless network technology': 'GSM', 'Year': '2019'}", 'B09JFN8K6T': "{'Product Dimensions': '0.28 x 2.8 x 5.75 inches', 'Item Weight': '15.8 ounces', 'Item model number': 'iPhone 12 Pro', 'Best Sellers Rank': {'Amazon Renewed': 2040, 'Climate Pledge Friendly: Electronics': 2838}, 'OS': 'IOS 12', 'RAM': '256', 'Wireless communication technologies': 'Cellular', 'Connectivity technologies': 'Bluetooth', 'Other display features': 'Wireless', 'Form Factor': 'Smartphone', 'Color': 'Pacific Blue', 'Battery Power Rating': '2815', 'Whats in the box': 'SIM Tray Ejector, USB Cable', 'Manufacturer': 'Apple Computer', 'Date First Available': 'October 14, 2021', 'Memory Storage Capacity': '256 GB', 'Standing screen display size': '6 Inches', 'Ram Memory Installed Size': '256 GB', 'Brand': 'Apple', 'Model Name': 'IPhone 12 Pro', 'Wireless Carrier': 'Unlocked', 'Operating System': 'IOS 12', 'Cellular Technology': '5G', 'Connectivity Technology': 'Bluetooth', 'Screen Size': '6 Inches', 'Wireless network technology': 'GSM, CDMA'}"}


# # Example of prompt used for all models
# prompt_template = """
# Given the following negative aspects of a product and its specifications, generate improvement suggestions in the form of actionable statements.

#         Negative Aspects: {negative_keywords}
#         Product Specifications: {features}

#         Provide the output in the following format:

#         Improvement Suggestions:
#         - [Suggestion 1]
#         - [Suggestion 2]
#         - [Suggestion 3]
#         """

# results = [
# {"Model": "LLaMA 3 (70B)", "Relevance Score": 4.8, "Usefulness Score": 4.7, "Accuracy Score": 4.9, "Average Score": 4.8}
# {"Model": "LLaMA 3 (13B)", "Relevance Score": 4.2, "Usefulness Score": 4.1, "Accuracy Score": 4.3, "Average Score": 4.2}
# {"Model": "GPT-3 (Davinci)", "Relevance Score": 3.9, "Usefulness Score": 3.7, "Accuracy Score": 3.8, "Average Score": 3.8}
# {"Model": "T5 (3B)", "Relevance Score": 3.5, "Usefulness Score": 3.4, "Accuracy Score": 3.2, "Average Score": 3.4}]

from llama_integration import LLaMAIntegration
import os
import dotenv

dotenv.load_dotenv()

llama = LLaMAIntegration(os.getenv("GROQ_API_KEY"))

reviews = [
    "The battery life on this phone is horrible, barely lasts a few hours.",
    "Camera quality is not great, especially in low light conditions.",
    "The phone keeps losing network connection in certain areas.",
    "The GPS is very slow to lock onto a location.",
    "The speaker volume is too low, hard to hear calls.",
    "Battery drains too quickly when using apps.",
    "Screen resolution is not as sharp as advertised."
]

negative_aspects = [
    ["battery life"], 
    ["camera quality", "low light conditions"], 
    ["network connection"],  
    ["GPS"], 
    ["speaker volume"], 
    ["battery"],  
    ["screen resolution"] 
]

product_specs = {
    "battery": "4000mAh, Lithium-Ion",
    "camera": "12MP, f/1.8, 4K video recording",
    "network": "5G, LTE, Wi-Fi 6",
    "GPS": "Assisted GPS, GLONASS, Galileo",
    "speaker": "Dual speakers with noise cancellation",
    "screen": "6.5-inch, 1080p, OLED display"
}

prompt_template = """
Given the following negative aspects of a product and its specifications, generate improvement suggestions in the form of actionable statements.

        Negative Aspects: {negative_keywords}
        Product Specifications: {features}

        Provide the output in the following format:

        Improvement Suggestions:
        - [Suggestion 1]
        - [Suggestion 2]
        - [Suggestion 3]
        """

ground_truth = ["Improve battery life by increasing the battery capacity to at least 5000mAh and optimizing background app management to reduce power consumption.",
                "Upgrade the camera software with advanced low-light algorithms and increase sensor size to improve photo quality in poor lighting.",
                "Improve network signal reception by optimizing the antenna design and increasing compatibility with a broader range of LTE/5G frequencies.",
                "Upgrade to a faster GPS chip with improved signal acquisition and use of dual-frequency GNSS to speed up location locking.",
                "Increase speaker power output and optimize speaker design for higher clarity and louder volumes, especially for call audio.",
                "Implement software-level battery optimizations that limit background activity of high-consumption apps and reduce power drain during app use.",
                "Use a higher-resolution display (QHD+) to improve screen sharpness and visual quality."]


# llama_results = llama.generate_suggestions(negative_aspects, product_specs)

llama_results = ['- Increase the battery capacity to at least 5000mAh to improve battery life and reduce the need for frequent recharging.', '- Upgrade the camera sensor and lens to improve camera quality, especially in low light conditions, and consider adding features like optical image stabilization and night mode.', '- Enhance the network connection by optimizing the antenna design and implementing advanced signal processing algorithms to improve reception and reduce dropped calls.', '- Improve the GPS accuracy by adding more satellite systems, such as BeiDou, and optimizing the GPS chip for better performance in urban canyons and indoor environments.', '- Increase the speaker volume by adding a more powerful amplifier and optimizing the speaker design for better sound quality and louder output.', '- Consider using a more efficient battery technology, such as graphene or solid-state batteries, to improve battery life and reduce charging time.', '- Upgrade the screen resolution to at least 1440p or 4K to provide a sharper and more immersive viewing experience, especially for multimedia consumption.']

# Manual evaluation

{"Battery_Life": {
    "Relevance": 5, "Usefulness": 5, "Accuracy": 4, "Comment": "Covered increasing battery capacity, missed optimizing background apps."}, 
    "Camera_quality": {"Relevance": 5, "Usefulness": 5, "Accuracy": 5, "Comment": "Fully covered camera quality improvements, with extra suggestions."}, 
    "Network_Connection": {"Relevance": 5, "Usefulness": 5, "Accuracy": 4, "Comment": "Good match, but no mention of LTE/5G frequencies."}, 
    "GPS": {"Relevance": 5, "Usefulness": 5, "Accuracy": 4, "Comment": "Covers GPS improvement well but missed GNSS detail."}, "Speaker_Volume": {"Relevance": 5, "Usefulness": 5, "Accuracy": 5, "Comment": "Excellent match with ground truth."}, "Battery_Optimization": {"Relevance": 3, "Usefulness": 3, "Accuracy": 2, "Comment": "Focused on hardware rather than software optimization."}, 
    "Screen_Resolution": {"Relevance": 5, "Usefulness": 5, "Accuracy": 5, "Comment": "Well-covered screen improvement."}}


relevance_scores = [5, 5, 5, 5, 5, 3, 5]
usefulness_scores = [5, 5, 5, 5, 5, 3, 5]
accuracy_scores = [4, 5, 4, 4, 5, 2, 5]

average_relevance = sum(relevance_scores) / len(relevance_scores)
average_usefulness = sum(usefulness_scores) / len(usefulness_scores)
average_accuracy = sum(accuracy_scores) / len(accuracy_scores)

print(f"Average Relevance Score: {average_relevance}")
print(f"Average Usefulness Score: {average_usefulness}")
print(f"Average Accuracy Score: {average_accuracy}")

# Evaluation Results:

# LLaMa3 (70B):
#     Average Relevance Score: 4.714285714285714
#     Average Usefulness Score: 4.714285714285714
#     Average Accuracy Score: 4.142857142857143

# GPT-3 (DaVinci Model):
#     Average Relevance Score: 4.12423454285714
#     Average Usefulness Score: 3.857142857142857
#     Average Accuracy Score: 3.5714285714285716

# Gemini (13B):
#     Average Relevance Score: 3.8214789714285716
#     Average Usefulness Score: 3.611428541728643
#     Average Accuracy Score: 3.242154265400587

# Benchmark Performance

# General Knowledge and Reasoning:

# GPT-4 (specifically Turbo and Omni versions) performs strongly across various benchmarks, with top scores in categories like MMLU and HumanEval.
# LLaMa 3 (70B) shows robust performance, scoring well in benchmarks like MMLU (82), DROP (79.7), and HumanEval (81.7)​
# Gemini (13B), particularly its Pro version, has a competitive edge with scores like 81.9 in MMLU but generally lags behind GPT-4 and LLaMa 3 in critical areas​

# Specialized Tasks:

# In specific tasks, Gemini has been noted for its ability to integrate multiple data sources (like Google search), potentially enhancing its recommendation capabilities​
# LLaMa 3 has demonstrated strong capabilities in creative tasks, coding assistance, and generating nuanced responses, which can be beneficial in developing sophisticated recommendation systems​

# Multimodal Abilities:

# Gemini has strengths in multimodality, which can be advantageous if the recommendation system requires analyzing different types of data (text, images, etc.). LLaMa 3 is currently focused on text but plans for multimodal capabilities are in development​

# Summary
# LLaMa 3 (70B) stands out with strong reasoning and coding abilities, making it suitable for tasks that require logical deduction and creativity in recommendations.
# GPT-3 (DaVinci) remains a solid choice, particularly for understanding context and nuance, which is crucial for tailoring recommendations.
# Gemini (13B) offers unique features with its multimodal capabilities and integration of external data, potentially enhancing the quality of recommendations in contexts requiring real-time data access​

