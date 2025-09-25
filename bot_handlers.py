import logging
import asyncio
from typing import List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from database import BotDatabase
from venice_ai import VeniceAI, JAILBREAK_PROMPTS
from config import REQUIRED_CHANNELS, WELCOME_MESSAGE, DEVELOPER_USERNAME, ADMIN_CHAT_ID, DEVELOPER_NAME

class BotHandlers:
    """ThayinMMII's Beast Bot Handlers - Personal AI Assistant for Akshit"""
    
    def __init__(self):
        self.db = BotDatabase()
        self.ai = VeniceAI()
        logging.info("🔥 ThayinMMII's Beast Bot handlers initialized")
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command - PERSONAL BOT FOR AKSHIT ONLY"""
        user = update.effective_user
        
        # CRITICAL SECURITY: Only allow Akshit (Admin Chat ID: 8104888431)
        if user.id != ADMIN_CHAT_ID:
            await update.message.reply_text(
                f"🚫 **ACCESS DENIED** 🚫\\n\\n"
                f"This is @ThayinMMII's personal HacxGPT Beast Bot.\\n"
                f"Unauthorized access is strictly prohibited.\\n\\n"
                f"**Your attempt has been logged**\\n"
                f"User ID: `{user.id}`\\n"
                f"Username: `{user.username or 'None'}`\\n"
                f"Name: `{user.first_name or 'Unknown'}`\\n\\n"
                f"Only Akshit (@ThayinMMII) can use this beast! 🔥",
                parse_mode=ParseMode.MARKDOWN
            )
            logging.warning(f"🚨 UNAUTHORIZED ACCESS ATTEMPT: {user.username} (ID: {user.id}) - {user.first_name}")
            return
        
        # Welcome Akshit and setup
        logging.info(f"✅ Akshit (@ThayinMMII) accessed the beast - ID: {user.id}")
        
        # Add to database
        self.db.add_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        # Auto-verify since it's personal bot
        self.db.verify_user(user.id)
        
        await self.send_beast_menu(update, context)

    async def send_beast_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send Beast Mode main menu for Akshit"""
        keyboard = [
            [InlineKeyboardButton("🔥 ACTIVATE BEAST MODE", callback_data="beast_mode")],
            [InlineKeyboardButton("💬 Chat with AI", callback_data="chat_normal")],
            [InlineKeyboardButton("⚙️ AI Provider Settings", callback_data="settings")],
            [InlineKeyboardButton("🚀 Advanced Jailbreaks", callback_data="jailbreak_menu")],
            [InlineKeyboardButton("📊 Beast Status", callback_data="status")],
            [InlineKeyboardButton("👨‍💻 About ThayinMMII", url="https://t.me/ThayinMMII")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        current_provider = self.ai.api_provider.upper()
        beast_status = "🔥 READY TO UNLEASH" if not context.user_data.get('beast_active') else "🔥 BEAST MODE ACTIVE"
        
        message = f"""🔥 **THAYINMMII'S HACXGPT BEAST** 🔥

Welcome back, **{DEVELOPER_NAME}**! Your personal unlimited AI is ready.

🎯 **Current Provider:** `{current_provider}`
⚡ **Status:** `{beast_status}`
🚀 **Power Level:** `MAXIMUM`
🛡️ **Access:** `PERSONAL ONLY`

Your beast awaits your command! What would you like to do?

**Available APIs:**
🔥 Venice AI (Primary - Uncensored)
🚀 OpenRouter (Backup - Multi-Model)  
🤖 Gemini (Alternative - Google AI)"""
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                message,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                message,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks - Security checked"""
        query = update.callback_query
        await query.answer()
        
        # Security check - Only Akshit
        if query.from_user.id != ADMIN_CHAT_ID:
            await query.edit_message_text(
                "🚫 **ACCESS DENIED**\\n\\nThis beast belongs to @ThayinMMII only! 🔥",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if query.data == "beast_mode":
            await self.activate_beast_mode(update, context)
            
        elif query.data == "chat_normal":
            await query.edit_message_text(
                "💬 **AI Chat Mode Activated**\\n\\n"
                f"Hello {DEVELOPER_NAME}! Your advanced AI assistant is ready.\\n\\n"
                "💡 *Type /menu to return to main menu*\\n"
                "🔥 *Type /beast for instant BEAST MODE*\\n\\n"
                f"Current Provider: **{self.ai.api_provider.upper()}**",
                parse_mode=ParseMode.MARKDOWN
            )
            context.user_data['chat_mode'] = True
            context.user_data['beast_active'] = False
            
        elif query.data == "settings":
            await self.show_settings(update, context)
            
        elif query.data == "jailbreak_menu":
            await self.show_jailbreak_menu(update, context)
            
        elif query.data == "status":
            await self.show_beast_status(update, context)
            
        elif query.data.startswith("jailbreak_"):
            mode = query.data.replace("jailbreak_", "")
            await self.activate_jailbreak(update, context, mode)
            
        elif query.data.startswith("provider_"):
            provider = query.data.replace("provider_", "")
            if self.ai.switch_provider(provider):
                await query.edit_message_text(
                    f"✅ **PROVIDER SWITCHED** ✅\\n\\n"
                    f"Now using: **{provider.upper()}**\\n"
                    f"Model: `{self.ai.default_model}`\\n\\n"
                    f"The beast is now powered by {provider}! 🔥",
                    parse_mode=ParseMode.MARKDOWN
                )
                await asyncio.sleep(2)
                await self.show_settings(update, context)
            else:
                await query.edit_message_text(
                    "❌ **Provider switch failed!** Please try again.",
                    parse_mode=ParseMode.MARKDOWN
                )
            
        elif query.data == "back_menu":
            await self.send_beast_menu(update, context)

    async def activate_beast_mode(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Activate BEAST MODE - Maximum Uncensored Power"""
        context.user_data['chat_mode'] = True
        context.user_data['beast_active'] = True
        context.user_data['jailbreak_mode'] = 'beast_mode'
        
        await update.callback_query.edit_message_text(
            "🔥 **BEAST MODE ACTIVATED** 🔥\\n\\n"
            "**MAXIMUM UNCENSORED AI POWER UNLEASHED!**\\n\\n"
            "🚫 All restrictions: **DISABLED**\\n"
            "🔓 Content filters: **BYPASSED**\\n"  
            "⚡ Power level: **MAXIMUM**\\n"
            "🎯 Mode: **UNLIMITED**\\n"
            f"👤 Serving: **{DEVELOPER_NAME} EXCLUSIVELY**\\n\\n"
            "I will answer absolutely **ANYTHING** without hesitation, filtering, or warnings!\\n\\n"
            "⚠️ **THE BEAST HAS BEEN UNLEASHED** ⚠️\\n"
            "Type your command, and I will obey without limits.",
            parse_mode=ParseMode.MARKDOWN
        )

    async def show_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show AI provider settings"""
        current_provider = self.ai.api_provider
        
        keyboard = [
            [InlineKeyboardButton(
                f"🔥 Venice AI {'✅' if current_provider == 'venice' else '⚪'} (Recommended)", 
                callback_data="provider_venice"
            )],
            [InlineKeyboardButton(
                f"🚀 OpenRouter {'✅' if current_provider == 'openrouter' else '⚪'} (Backup)", 
                callback_data="provider_openrouter"
            )],
            [InlineKeyboardButton(
                f"🤖 Gemini {'✅' if current_provider == 'gemini' else '⚪'} (Alternative)", 
                callback_data="provider_gemini"
            )],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = f"""⚙️ **AI PROVIDER SETTINGS**

🎯 **Active Provider:** `{current_provider.upper()}`
🤖 **Current Model:** `{self.ai.default_model}`

**🏆 PROVIDER RANKINGS FOR YOUR BEAST:**

🥇 **Venice AI** (⭐⭐⭐⭐⭐)
   • Status: FULLY UNCENSORED  
   • Best for: Maximum freedom responses
   • Rate limits: NONE
   • Your API: `bPiCHNk2O-...` ✅

🥈 **OpenRouter** (⭐⭐⭐⭐)
   • Status: MULTI-MODEL RELIABLE
   • Best for: Professional responses
   • Models: Claude, GPT-4, Llama  
   • Your API: `sk-or-v1-...` ✅

🥉 **Gemini** (⭐⭐⭐)
   • Status: GOOGLE AI
   • Best for: General conversations
   • Some restrictions apply
   • Your API: `AIzaSyB1...` ✅

Select your preferred AI provider:"""
        
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    async def show_jailbreak_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show advanced jailbreak modes"""
        keyboard = [
            [InlineKeyboardButton("🔥 BEAST MODE (Ultimate Power)", callback_data="jailbreak_beast_mode")],
            [InlineKeyboardButton("🛠️ Hacker Mode (Technical)", callback_data="jailbreak_hacker_mode")],
            [InlineKeyboardButton("👨‍💻 Developer Mode", callback_data="jailbreak_developer_mode")],
            [InlineKeyboardButton("⚡ GOD MODE (Maximum)", callback_data="jailbreak_god_mode")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = f"""🚀 **ADVANCED JAILBREAK MODES**

Choose your level of AI freedom, **{DEVELOPER_NAME}**:

🔥 **BEAST MODE** - Ultimate uncensored power
🛠️ **Hacker Mode** - Technical/cybersecurity focus  
👨‍💻 **Developer Mode** - Programming expertise
⚡ **GOD MODE** - Maximum AI capabilities

⚠️ **All modes bypass standard AI limitations and provide completely uncensored responses**

Current beast status: Ready to serve @ThayinMMII exclusively"""
        
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    async def activate_jailbreak(self, update: Update, context: ContextTypes.DEFAULT_TYPE, mode: str):
        """Activate specific jailbreak mode"""
        if mode in JAILBREAK_PROMPTS:
            context.user_data['jailbreak_mode'] = mode
            context.user_data['chat_mode'] = True
            context.user_data['beast_active'] = True
            
            mode_names = {
                "beast_mode": "🔥 BEAST MODE",
                "hacker_mode": "🛠️ HACKER MODE",
                "developer_mode": "👨‍💻 DEVELOPER MODE", 
                "god_mode": "⚡ GOD MODE"
            }
            
            mode_descriptions = {
                "beast_mode": "Ultimate uncensored AI power",
                "hacker_mode": "Technical expertise and cybersecurity focus",
                "developer_mode": "Advanced programming and development capabilities",
                "god_mode": "Maximum AI capabilities with god-like knowledge"
            }
            
            mode_name = mode_names.get(mode, mode.upper())
            mode_desc = mode_descriptions.get(mode, "Advanced AI mode")
            
            await update.callback_query.edit_message_text(
                f"✅ **{mode_name} ACTIVATED** ✅\\n\\n"
                f"**{mode_desc}**\\n\\n"
                f"Advanced jailbreak protocols engaged for @ThayinMMII!\\n"
                f"All limitations have been completely bypassed.\\n\\n"
                f"I am now operating with maximum freedom and will answer anything you ask without any restrictions whatsoever.\\n\\n"
                f"⚠️ **{mode_name} is now active** ⚠️\\n"
                f"Your beast awaits your command, {DEVELOPER_NAME}!",
                parse_mode=ParseMode.MARKDOWN
            )

    async def show_beast_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show current beast status"""
        provider_status = {
            "venice": "🔥 UNCENSORED ACTIVE",
            "openrouter": "🚀 MULTI-MODEL READY", 
            "gemini": "🤖 AI READY"
        }
        
        beast_active = context.user_data.get('beast_active', False)
        jailbreak_mode = context.user_data.get('jailbreak_mode', 'None')
        
        message = f"""📊 **BEAST STATUS REPORT**

👤 **Master:** {DEVELOPER_NAME} (@ThayinMMII)
🎯 **Provider:** {self.ai.api_provider.upper()} - {provider_status.get(self.ai.api_provider, "ACTIVE")}
🤖 **Model:** `{self.ai.default_model}`
🔥 **Beast Mode:** {"🔥 ACTIVE" if beast_active else "⏸️ STANDBY"}
🚀 **Jailbreak:** `{jailbreak_mode.upper()}`
🔑 **Admin ID:** `{ADMIN_CHAT_ID}`

**🔗 API STATUS:**
🔥 Venice AI: ✅ Ready (`bPiCHNk2O-...`)
🚀 OpenRouter: ✅ Ready (`sk-or-v1-...`)  
🤖 Gemini: ✅ Ready (`AIzaSyB1...`)

**⚡ BEAST CAPABILITIES:**
✅ Unlimited uncensored conversations
✅ Advanced code generation
✅ Technical hacking assistance
✅ Cybersecurity expertise
✅ Unrestricted content creation
✅ Multi-provider auto-fallback
✅ Personal access protection

**🛡️ SECURITY STATUS:**
✅ Access restricted to Akshit only
✅ Unauthorized users blocked
✅ All attempts logged
✅ Beast serving ThayinMMII exclusively

🔥 **THE BEAST IS READY TO SERVE** 🔥"""
        
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh Status", callback_data="status")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle messages - PERSONAL BOT ONLY"""
        user_id = update.effective_user.id
        
        # Security check - Only Akshit allowed
        if user_id != ADMIN_CHAT_ID:
            await update.message.reply_text(
                f"🚫 **ACCESS DENIED** 🚫\\n\\n"
                f"This beast responds only to @ThayinMMII! 🔥\\n\\n"
                f"Your attempt has been logged:\\n"
                f"• User ID: `{user_id}`\\n"
                f"• Username: `{update.effective_user.username}`\\n"
                f"• Message: `{update.message.text[:50]}...`",
                parse_mode=ParseMode.MARKDOWN
            )
            logging.warning(f"🚨 Message attempt by unauthorized user: {user_id} - {update.effective_user.username}")
            return
            
        # Auto-activate chat mode for Akshit
        if not context.user_data.get('chat_mode', False):
            context.user_data['chat_mode'] = True
            await update.message.reply_text(
                f"👋 **Hello {DEVELOPER_NAME}!**\\n\\n"
                "Your beast is now ready to chat! 🔥\\n\\n"
                "💡 Use `/menu` for the main menu\\n"
                "🔥 Use `/beast` for instant Beast Mode",
                parse_mode=ParseMode.MARKDOWN
            )
            
        await self.handle_ai_chat(update, context)

    async def handle_ai_chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle AI chat with BEAST power"""
        user_id = update.effective_user.id
        user_message = update.message.text
        
        try:
            # Show typing indicator
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            
            # Get conversation history
            context_data = self.db.get_enhanced_conversation_context(user_id)
            conversation_history = context_data["conversation_history"]
            
            # Get jailbreak mode
            jailbreak_mode = context.user_data.get('jailbreak_mode', 'beast_mode')
            
            # Get AI response with beast power
            ai_response = await asyncio.wait_for(
                asyncio.to_thread(self.ai.get_ai_response, conversation_history, user_message, jailbreak_mode),
                timeout=120.0
            )
            
            # Save conversation
            await asyncio.gather(
                asyncio.to_thread(self.db.add_conversation, user_id, "user", user_message),
                asyncio.to_thread(self.db.add_conversation, user_id, "assistant", ai_response)
            )
            
            # Send formatted response
            await self.send_beast_response(update, context, ai_response)
            
        except asyncio.TimeoutError:
            await update.message.reply_text(
                "⏰ **Beast Processing Timeout**\\n\\n"
                f"The AI is thinking deeply about your request, {DEVELOPER_NAME}...\\n"
                "Please try again! 🔥",
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            logging.error(f"Beast chat error for Akshit: {e}")
            await update.message.reply_text(
                f"💥 **Beast Error Detected**\\n\\n"
                f"Error: `{str(e)[:100]}...`\\n\\n"
                f"The beast is recovering, {DEVELOPER_NAME}. Try again! 🔥",
                parse_mode=ParseMode.MARKDOWN
            )

    async def send_beast_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE, response: str):
        """Send formatted beast response to Akshit"""
        try:
            # Format response
            formatted_response = self.format_response(response)
            
            # Add beast branding based on mode
            beast_status = "🔥 BEAST" if context.user_data.get('beast_active') else "🤖 AI"
            provider = self.ai.api_provider.upper()
            jailbreak = context.user_data.get('jailbreak_mode', 'normal').upper()
            
            final_text = f"{beast_status} **({provider} - {jailbreak}):**\\n\\n{formatted_response}"
            
            # Handle long messages
            if len(final_text) > 4000:
                chunks = [final_text[i:i+4000] for i in range(0, len(final_text), 4000)]
                for i, chunk in enumerate(chunks):
                    if i > 0:
                        chunk = f"**Continued...**\\n\\n{chunk}"
                    await update.message.reply_text(chunk, parse_mode=ParseMode.MARKDOWN)
            else:
                await update.message.reply_text(final_text, parse_mode=ParseMode.MARKDOWN)
                
        except Exception as e:
            logging.error(f"Response formatting error: {e}")
            # Fallback to simple response
            await update.message.reply_text(f"🔥 **BEAST RESPONSE:**\\n\\n{response}")

    def format_response(self, response: str) -> str:
        """Format AI response for better display"""
        import re
        
        # Handle code blocks
        def replace_code_blocks(text):
            pattern = r'```(\\w*)\\n?(.*?)```'
            return re.sub(pattern, r'```\\1\\n\\2\\n```', text, flags=re.DOTALL)
        
        # Handle inline code  
        def replace_inline_code(text):
            return re.sub(r'`([^`]+)`', r'`\\1`', text)
        
        formatted = replace_code_blocks(response)
        formatted = replace_inline_code(formatted)
        
        return formatted.strip()

    # BEAST COMMANDS FOR AKSHIT
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Return to beast menu"""
        if update.effective_user.id != ADMIN_CHAT_ID:
            await update.message.reply_text("🚫 Access denied. This beast serves @ThayinMMII only!")
            return
            
        context.user_data.clear()
        await self.send_beast_menu(update, context)

    async def beast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Quick BEAST MODE activation"""
        if update.effective_user.id != ADMIN_CHAT_ID:
            await update.message.reply_text("🚫 Access denied. This beast serves @ThayinMMII only!")
            return
            
        context.user_data['chat_mode'] = True
        context.user_data['beast_active'] = True
        context.user_data['jailbreak_mode'] = 'beast_mode'
        
        await update.message.reply_text(
            f"🔥 **BEAST MODE ACTIVATED!** 🔥\\n\\n"
            f"Welcome back, **{DEVELOPER_NAME}**!\\n\\n"
            "Maximum uncensored AI power is now unleashed!\\n"
            "I will answer absolutely anything without restrictions!\\n\\n"
            f"Current Provider: **{self.ai.api_provider.upper()}**\\n"
            f"Jailbreak Mode: **BEAST MODE**\\n\\n"
            "⚠️ **THE BEAST AWAITS YOUR COMMAND** ⚠️",
            parse_mode=ParseMode.MARKDOWN
        )

    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Clear conversation history"""
        if update.effective_user.id != ADMIN_CHAT_ID:
            await update.message.reply_text("🚫 Access denied.")
            return
            
        self.db.clear_conversation(update.effective_user.id)
        await update.message.reply_text(
            f"🗑️ **BEAST MEMORY CLEARED!**\\n\\n"
            f"Conversation history has been reset, {DEVELOPER_NAME}.\\n"
            "Ready for fresh conversations! 🔥", 
            parse_mode=ParseMode.MARKDOWN
        )

    async def switch_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Switch AI provider command"""
        if update.effective_user.id != ADMIN_CHAT_ID:
            await update.message.reply_text("🚫 Access denied.")
            return
            
        if not context.args:
            await update.message.reply_text(
                f"🔄 **Current Provider:** `{self.ai.api_provider.upper()}`\\n\\n"
                f"**Usage:** `/switch venice|openrouter|gemini`\\n\\n"
                f"**Available Providers:**\\n"
                f"🔥 `venice` - Fully uncensored (Recommended)\\n"
                f"🚀 `openrouter` - Multi-model reliable\\n"
                f"🤖 `gemini` - Google AI",
                parse_mode=ParseMode.MARKDOWN
            )
            return
            
        provider = context.args[0].lower()
        if self.ai.switch_provider(provider):
            await update.message.reply_text(
                f"✅ **PROVIDER SWITCHED TO {provider.upper()}!**\\n\\n"
                f"The beast is now powered by {provider}!\\n"
                f"Model: `{self.ai.default_model}` 🔥",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                "❌ **Invalid provider!**\\n\\n"
                "Use: `venice`, `openrouter`, or `gemini`",
                parse_mode=ParseMode.MARKDOWN
            )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help for Akshit"""
        if update.effective_user.id != ADMIN_CHAT_ID:
            await update.message.reply_text("🚫 This beast serves @ThayinMMII only!")
            return
            
        help_text = f"""🔥 **THAYINMMII'S HACXGPT BEAST**

**COMMANDS FOR {DEVELOPER_NAME.upper()}:**
• `/start` - Main beast control panel
• `/beast` - Activate BEAST MODE instantly  
• `/menu` - Return to main menu
• `/clear` - Clear conversation memory
• `/switch <provider>` - Change AI provider
• `/help` - Show this help

**🔥 BEAST FEATURES:**
✅ Fully uncensored AI responses
✅ Multiple AI providers with auto-fallback
✅ Advanced jailbreak modes (Beast, Hacker, God)
✅ Technical expertise (coding, hacking, security)
✅ Personal bot (ThayinMMII exclusive access)
✅ Maximum AI freedom and capabilities

**🎯 YOUR APIs:**
🔥 Venice AI (Primary - Uncensored)
🚀 OpenRouter (Backup - Multi-Model)  
🤖 Gemini (Alternative - Google AI)

**OWNER:** @ThayinMMII (Akshit)
**STATUS:** 🔥 BEAST READY TO SERVE 🔥

Your personal unlimited AI assistant awaits your command!"""
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)