import json
import os

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def main():
    master_file = 'data/projects.json'
    input_file = 'input/projects.json'
    stats_file = 'output/parsed_stats.json'
    
    master_projects = load_json(master_file) or []
    input_projects = load_json(input_file) or []
    parsed_stats = load_json(stats_file) or {}
    
    # Create a set of existing links for quick lookup
    existing_links = {p['link'] for p in master_projects if 'link' in p}
    
    # Get current max created_order
    current_max_order = max([p.get('created_order', 0) for p in master_projects]) if master_projects else 0
    
    # Extract all timeframe stats for lookup
    timeframes = ['all_time', 'day', 'week', 'month']
    stats_maps = {}
    for tf in timeframes:
        stats_maps[tf] = {}
        tf_stats = parsed_stats.get(tf, [])
        for stat in tf_stats:
            title = stat['title']
            if title not in stats_maps[tf]:
                stats_maps[tf][title] = []
            stats_maps[tf][title].append(stat)

    new_projects_added = 0
    
    # Process input projects
    for p_in in input_projects:
        link = p_in.get('link')
        if link not in existing_links:
            # This is a new project
            new_project = p_in.copy()
            
            # 1. Set updated to created
            if 'created' in new_project:
                new_project['updated'] = new_project['created']
            
            # 2. Increment created_order
            current_max_order += 1
            new_project['created_order'] = current_max_order
            
            # 3. Fill tip info from stats if available
            title = new_project.get('title')
            
            # Match all_time first
            if title in stats_maps['all_time'] and stats_maps['all_time'][title]:
                # Try to match views if multiples, else take first
                best_stat = stats_maps['all_time'][title][0]
                if len(stats_maps['all_time'][title]) > 1:
                    p_views = new_project.get('views', 0)
                    min_diff = float('inf')
                    for s in stats_maps['all_time'][title]:
                        diff = abs(s['views'] - p_views)
                        if diff < min_diff:
                            min_diff = diff
                            best_stat = s
                
                new_project['tips_all_time'] = best_stat['tips']
                new_project['on_platform_all_time'] = best_stat['on_platform']
                new_project['off_platform_all_time'] = best_stat['off_platform']
                new_project['total_earnings_all_time'] = best_stat['total']
            else:
                new_project['tips_all_time'] = 0
                new_project['on_platform_all_time'] = 0
                new_project['off_platform_all_time'] = 0
                new_project['total_earnings_all_time'] = 0
                
            # Match other timeframes
            for tf in ['day', 'week', 'month']:
                if title in stats_maps[tf] and stats_maps[tf][title]:
                    # Just take the first one or logic similar to above
                    tf_stat = stats_maps[tf][title][0]
                    new_project[f'tips_{tf}'] = tf_stat['tips']
                    new_project[f'total_earnings_{tf}'] = tf_stat['total']
                else:
                    new_project[f'tips_{tf}'] = 0
                    new_project[f'total_earnings_{tf}'] = 0
            
            master_projects.append(new_project)
            new_projects_added += 1
        else:
            # Project already exists, maybe update views/likes if higher?
            # User didn't explicitly ask for this but it's good practice. 
            # I'll stick to what was asked: adding NEW ones.
            pass

    # Sort ENTIRE list by created date to assign global order
    master_projects.sort(key=lambda x: x.get('created', ''))
    
    # Assign created_order 1 to N
    for idx, project in enumerate(master_projects, 1):
        project['created_order'] = idx

    # Final sort primarily by all time total tips
    master_projects.sort(key=lambda x: (x.get('tips_all_time', 0), x.get('total_earnings_all_time', 0)), reverse=True)

    # Save master list
    with open(master_file, 'w', encoding='utf-8') as f:
        json.dump(master_projects, f, indent=2)
        
    print(f"Added {new_projects_added} new projects.")
    print(f"Total projects: {len(master_projects)}")
    print("Assigned global chronological created_order.")

if __name__ == "__main__":
    main()
