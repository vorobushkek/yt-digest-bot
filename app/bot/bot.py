import os
import asyncio
import logging
from typing import Any, Dict

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web, ClientSession

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "webhook_secret")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class YouTubeDigestBot:
    """YouTube Digest Bot implementation"""
    
    def __init__(self):
        self.bot = bot
        self.dp = dp
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup message handlers"""
        
        @self.dp.message(Command("start"))
        async def start_handler(message: types.Message) -> None:
            """Handle /start command"""
            welcome_text = (
                "🤖 Welcome to YouTube Digest Bot!\n\n"
                "I help you create digests from YouTube channels.\n\n"
                "Available commands:\n"
                "/start - Show this help message\n"
                "/help - Show help information\n"
                "/status - Check bot status\n"
                "/digest - Generate a digest (coming soon)"
            )
            await message.reply(welcome_text)
        
        @self.dp.message(Command("help"))
        async def help_handler(message: types.Message) -> None:
            """Handle /help command"""
            help_text = (
                "📚 YouTube Digest Bot Help\n\n"
                "This bot creates summaries from YouTube channels.\n\n"
                "Commands:\n"
                "/start - Start the bot\n"
                "/help - Show this help\n"
                "/status - Bot status\n\n"
                "🚧 More features coming soon!"
            )
            await message.reply(help_text)
        
        @self.dp.message(Command("status"))
        async def status_handler(message: types.Message) -> None:
            """Handle /status command"""
            status_text = (
                "✅ Bot Status: Online\n"
                f"🤖 Bot ID: {self.bot.id}\n"
                "📊 Ready to process YouTube digests"
            )
            await message.reply(status_text)
        
        @self.dp.message(Command("digest"))
        async def digest_handler(message: types.Message) -> None:
            """Handle /digest command"""
            digest_text = (
                "🔄 Digest feature is under development!\n\n"
                "Coming soon:\n"
                "• Subscribe to YouTube channels\n"
                "• Generate daily/weekly digests\n"
                "• Get video summaries\n"
                "• Customizable digest preferences"
            )
            await message.reply(digest_text)
        
        @self.dp.message()
        async def default_handler(message: types.Message) -> None:
            """Handle all other messages"""
            await message.reply(
                "🤔 I don't understand this command. Type /help for available commands."
            )
    
    async def set_webhook(self) -> None:
        """Set up webhook"""
        if WEBHOOK_URL:
            webhook_url = f"{WEBHOOK_URL}{WEBHOOK_PATH}"
            await self.bot.set_webhook(
                url=webhook_url,
                secret_token=WEBHOOK_SECRET
            )
            logger.info(f"Webhook set to {webhook_url}")
        else:
            logger.warning("WEBHOOK_URL not configured")
    
    async def delete_webhook(self) -> None:
        """Delete webhook"""
        await self.bot.delete_webhook()
        logger.info("Webhook deleted")
    
    async def set_commands(self) -> None:
        """Set bot commands in Telegram menu"""
        commands = [
            BotCommand(command="start", description="Start the bot"),
            BotCommand(command="help", description="Show help information"),
            BotCommand(command="status", description="Check bot status"),
            BotCommand(command="digest", description="Generate digest (coming soon)")
        ]
        await self.bot.set_my_commands(commands)
        logger.info("Bot commands set")


# Global bot instance
yt_bot = YouTubeDigestBot()


async def process_webhook_update(update: Dict[str, Any]) -> None:
    """Process webhook update"""
    try:
        telegram_update = types.Update(**update)
        await dp.feed_update(bot, telegram_update)
    except Exception as e:
        logger.error(f"Error processing webhook update: {e}")
        raise


async def init_bot() -> None:
    """Initialize bot"""
    try:
        await yt_bot.set_commands()
        await yt_bot.set_webhook()
        logger.info("Bot initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize bot: {e}")
        raise


async def shutdown_bot() -> None:
    """Shutdown bot"""
    try:
        await yt_bot.delete_webhook()
        await bot.session.close()
        logger.info("Bot shutdown complete")
    except Exception as e:
        logger.error(f"Error during bot shutdown: {e}")


if __name__ == "__main__":
    # For testing purposes - run polling mode
    async def main():
        await yt_bot.set_commands()
        logger.info("Starting bot in polling mode...")
        await dp.start_polling(bot)
    
    asyncio.run(main())
