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

    # GraphQL query to get all contributions (commits, PRs, issues)
    query = """
    query($username: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $username) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """
    
    variables = {
        "username": username,
        "from": f"{year}-01-01T00:00:00Z",
        "to": f"{year}-12-31T23:59:59Z"
    }
    
    response = requests.post(
        "https://api.github.com/graphql",
        headers=headers,
        json={"query": query, "variables": variables}
    )
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from GitHub", "details": response.text}), response.status_code
        
    data = response.json()
    if "errors" in data:
        return jsonify({"error": "GraphQL error", "details": data["errors"]}), 400
        
    calendar = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    total_activities = calendar["totalContributions"]
    
    # Restructure into our existing format for the frontend
    prs_by_date = {}
    for week in calendar["weeks"]:
        for day in week["contributionDays"]:
            date_str = day["date"].split("T")[0]
            count = day["contributionCount"]
            if count > 0:
                # Mock PR entries to keep frontend structure compatible
                prs_by_date[date_str] = [{"title": "Atividade", "state": "merged"} for _ in range(count)]
    
    stats = {"open": 0, "closed": 0, "merged": total_activities}

    return jsonify({
        "username": username,
        "year": year,
        "total_prs": total_activities,
        "stats": stats,
        "prs_by_date": prs_by_date
    })

if __name__ == '__main__':
    app.run(debug=True)
