#!/usr/bin/env python3
"""
Script to send crawled data to n8n webhook.
This script collects all JSON files from the ai_training_data directory,
combines them into a single payload, and sends it to the n8n webhook URL.
"""

import os
import json
import glob
import requests
from pathlib import Path
import sys

def main():
    # Get the webhook URL from environment variable
    webhook_url = os.environ.get('N8N_WEBHOOK_URL', 'http://localhost:5678/webhook-test/86260a05-9971-4baa-a4af-f9b1e60894ee')

    if not webhook_url:
        print("Error: N8N_WEBHOOK_URL environment variable is not set.")
        print("Please set the N8N_WEBHOOK_URL environment variable to the n8n webhook URL.")
        sys.exit(1)

    # Get the data directory from command line argument or use default
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "ai_training_data"
    data_path = Path(data_dir)

    if not data_path.exists() or not data_path.is_dir():
        print(f"Error: Data directory '{data_dir}' does not exist or is not a directory.")
        sys.exit(1)

    # Find all JSON files in the data directory
    json_files = glob.glob(str(data_path / "*.json"))

    if not json_files:
        print(f"No JSON files found in '{data_dir}' directory.")
        sys.exit(0)

    # Collect all data from JSON files
    all_data = []
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_data.append(data)
        except Exception as e:
            print(f"Error reading file {json_file}: {str(e)}")

    # Create the payload
    payload = {
        "data": all_data,
        "metadata": {
            "total_files": len(json_files),
            "total_items": len(all_data)
        }
    }

    # Send the data to the webhook
    try:
        print(f"Sending data to n8n webhook ({len(all_data)} items)...")
        print(f"Payload size: {len(json.dumps(payload))} bytes")

        # Print the first few characters of the webhook URL (for debugging, without revealing the full URL)
        webhook_url_prefix = webhook_url[:10] + "..." if len(webhook_url) > 10 else "..."
        print(f"Webhook URL prefix: {webhook_url_prefix}")

        # Send the request with timeout
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30  # 30 seconds timeout
        )

        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")

        if response.status_code >= 200 and response.status_code < 300:
            print(f"Success! Data sent to n8n webhook. Response: {response.status_code}")
            print(f"Response content (first 200 chars): {response.text[:200]}")
        else:
            print(f"Error sending data to webhook. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            sys.exit(1)

    except requests.exceptions.Timeout:
        print("Error: Request to n8n webhook timed out after 30 seconds")
        sys.exit(2)
    except requests.exceptions.ConnectionError as e:
        print(f"Error: Connection error when sending to n8n webhook: {str(e)}")
        sys.exit(3)
    except Exception as e:
        print(f"Error sending data to webhook: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
