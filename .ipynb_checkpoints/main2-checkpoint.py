import requests
import time
import csv

import requests
import time
import csv

def extract_contest_leaderboard(contest_slug, pages_to_fetch=5):
    """
    Extracts the leaderboard for a specific LeetCode contest.
    """
    base_url = f"https://leetcode.com/contest/api/ranking/{contest_slug}/"
    leaderboard = []
    
    # --- NEW: Add browser headers to bypass the 403 Forbidden error ---
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"https://leetcode.com/contest/{contest_slug}/ranking/"
    }
    
    print(f"Starting extraction for {contest_slug}...")
    
    for page in range(1, pages_to_fetch + 1):
        params = {
            'pagination': page,
            'region': 'global'
        }
        
        try:
            # --- NEW: Pass the headers into the request ---
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status() 
            
            data = response.json()
            users = data.get('total_rank', [])
            
            if not users:
                print(f"No more data found at page {page}. Stopping.")
                break
                
            for user in users:
                leaderboard.append({
                    'Rank': user.get('rank'),
                    'Username': user.get('username'),
                    'Score': user.get('score'),
                    'Finish Time (Unix)': user.get('finish_time'),
                    'Country': user.get('country_name') or 'Unknown'
                })
                
            print(f"Successfully scraped page {page}")
            time.sleep(1) 
            
        except requests.exceptions.RequestException as e:
            print(f"An error occurred on page {page}: {e}")
            break
            
    return leaderboard

def save_to_csv(data, filename):
    """Saves the extracted list of dictionaries to a CSV file."""
    if not data:
        print("No data to save.")
        return
        
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
        
    print(f"\nSuccess! Leaderboard saved to {filename}")

if __name__ == "__main__":
    # --- CONFIGURATION ---
    # Replace with your target contest slug
    TARGET_CONTEST = "weekly-contest-491" 
    
    # Define how many pages you want (LeetCode shows 25 users per page)
    # 4 pages = Top 100 users
    PAGES_TO_SCRAPE = 4 
    
    # --- EXECUTION ---
    scraped_data = extract_contest_leaderboard(TARGET_CONTEST, PAGES_TO_SCRAPE)
    save_to_csv(scraped_data, f"{TARGET_CONTEST}_top_100.csv")