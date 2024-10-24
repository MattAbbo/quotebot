import requests
import time

# Function to send a quote to a webhook
def send_quote_to_webhook(webhook_url, quote_data):
    response = requests.post(webhook_url, json=quote_data)
    return response.status_code

if __name__ == "__main__":
    # Replace with your actual webhook URL (for testing, use https://webhook.site/)
    webhook_url = "https://your-webhook-url.com"

    # Define a list of quotes to be sent
    quotes = [
        {"author": "Nietzsche", "quote": "That which does not kill us makes us stronger."},
        {"author": "Rilke", "quote": "Let everything happen to you, beauty and terror."},
        {"author": "Mary Oliver", "quote": "Tell me, what is it you plan to do with your one wild and precious life?"},
        {"author": "Dylan Thomas", "quote": "Do not go gentle into that good night."},
        {"author": "Emily Dickinson", "quote": "Hope is the thing with feathers."}
    ]

    # Send each quote with a 5-minute delay between them
    for quote in quotes:
        status = send_quote_to_webhook(webhook_url, quote)
        print(f"Sent quote: '{quote['quote']}' by {quote['author']}, status code: {status}")
        time.sleep(300)  # Wait for 5 minutes (300 seconds) before sending the next quote
