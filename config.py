# Your Telegram bot token.
BOT_TOKEN = "6551312087:AAG7IqLj97bGxPhP86_dl5ZJ8HeDBvRhDBw"

# Telegram API ID and Hash. This is NOT your bot token and shouldn't be changed.
API_ID = 29297194
API_HASH = "6e7ded48d526c706d213c4fda1ce84aa"

# Chat used for logging errors.
LOG_CHAT = -1001820588722


# Chat used for logging user actions (like buy, gift, etc).
ADMIN_CHAT = -925966502


# How many updates can be handled in parallel.
# Don't use high values for low-end servers.
WORKERS = 20

# Admins can access panel and add new materials to the bot.
ADMINS = [1334532423]

# Sudoers have full access to the server and can execute commands.
SUDOERS = [1334532423]

# All sudoers should be admins too
ADMINS.extend(SUDOERS)

GIFTERS = []