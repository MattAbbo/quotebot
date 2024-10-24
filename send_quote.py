import os
import requests
import random
from supabase import create_client, Client

# Initialize the Supabase client using environment variables
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to get a random quote
def get_random_quote():
    response = supabase.table('quotes').select('*').execute()
    quotes = response.data
    if quotes:
        return random.choice(quotes)  # Select a random quote
    else:
        return None

# Function to increment the sent count
def increment_sent_count(quote_id):
    supabase.table('quotes').update({'sent_count': 'sent_count + 1'}).eq('id', quote_id).execute()

# Function to send a quote to a webhook
def send_quote_to_webhook(webhook_url, quote):
    data = {
        "author": quote['author'],
        "quote": quote['quote']
    }
    response = requests.post(webhook_url, json=data)
    return response.status_code

if __name__ == "__main__":
    webhook_url = "https://your-webhook-url.com"  # Replace with your webhook URL
    random_quote = get_random_quote()

    if random_quote:
        # Send the quote to the webhook
        status = send_quote_to_webhook(webhook_url, random_quote)
        print(f"Sent quote: '{random_quote['quote']}' by {random_quote['author']}, status code: {status}")

        # Increment the sent count in the database
        increment_sent_count(random_quote['id'])
    else:
        print("No quotes available")
