# Restaurant Management System

A command-line restaurant management application written in Python. The system supports separate role menus for Customer, Chef, Manager, and Admin, with persistent state saved using text files.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Running the App](#running-the-app)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Notes](#notes)
- [License](#license)

## Features

- Role-based interface for:
  - Customer
  - Chef
  - Manager
  - Admin
- Customer capabilities:
  - Signup and login
  - View orders
  - Add orders
  - Edit orders
  - Delete orders
  - Submit feedback
- Chef capabilities:
  - View all orders
  - Update order status
  - Manage ingredients
  - Update chef profile
- Manager capabilities:
  - Manage customers
  - Manage menu items
  - Update profile information
- Admin capabilities:
  - Manage staff records
  - View sales report
  - View and add customer feedback
  - Update profile information

## Getting Started

1. Clone or download the repository.
2. Open a terminal and navigate to the project folder.
3. Run the application with Python.

## Prerequisites

- Python 3.x installed on your system.

## Running the App

From the project folder, run:

```bash
python main.py
```

> Note: The application now uses `main.py` as the executable script.

## Project Structure

- `main.py` — main application source code and entrypoint
- `menu.txt` — menu item data
- `orders.txt` — order records
- `feedback.txt` — customer feedback records
- `ingredients.txt` — ingredient list
- `staff.txt` — staff records
- `manager_profile.txt` — manager profile data file created at runtime
- `README.md` — documentation

## How It Works

- The system uses plain text files for persistent storage.
- Role menus are displayed based on the selected user type.
- Customers can manage their own orders and send feedback.
- Chefs can view orders, update statuses, and manage ingredients.
- Managers can manage customers and menu items.
- Admins can manage staff, review sales, and read feedback.

## Notes

- No external dependencies are required.
- The application now uses `main.py` as the executable script.
- The application creates `customers.txt` at runtime when customer accounts are added.

## License

This repository is ready for GitHub upload.
