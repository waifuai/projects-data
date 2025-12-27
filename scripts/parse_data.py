import os
import json
import re

def parse_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
    
    # Header usually ends at the line containing "Project\tViews..."
    start_index = -1
    for i, line in enumerate(lines):
        if "Project" in line and "Views" in line and "Total" in line:
            start_index = i + 1
            break
    
    if start_index == -1:
        # Fallback if header not found exactly
        start_index = 21 

    projects = []
    i = start_index
    while i + 10 < len(lines):
        try:
            title = lines[i]
            # lines[i+1] is usually the same title
            views_str = lines[i+2].replace(',', '').strip()
            on_platform_str = lines[i+3].replace(',', '').strip()
            # i+4 is diamond
            off_platform_str = lines[i+5].replace(',', '').strip()
            # i+6 is diamond
            tips_str = lines[i+7].replace(',', '').strip()
            # i+8 is diamond
            total_str = lines[i+9].replace(',', '').strip()
            # i+10 is diamond
            
            projects.append({
                "title": title,
                "views": int(views_str) if views_str else 0,
                "on_platform": int(on_platform_str) if on_platform_str else 0,
                "off_platform": int(off_platform_str) if off_platform_str else 0,
                "tips": int(tips_str) if tips_str else 0,
                "total": int(total_str) if total_str else 0
            })
            i += 11
        except Exception as e:
            print(f"Error parsing at line {i} in {file_path}: {e}")
            i += 1 # Try to skip a line and see if we sync back up
            
    return projects

def main():
    input_dir = 'input'
    output_dir = 'output'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    all_stats = {}
    
    files = ['day.txt', 'week.txt', 'month.txt', 'all_time.txt']
    for filename in files:
        file_path = os.path.join(input_dir, filename)
        if os.path.exists(file_path):
            print(f"Parsing {filename}...")
            data = parse_txt_file(file_path)
            stats_key = filename.replace('.txt', '')
            all_stats[stats_key] = data
            
            # Save individual output as requested
            output_filename = filename.replace('.txt', '.json')
            with open(os.path.join(output_dir, output_filename), 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
    # Save combined output
    with open(os.path.join(output_dir, 'parsed_stats.json'), 'w', encoding='utf-8') as f:
        json.dump(all_stats, f, indent=2)
    
    print("Parsing complete.")

if __name__ == "__main__":
    main()
