# Task Tracker CLI

Task Tracker CLI is a simple, Python-based command-line interface for managing personal or project tasks. Developed as part of [roadmap.sh’s](https://roadmap.sh/projects/task-tracker) project guide, this tool focuses on core CLI skills and JSON-based data handling, ensuring a straightforward approach to task management.

### Project Featured by : [roadmap.sh](https://roadmap.sh/projects/task-tracker)

## Features

- **Task Management**: Easily add, update, delete, and list tasks.
- **Color-Coded Output**: Enjoy enhanced readability with customizable color options.
- **JSON Data Storage**: Task data is persistently stored in JSON format.
- **Modular Code Structure**: Designed to be extensible and maintainable.

## Getting Started

### Prerequisites

- Python 3.x installed on your system.

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Akkiraj1234/roadmap.sh-solutiones
    cd "Task Tracker CLI"
    ```

2. **Run the Script**:
    ```bash
    python task-cli.py [command] [options]
    ```

### Commands Overview

| Command | Description                 | Usage Example                                      |
|---------|-----------------------------|----------------------------------------------------|
| `add`   | Adds a new task             | `python task-cli.py add "Task Description"`        |
| `update`| Updates a task by its ID    | `python task-cli.py update [task_id] "New Description"` |
| `delete`| Deletes a task by its ID    | `python task-cli.py delete [task_id]`              |
| `list`  | Lists all tasks in the tracker | `python task-cli.py list`                       |

### Color Customization

Task Tracker CLI includes color-coded outputs for better visibility of tasks. Through the `CILcolor` class, you can set colors and styles (such as bold, italic, underline) for task statuses or priority levels.

**Available Colors**

The CLI supports both ANSI color names and RGB customization, which you can modify within the script to suit your preferences.

### JSON Data Format

The task data is stored in `tasks.json`, structured as follows:
```json
{
    "0": {
        "description": "Sample task",
        "status": "todo",
        "createdAt": 1730454918.488961,
        "updatedAt": 1730454918.488961
    }
}
```

### Each task entry includes:

- **description**: Brief description of the task
- **status**: Current task status *(e.g., "todo", "in progress", "completed")*
- **createdAt**: Timestamp of task creation
- **updatedAt**: Timestamp of the last update

## Contributing
Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make changes and test thoroughly.
4. Submit a pull request for review.

### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Developed as part of the roadmap.sh Task Tracker project.

This version includes a clear structure with consistent formatting for easy readability and usage. Feel free to modify the repository link and task statuses if needed. Let me know if there’s anything more to add!

