from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def assess_truthfulness(text):
    sentiment = analyzer.polarity_scores(text)
    compound_score = sentiment['compound']

    return compound_score # < -0.05 is fallacy, > 0.05 is truth, otherwise neutral

if __name__ == "__main__":
    text_input = input("Enter the text to assess its truthfulness: ")
    result = assess_truthfulness(text_input)
    print(f"Truthfulness Assessment: {result}")
