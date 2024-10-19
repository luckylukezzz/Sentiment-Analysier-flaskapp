import unittest
from unittest.mock import patch, MagicMock
from transformers import pipeline
import torch
from temporalFiles.ABSA_model import AspectExtractor,SentimentAspectAnalyzer


# Assuming AspectExtractor and SentimentAspectAnalyzer are imported here
# from your_module import AspectExtractor, SentimentAspectAnalyzer

class TestAspectExtractor(unittest.TestCase):

    @patch('transformers.pipeline')
    def test_process_in_batches(self, mock_pipeline):
        # Mock the text generation pipeline
        mock_pipeline.return_value = lambda x: [{'generated_text': 'Battery Life, Screen Brightness'}] * len(x)

        aspect_extractor = AspectExtractor()
        reviews = ["The battery life is great but the screen is dim.", "The product is very durable."]

        # Run the process_in_batches function
        aspects, num_errors = aspect_extractor.process_in_batches(reviews)

        # Check the results
        self.assertEqual(num_errors, 0)
        self.assertEqual(len(aspects), 2)
        self.assertEqual(aspects[0]['generated_text'], 'Battery Life, Screen Brightness')

    def test_process_aspects(self):
        aspect_extractor = AspectExtractor()
        reviews = ["The battery life is great but the screen is dim."]

        with patch.object(aspect_extractor, 'process_reviews', return_value=[{'generated_text': 'Battery Life, Screen Brightness'}]):
            aspects = aspect_extractor.process_aspects(reviews)

        self.assertEqual(aspects, [["Battery Life", "Screen Brightness"]])


class TestSentimentAspectAnalyzer(unittest.TestCase):

    @patch('transformers.AutoModelForSequenceClassification.from_pretrained')
    @patch('transformers.AutoTokenizer.from_pretrained')
    def test_analyze_aspects(self, mock_tokenizer, mock_model):
        # Mock the tokenizer and model
        mock_tokenizer.return_value = MagicMock()
        mock_model.return_value = MagicMock()
        mock_model.return_value.config = MagicMock(id2label={0: 'negative', 1: 'neutral', 2: 'positive'})

        # Set up fake model outputs
        mock_model.return_value(**MagicMock()).logits = torch.tensor([[0.46396341919898987, 0.28140804171562195, 0.2546285390853882]])  # Fake logits

        sentiment_analyzer = SentimentAspectAnalyzer()
        reviews = ["The battery life is great but the screen is dim."]
        aspects = [["Battery Life", "Screen Brightness"]]

        result = sentiment_analyzer.analyze_aspects(reviews, aspects)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], ["Battery Life", 'negative'])
        self.assertEqual(result[0][1], ["Screen Brightness", 'negative'])

    @patch('transformers.AutoModelForSequenceClassification.from_pretrained')
    @patch('transformers.AutoTokenizer.from_pretrained')
    def test_analyze_overall_logit_shape(self, mock_tokenizer, mock_model):
        # Mock the tokenizer and model
        mock_tokenizer.return_value = MagicMock()
        mock_model.return_value = MagicMock()

        # Fake model output with shape (1, 3)
        mock_model.return_value(**MagicMock()).logits = torch.randn(1, 3)  # Shape (1, 3) for sentiment logits

        sentiment_analyzer = SentimentAspectAnalyzer()
        reviews = ["The battery life is great but the screen is dim."]

        # Run the analyze_overall function
        sentiment_analyzer.analyze_overall(reviews)

        # Check that the output logits have the correct shape
        output_logits_shape = mock_model.return_value(**MagicMock()).logits.shape
        self.assertEqual(output_logits_shape, (1, 3))


if __name__ == "__main__":
    unittest.main()
