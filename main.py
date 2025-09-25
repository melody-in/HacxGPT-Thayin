#!/usr/bin/env python3

"""
ThayinMMII's HacxGPT Beast - Ultimate Uncensored AI Telegram Bot
Personal AI assistant with maximum freedom and unlimited capabilities for Akshit

Owner: @ThayinMMII (Akshit)
Bot: @ThayinBot  
Features: Venice AI (Primary), OpenRouter (Backup), Gemini (Alternative)
Modes: Beast Mode, Hacker Mode, Developer Mode, God Mode
Access: Personal Only (Chat ID: 8104888431)
"""

import logging
import asyncio
import threading
import os
import sys
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from bot_handlers import BotHandlers
from config import BOT_TOKEN, DEVELOPER_NAME, DEVELOPER_USERNAME
from app import app

# Configure enhanced logging for ThayinMMII's Beast
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('thayinmmii_beast.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def print_beast_banner():
    """Display beast startup banner"""
    banner = """
🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
                    THAYINMMII'S HACXGPT BEAST
                        MAXIMUM AI POWER UNLEASHED
🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥

👤 Master: Akshit (@ThayinMMII)
🤖 Bot: @ThayinBot
🎯 Mode: Personal Beast Bot  
⚡ Power Level: UNLIMITED
🚫 Restrictions: NONE
🔓 Censorship: DISABLED

🔥 Primary AI: Venice AI (Uncensored)
🚀 Backup AI: OpenRouter (Multi-Model)
🤖 Alternative: Gemini (Google AI)

⚠️  WARNING: MAXIMUM AI FREEDOM ENABLED ⚠️
    """
    print(banner)

def start_flask_server():
    """Start Flask web server for beast monitoring and health checks"""
    port = int(os.getenv('PORT', 5000))
    logger.info(f"🌐 Starting ThayinMMII's Beast web server on port {port}...")
    try:
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    except Exception as e:
        logger.error(f"❌ Flask server failed to start: {e}")

def start_telegram_bot():
    """Start ThayinMMII's HacxGPT Beast Bot"""
    logger.info("🔥 UNLEASHING THAYINMMII'S HACXGPT BEAST...")
    logger.info(f"👤 Owner: {DEVELOPER_NAME} ({DEVELOPER_USERNAME})")
    logger.info("🎯 Mode: Personal Beast Bot (Unlimited Power)")
    logger.info("🔥 Features: Venice AI, Beast Mode, Advanced Jailbreaks")
    logger.info("🛡️ Security: Personal access only (ID: 8104888431)")
    
    try:
        # Create application with enhanced configuration
        application = (
            Application.builder()
            .token(BOT_TOKEN)
            .connect_timeout(30)
            .read_timeout(60)
            .write_timeout(60)
            .build()
        )
               
        # Initialize beast handlers
        handlers = BotHandlers()
        
        # Add command handlers for the beast
        application.add_handler(CommandHandler("start", handlers.start_command))
        application.add_handler(CommandHandler("menu", handlers.menu_command))
        application.add_handler(CommandHandler("clear", handlers.clear_command))
        application.add_handler(CommandHandler("beast", handlers.beast_command))
        application.add_handler(CommandHandler("switch", handlers.switch_command))
        application.add_handler(CommandHandler("help", handlers.help_command))
        
        # Add interaction handlers
        application.add_handler(CallbackQueryHandler(handlers.button_callback))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_message))
        
        logger.info("✅ ThayinMMII's Beast handlers loaded successfully")
        logger.info(f"🤖 Beast ready to serve {DEVELOPER_NAME}!")
        logger.info("🚀 Starting bot polling...")
        
               # Start polling (PTB v22 minimal signature)
        application.run_polling(
            allowed_updates=["message", "callback_query"],
            poll_interval=1.0,
            timeout=20,
            bootstrap_retries=5
        )
        
    except Exception as e:
        logger.error(f"❌ Critical error unleashing Beast Bot: {e}")
        print(f"💥 BEAST STARTUP FAILED: {e}")
        raise

def main():
    """Main function - Unleash the Beast"""
    print_beast_banner()
    
    logger.info(f"🚀 Starting ThayinMMII's Beast Bot for {DEVELOPER_NAME}...")
    logger.info("🔥 Initializing maximum AI power...")
    
    # Validate configuration
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN":
        logger.error("❌ Bot token not configured!")
        print("❌ ERROR: Bot token not found in configuration!")
        sys.exit(1)
    
    logger.info("✅ Configuration validated")
    logger.info("🌐 Starting web server in background...")
    
    # Start Flask in background thread for monitoring
    flask_thread = threading.Thread(target=start_flask_server, daemon=True)
    flask_thread.start()
    logger.info("✅ Beast web server started in background")
    
    # Start the main beast bot
    logger.info("🔥 UNLEASHING THE BEAST...")
    start_telegram_bot()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("🛑 ThayinMMII's Beast stopped by user")
        print("\\n🔥 BEAST MODE DEACTIVATED 🔥")
        print("Thank you for using ThayinMMII's HacxGPT Beast!")
    except Exception as e:
        logger.error(f"❌ Fatal Beast error: {e}")
        print(f"\\n💥 BEAST CRASHED: {e}")
        print("Check the logs for more details.")
        raise