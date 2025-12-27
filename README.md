# Projects Data 📊

Welcome to the **projects-data** repository! This project serves as a central hub for datasets related to WebSim projects and WaifuAI GitHub repositories. It provides structured JSON data that can be used for analysis, visualization, or integration into other applications.

## 📂 Data Overview

The core of this repository lies in the `data/` directory, which contains snapshot data of projects and repositories.

| File | Description |
| :--- | :--- |
| `data/projects.json` | A collection of projects from WebSim, including metadata like views, likes, and descriptions. |
| `data/github.json` | A curated list of GitHub repositories under the `waifuai` organization with their metadata. |

## 🧬 Data Schemas

### `projects.json`

This file contains an array of project objects. Each object represents a single WebSim project.

```json
{
  "title": "Project Title",
  "description": "A brief description of the project...",
  "link": "/p/project_id",
  "thumbnail": "https://project-screenshots.websim.com/thumbnail.jpg",
  "views": 123,
  "likes": 45,
  "created": "ISO-8601 Timestamp",
  "updated": "ISO-8601 Timestamp",
  "created_order": 1
}
```

- **title**: The name of the project.
- **description**: A short summary of what the project does.
- **link**: The relative path or ID to access the project.
- **thumbnail**: URL to the project's preview image.
- **views**: Total capture count of views.
- **likes**: Total count of likes.
- **created**: Timestamp of when the project was created.
- **updated**: Timestamp of the last update.
- **created_order**: An integer representing the chronological order of creation.

### `github.json`

This file contains an array of repository objects fetched from GitHub.

```json
{
  "name": "repo-name",
  "description": "Repository description...",
  "html_url": "https://github.com/waifuai/repo-name",
  "language": "Python",
  "stargazers_count": 10
}
```

- **name**: The name of the repository.
- **description**: The description provided on GitHub.
- **html_url**: Direct link to the repository.
- **language**: The primary programming language used.
- **stargazers_count**: Number of stars the repository has received.

## 🚀 Usage

You can easily load this data using Python to start your analysis.

```python
import json
import os

# Define paths
base_path = 'data'
projects_path = os.path.join(base_path, 'projects.json')
github_path = os.path.join(base_path, 'github.json')

# Load WebSim Projects
with open(projects_path, 'r', encoding='utf-8') as f:
    projects = json.load(f)
    print(f"Loaded {len(projects)} WebSim projects.")

# Load GitHub Repos
with open(github_path, 'r', encoding='utf-8') as f:
    repos = json.load(f)
    print(f"Loaded {len(repos)} GitHub repositories.")
```

## 📄 License

This project is licensed under the terms of the [LICENSE](LICENSE) file.
