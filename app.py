import os
from datetime import datetime
import requests
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/prs/<username>')
def get_user_prs(username):
    year = request.args.get('year', str(datetime.now().year))
    
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    # We use GitHub's Search API to find Pull Requests authored by the user
    # Query: type:pr author:<username> created:<year>-01-01..<year>-12-31
    # We will fetch all PRs (handling pagination)
    
    prs = []
    page = 1
    per_page = 100
    
    while True:
        query = f"type:pr author:{username} created:{year}-01-01..{year}-12-31"
        url = f"https://api.github.com/search/issues?q={query}&per_page={per_page}&page={page}"
        
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch data from GitHub", "details": response.json()}), response.status_code
            
        data = response.json()
        items = data.get("items", [])
        
        if not items:
            break
            
        for item in items:
            # item is an issue object, but we filtered by type:pr
            created_at = item["created_at"]
            date_str = created_at.split("T")[0]
            
            state = item["state"]
            pr_info = item.get("pull_request", {})
            if state == "closed" and pr_info.get("merged_at"):
                state = "merged"
            
            prs.append({
                "title": item["title"],
                "url": item["html_url"],
                "state": state,
                "date": date_str,
                "created_at": created_at
            })
            
        if len(items) < per_page:
            break
            
        page += 1

    # Group by date and calculate stats
    prs_by_date = {}
    stats = {"open": 0, "closed": 0, "merged": 0}
    
    for pr in prs:
        date = pr["date"]
        if date not in prs_by_date:
            prs_by_date[date] = []
        prs_by_date[date].append(pr)
        
        state = pr["state"]
        if state in stats:
            stats[state] += 1

    return jsonify({
        "username": username,
        "year": year,
        "total_prs": len(prs),
        "stats": stats,
        "prs_by_date": prs_by_date
    })

if __name__ == '__main__':
    app.run(debug=True)
