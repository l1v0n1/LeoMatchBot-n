# LeoMatchBot

A Telegram bot for matching and connecting people with similar interests.

## Features

- User profile creation and management
- Profile matching based on similar interests and location
- Admin management system
- User messaging and notifications
- Activity tracking

## Requirements

- Python 3.7+
- Telegram Bot Token

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/LeoMatchBot-n.git
cd LeoMatchBot-n
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your bot:
   - Create a `config.py` file with your Telegram Bot token

5. Initialize the database:
```bash
python start_bot.py
```

## Usage

Run the bot:
```bash
python start_bot.py
```

Check user activity:
```bash
python check_activity_users.py
```

## Project Structure

- `start_bot.py` - Main entry point for the bot
- `work_with_db.py` - Database operations
- `buttons.py` - Telegram keyboard buttons
- `handlers/` - Message and command handlers
- `config.py` - Configuration file for tokens
- `create_bot.py` - Bot initialization
- `check_activity_users.py` - Tracking user activity

## License

MIT

## Contributors

- Your Name 