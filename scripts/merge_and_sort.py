import json
import os

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def main():
    projects_file = 'data/projects.json'
    parsed_stats_file = 'output/parsed_stats.json'
    
    projects = load_json(projects_file)
    parsed_stats = load_json(parsed_stats_file)
    
    if not projects or not parsed_stats:
        print("Missing input files.")
        return

    # Extract all_time stats
    all_time_stats = parsed_stats.get('all_time', [])
    
    # Create a map for quick lookup: title -> list of stats
    stats_map = {}
    for stat in all_time_stats:
        title = stat['title']
        if title not in stats_map:
            stats_map[title] = []
        stats_map[title].append(stat)

    # We also want day, month, week if possible
    other_timeframes = ['day', 'week', 'month']
    other_stats_maps = {}
    for tf in other_timeframes:
        other_stats_maps[tf] = {}
        tf_stats = parsed_stats.get(tf, [])
        for stat in tf_stats:
            title = stat['title']
            if title not in other_stats_maps[tf]:
                other_stats_maps[tf][title] = []
            other_stats_maps[tf][title].append(stat)

    # Merge stats into projects
    # Since we don't have unique IDs in stats, we'll match by title.
    # To handle duplicate titles, we'll track which stats we've used for which projects.
    # A simple way is to match them in the order they appear in projects.json (which is chronological).
    # But wait, dashboard might have a different order. 
    # Let's try to match by views if there are multiples.
    
    for project in projects:
        title = project.get('title')
        if title in stats_map and stats_map[title]:
            # If multiple, find the one with closest views
            best_stat_idx = 0
            if len(stats_map[title]) > 1:
                p_views = project.get('views', 0)
                min_diff = float('inf')
                for idx, s in enumerate(stats_map[title]):
                    diff = abs(s['views'] - p_views)
                    if diff < min_diff:
                        min_diff = diff
                        best_stat_idx = idx
            
            stat = stats_map[title].pop(best_stat_idx)
            project['tips_all_time'] = stat['tips']
            project['on_platform_all_time'] = stat['on_platform']
            project['off_platform_all_time'] = stat['off_platform']
            project['total_earnings_all_time'] = stat['total']
            
            # Match other timeframes if available for the same title
            for tf in other_timeframes:
                if title in other_stats_maps[tf] and other_stats_maps[tf][title]:
                    # For simplicity, we'll take the first one or try to match views again
                    # But views won't match across timeframes. 
                    # Let's just take the first one available for that title.
                    tf_stat = other_stats_maps[tf][title].pop(0)
                    project[f'tips_{tf}'] = tf_stat['tips']
                    project[f'total_earnings_{tf}'] = tf_stat['total']
        else:
            # Initialize with 0 if no stats found
            project['tips_all_time'] = 0
            project['on_platform_all_time'] = 0
            project['off_platform_all_time'] = 0
            project['total_earnings_all_time'] = 0
            for tf in other_timeframes:
                project[f'tips_{tf}'] = 0
                project[f'total_earnings_{tf}'] = 0

    # The user wants to sort by "number of all time total tips"
    # Primarily by tips_all_time, then maybe by total_earnings_all_time as tie-breaker
    projects.sort(key=lambda x: (x.get('tips_all_time', 0), x.get('total_earnings_all_time', 0)), reverse=True)

    # Save the updated projects.json
    with open(projects_file, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2)
        
    print(f"Successfully updated and sorted {len(projects)} projects.")

if __name__ == "__main__":
    main()
