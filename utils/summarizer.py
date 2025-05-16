from transformers import pipeline

# Load the summarization pipeline using a pre-trained model
# 'distilbart-cnn-12-6' is a lightweight version of BART fine-tuned for summarization
# 'framework="pt"' ensures it's using PyTorch backend
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", framework="pt")

# Function to summarize a given text
def summarize_text(text, max_length=130, min_length=30):
    try:
        # Perform summarization with specified length parameters
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        # Handle and return any errors
        return f"[Summarization failed: {e}]"
