#!/usr/bin/env python3
"""
Update repository statistics (clones, forks, stars) and generate SVG chart.
Reads from/stores to .github/stats/metrics.json and generates .github/stats/metrics.svg
"""

import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, List, Optional
import argparse
from pathlib import Path

# Try to import optional dependencies, but provide fallback
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("Warning: requests module not available", file=sys.stderr)

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.ticker import MaxNLocator
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Warning: matplotlib not installed. SVG generation will use fallback.", 
          file=sys.stderr)


class RepoStatsUpdater:
    def __init__(self, token: str, repo: str, stats_dir: str = ".github/stats"):
        self.token = token
        self.repo = repo
        self.stats_dir = Path(stats_dir)
        self.stats_dir.mkdir(exist_ok=True)
        self.metrics_file = self.stats_dir / "metrics.json"
        self.svg_file = self.stats_dir / "metrics.svg"
        
    def fetch_clones_data(self) -> Optional[Dict]:
        """Fetch clones data from GitHub Traffic API"""
        if not HAS_REQUESTS:
            print("Error: requests module required for API calls", file=sys.stderr)
            return None
            
        owner, repo_name = self.repo.split('/')
        url = f"https://api.github.com/repos/{owner}/{repo_name}/traffic/clones"
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching clones data: {e}", file=sys.stderr)
            return None
    
    def fetch_repo_info(self) -> Optional[Dict]:
        """Fetch repository info to get forks and stars count"""
        if not HAS_REQUESTS:
            print("Error: requests module required for API calls", file=sys.stderr)
            return None
            
        owner, repo_name = self.repo.split('/')
        url = f"https://api.github.com/repos/{owner}/{repo_name}"
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return {
                "forks": data.get("forks_count", 0),
                "stars": data.get("stargazers_count", 0)
            }
        except Exception as e:
            print(f"Error fetching repo info: {e}", file=sys.stderr)
            return None
    
    def load_existing_data(self) -> List[Dict]:
        """Load existing metrics data from JSON file"""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {self.metrics_file}, starting fresh", 
                      file=sys.stderr)
        return []
    
    def save_data(self, data: List[Dict]):
        """Save metrics data to JSON file"""
        # Sort by date before saving
        data.sort(key=lambda x: x["date"])
        with open(self.metrics_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(data)} data points to {self.metrics_file}")
    
    def get_today_clones(self, clones_data: Dict) -> int:
        """
        Extract today's clone count from traffic data.
        Uses the count for today if available, otherwise 0.
        """
        if not clones_data or "clones" not in clones_data:
            return 0
        
        today = datetime.now(timezone.utc).date()
        today_str = today.isoformat()
        
        for clone_day in clones_data["clones"]:
            # GitHub API returns timestamps in YYYY-MM-DD format
            if clone_day["timestamp"].startswith(today_str):
                return clone_day["count"]  # Using total count
        
        return 0
    
    def update_data(self, clones_count: int, forks_count: int, stars_count: int) -> List[Dict]:
        """Update the historical data with today's metrics"""
        data = self.load_existing_data()
        today = datetime.now(timezone.utc).date().isoformat()
        
        # Check if we already have an entry for today
        existing_entry = None
        for i, entry in enumerate(data):
            if entry["date"] == today:
                existing_entry = i
                break
        
        new_entry = {
            "date": today,
            "clones": clones_count,
            "forks": forks_count,
            "stars": stars_count
        }
        
        if existing_entry is not None:
            # Update existing entry
            data[existing_entry] = new_entry
            print(f"Updated existing entry for {today}")
        else:
            # Append new entry
            data.append(new_entry)
            print(f"Added new entry for {today}")
        
        return data
    
    def generate_svg_matplotlib(self, data: List[Dict]) -> bool:
        """Generate SVG using matplotlib"""
        if not HAS_MATPLOTLIB or len(data) < 2:
            return False
        
        # Sort data by date
        data.sort(key=lambda x: x["date"])
        
        # Extract data
        dates = [datetime.strptime(d["date"], "%Y-%m-%d") for d in data]
        clones = [d["clones"] for d in data]
        forks = [d["forks"] for d in data]
        stars = [d["stars"] for d in data]
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot lines
        ax.plot(dates, clones, 'b-', label='Daily Clones', linewidth=2, marker='o', markersize=4)
        ax.plot(dates, forks, 'g-', label='Total Forks', linewidth=2, marker='s', markersize=4)
        ax.plot(dates, stars, 'r-', label='Total Stars', linewidth=2, marker='^', markersize=4)
        
        # Formatting
        ax.set_title(f'Repository Statistics: {self.repo}', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper left')
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45, ha='right')
        
        # Use integer ticks for y-axis
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save as SVG
        plt.savefig(self.svg_file, format='svg', dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"Generated matplotlib SVG chart at {self.svg_file}")
        return True
    
    def generate_svg_fallback(self, data: List[Dict]) -> bool:
        """Fallback method to generate a simple SVG without matplotlib"""
        if len(data) < 2:
            return self.generate_placeholder_svg()
        
        # Sort data
        data.sort(key=lambda x: x["date"])
        
        # Simple SVG template
        width, height = 800, 400
        margin = 50
        chart_width = width - 2 * margin
        chart_height = height - 2 * margin
        
        # Find max values for scaling
        max_clones = max(d["clones"] for d in data) or 1
        max_forks = max(d["forks"] for d in data) or 1
        max_stars = max(d["stars"] for d in data) or 1
        max_value = max(max_clones, max_forks, max_stars)
        
        # Calculate points
        points_clones = []
        points_forks = []
        points_stars = []
        
        for i, entry in enumerate(data):
            x = margin + (i / (len(data) - 1)) * chart_width
            y_clones = height - margin - (entry["clones"] / max_value) * chart_height
            y_forks = height - margin - (entry["forks"] / max_value) * chart_height
            y_stars = height - margin - (entry["stars"] / max_value) * chart_height
            
            points_clones.append(f"{x},{y_clones}")
            points_forks.append(f"{x},{y_forks}")
            points_stars.append(f"{x},{y_stars}")
        
        # Create SVG content
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .axis {{ stroke: #333; stroke-width: 1; }}
    .grid {{ stroke: #ddd; stroke-width: 0.5; stroke-dasharray: 5,5; }}
    .line-clones {{ stroke: #1f77b4; stroke-width: 2; fill: none; }}
    .line-forks {{ stroke: #2ca02c; stroke-width: 2; fill: none; }}
    .line-stars {{ stroke: #d62728; stroke-width: 2; fill: none; }}
    .dot-clones {{ fill: #1f77b4; r: 4; }}
    .dot-forks {{ fill: #2ca02c; r: 4; }}
    .dot-stars {{ fill: #d62728; r: 4; }}
    .legend {{ font-family: Arial; font-size: 12px; }}
  </style>
  
  <!-- Background -->
  <rect width="{width}" height="{height}" fill="white"/>
  
  <!-- Grid lines -->
  <line x1="{margin}" y1="{margin}" x2="{margin}" y2="{height-margin}" class="grid"/>
  <line x1="{width-margin}" y1="{margin}" x2="{width-margin}" y2="{height-margin}" class="grid"/>
  
  <!-- Axes -->
  <line x1="{margin}" y1="{height-margin}" x2="{width-margin}" y2="{height-margin}" class="axis"/>
  <line x1="{margin}" y1="{margin}" x2="{margin}" y2="{height-margin}" class="axis"/>
  
  <!-- Data lines -->
  <polyline points="{ ' '.join(points_clones) }" class="line-clones"/>
  <polyline points="{ ' '.join(points_forks) }" class="line-forks"/>
  <polyline points="{ ' '.join(points_stars) }" class="line-stars"/>
  
  <!-- Data points -->
  {''.join(f'<circle cx="{points_clones[i].split(",")[0]}" cy="{points_clones[i].split(",")[1]}" class="dot-clones"/>' for i in range(len(points_clones)))}
  {''.join(f'<circle cx="{points_forks[i].split(",")[0]}" cy="{points_forks[i].split(",")[1]}" class="dot-forks"/>' for i in range(len(points_forks)))}
  {''.join(f'<circle cx="{points_stars[i].split(",")[0]}" cy="{points_stars[i].split(",")[1]}" class="dot-stars"/>' for i in range(len(points_stars)))}
  
  <!-- Legend -->
  <g transform="translate({width-200}, {margin+20})">
    <rect x="0" y="0" width="15" height="15" fill="#1f77b4"/>
    <text x="20" y="12" class="legend">Daily Clones</text>
    
    <rect x="0" y="25" width="15" height="15" fill="#2ca02c"/>
    <text x="20" y="37" class="legend">Total Forks</text>
    
    <rect x="0" y="50" width="15" height="15" fill="#d62728"/>
    <text x="20" y="62" class="legend">Total Stars</text>
  </g>
  
  <!-- Title -->
  <text x="{width/2}" y="30" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">
    Repository Statistics: {self.repo}
  </text>
</svg>'''
        
        with open(self.svg_file, 'w') as f:
            f.write(svg_content)
        
        print(f"Generated fallback SVG chart at {self.svg_file}")
        return True
    
    def generate_placeholder_svg(self) -> bool:
        """Generate a placeholder SVG when not enough data is available"""
        width, height = 800, 400
        
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .title {{ font-family: Arial; font-size: 16px; font-weight: bold; }}
    .message {{ font-family: Arial; font-size: 14px; }}
    .data {{ font-family: Arial; font-size: 12px; }}
  </style>
  
  <!-- Background -->
  <rect width="{width}" height="{height}" fill="#f5f5f5"/>
  
  <!-- Title -->
  <text x="{width/2}" y="60" text-anchor="middle" class="title">
    Repository Statistics: {self.repo}
  </text>
  
  <!-- Message -->
  <text x="{width/2}" y="150" text-anchor="middle" class="message">
    ⏳ Collecting data... Chart will appear after 2+ days of data collection.
  </text>
  
  <!-- Current data display -->
  <g transform="translate({width/2-150}, 200)">
    <text x="0" y="0" class="data" font-weight="bold">Current Values:</text>
'''
        
        # Load current data to display
        data = self.load_existing_data()
        if data:
            latest = data[-1]
            svg_content += f'''
    <text x="0" y="30" class="data">📅 Date: {latest["date"]}</text>
    <text x="0" y="60" class="data">📊 Daily Clones: {latest["clones"]}</text>
    <text x="0" y="90" class="data">🍴 Total Forks: {latest["forks"]}</text>
    <text x="0" y="120" class="data">⭐ Total Stars: {latest["stars"]}</text>
'''
        else:
            svg_content += f'''
    <text x="0" y="30" class="data">No data available yet</text>
'''
        
        svg_content += f'''
  </g>
  
  <!-- Note -->
  <text x="{width/2}" y="350" text-anchor="middle" class="data" fill="#666">
    Chart updates daily. First chart will appear after 2 data points.
  </text>
</svg>'''
        
        with open(self.svg_file, 'w') as f:
            f.write(svg_content)
        
        print(f"Generated placeholder SVG at {self.svg_file}")
        return True
    
    def generate_svg(self, data: List[Dict]) -> bool:
        """Generate SVG chart using best available method"""
        if len(data) < 2:
            print(f"Only {len(data)} data point(s) available, generating placeholder", file=sys.stderr)
            return self.generate_placeholder_svg()
        
        # Try matplotlib first, fall back to simple SVG
        if self.generate_svg_matplotlib(data):
            return True
        
        return self.generate_svg_fallback(data)
    
    def update_readme(self):
        """Update README.md with link to the SVG"""
        readme_path = Path("README.md")
        if not readme_path.exists():
            print("README.md not found", file=sys.stderr)
            return False
        
        with open(readme_path, 'r') as f:
            content = f.read()
        
        # Define the badge section with the SVG
        svg_section = f'''
## Repository Statistics

![Repo Stats](.github/stats/metrics.svg)

*Daily clones, total forks, and total stars over time. Updated daily at 00:00 UTC.*

'''
        
        # Check if the section already exists
        if "## Repository Statistics" in content:
            # Replace existing section
            import re
            pattern = r'## Repository Statistics.*?(?=\n## |\Z)'
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, svg_section.strip(), content, flags=re.DOTALL)
            else:
                content += '\n' + svg_section
        else:
            # Add after first heading or at beginning
            if content.startswith('# '):
                # Find the end of first section
                lines = content.split('\n')
                insert_pos = 0
                for i, line in enumerate(lines[1:], 1):
                    if line.startswith('## '):
                        insert_pos = i
                        break
                if insert_pos == 0:
                    insert_pos = len(lines)
                lines.insert(insert_pos, '\n' + svg_section.strip() + '\n')
                content = '\n'.join(lines)
            else:
                # Just append
                content += '\n' + svg_section
        
        with open(readme_path, 'w') as f:
            f.write(content)
        
        print("Updated README.md with chart link")
        return True


def main():
    parser = argparse.ArgumentParser(description='Update repository statistics')
    parser.add_argument('--token', required=True, help='GitHub token')
    parser.add_argument('--repo', required=True, help='Repository in owner/name format')
    parser.add_argument('--stats-dir', default='.github/stats', help='Statistics directory')
    
    args = parser.parse_args()
    
    updater = RepoStatsUpdater(args.token, args.repo, args.stats_dir)
    
    # Fetch data
    print("Fetching clones data...")
    clones_data = updater.fetch_clones_data()
    
    print("Fetching repository info...")
    repo_info = updater.fetch_repo_info()
    
    if not repo_info:
        print("Failed to fetch repository info", file=sys.stderr)
        sys.exit(1)
    
    # Get today's clones
    clones_today = updater.get_today_clones(clones_data) if clones_data else 0
    
    # Update data
    data = updater.update_data(
        clones_count=clones_today,
        forks_count=repo_info["forks"],
        stars_count=repo_info["stars"]
    )
    
    # Save data
    updater.save_data(data)
    
    # Generate SVG (will create placeholder if not enough data)
    if updater.generate_svg(data):
        print("SVG chart generated successfully")
    else:
        print("Failed to generate SVG chart", file=sys.stderr)
        sys.exit(1)
    
    # Update README
    updater.update_readme()
    
    print("Done!")


if __name__ == "__main__":
    main()