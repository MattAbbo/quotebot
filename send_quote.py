import os
import requests
import random
from supabase import create_client, Client

# Initialize the Supabase client using environment variables
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to get a random unsent quote (sent_count = 0)
def get_random_unsent_quote():
    response = supabase.table('quotes').select('*').eq('sent_count', 0).execute()
    quotes = response.data
    if quotes:
        return random.choice(quotes)  # Select a random unsent quote
    else:
        return None

# Function to increment the sent count for a specific quote
def increment_sent_count(quote_id):
    # First, get the current sent_count for the quote
    response = supabase.table('quotes').select('sent_count').eq('id', quote_id).single().execute()
    current_count = response.data['sent_count']
    
    # Increment the sent_count by 1
    new_count = current_count + 1

    # Update the quote with the new sent_count
    supabase.table('quotes').update({'sent_count': new_count}).eq('id', quote_id).execute()

# Function to send a quote to a webhook
def send_quote_to_webhook(webhook_url, quote):
    data = {
        "author": quote['author'],
        "quote": quote['quote']
    }
    response = requests.post(webhook_url, json=data)
    return response.status_code

# Function to reset all sent_count values to 0 (when all quotes have been sent)
def reset_sent_counts():
    # Fetch all quotes
    response = supabase.table('quotes').select('id').execute()
    quotes = response.data
    
    # Loop through each quote and reset its sent_count
    for quote in quotes:
        supabase.table('quotes').update({'sent_count': 0}).eq('id', quote['id']).execute()

if __name__ == "__main__":
    webhook_url = "https://webhook.site/e2c2b183-d14c-4c7a-8dab-0b15d2d94f80"  # Replace with your webhook URL

    # Get a random unsent quote
    random_quote = get_random_unsent_quote()

    if random_quote:
        # Send the quote to the webhook
        status = send_quote_to_webhook(webhook_url, random_quote)
        print(f"Sent quote: '{random_quote['quote']}' by {random_quote['author']}, status code: {status}")

        # Increment the sent count in the database
        increment_sent_count(random_quote['id'])
    else:
        # No unsent quotes available, reset all sent_count values
        print("No unsent quotes available. Resetting all sent counts.")
        reset_sent_counts()
