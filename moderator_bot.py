from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram.error import BadRequest

# Initialize welcome message and rules
welcome_message = "Welcome to the chat!"
rules_message = "Be kind and respectful to others."

# Command handlers
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome to the moderation bot! Type /help for commands.")

async def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "/start - Start the bot\n"
        "/help - Show this message\n"
        "/ban - Ban a user (reply to their message)\n"
        "/unban - Unban a user (reply to their message)\n"
        "/delete - Delete the last message (reply to the message)\n"
        "/mute - Mute a user (reply to their message)\n"
        "/unmute - Unmute a user (reply to their message)\n"
        "/promote - Promote a user (reply to their message)\n"
        "/demote - Demote an admin (reply to their message)\n"
        "/kick - Kick a user (reply to their message)\n"
        "/setwelcome - Set a welcome message\n"
        "/showwelcome - Show the current welcome message\n"
        "/clear - Clear a specified number of messages (use /clear <number>)\n"
        "/info - Show information about the chat\n"
        "/rules - Show the chat rules"
    )
    await update.message.reply_text(help_text)

async def ban(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        try:
            await context.bot.ban_chat_member(update.message.chat_id, update.message.reply_to_message.from_user.id)
            await update.message.reply_text("User has been banned.")
        except BadRequest:
            await update.message.reply_text("Unable to ban the user.")
    else:
        await update.message.reply_text("Reply to a user's message to ban them.")

async def unban(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        try:
            await context.bot.unban_chat_member(update.message.chat_id, update.message.reply_to_message.from_user.id)
            await update.message.reply_text("User has been unbanned.")
        except BadRequest:
            await update.message.reply_text("Unable to unban the user.")
    else:
        await update.message.reply_text("Reply to a user's message to unban them.")

async def delete(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        try:
            await context.bot.delete_message(update.message.chat_id, update.message.reply_to_message.message_id)
            await update.message.reply_text("Message deleted.")
        except BadRequest:
            await update.message.reply_text("Unable to delete the message.")
    else:
        await update.message.reply_text("Reply to the message you want to delete.")

async def mute(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        try:
            await context.bot.restrict_chat_member(
                update.message.chat_id, update.message.reply_to_message.from_user.id, permissions=ChatPermissions(can_send_messages=False)
            )
            await update.message.reply_text("User has been muted.")
        except BadRequest:
            await update.message.reply_text("Unable to mute the user.")
    else:
        await update.message.reply_text("Reply to a user's message to mute them.")

async def unmute(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        try:
            await context.bot.restrict_chat_member(
                update.message.chat_id, update.message.reply_to_message.from_user.id, permissions=ChatPermissions(can_send_messages=True)
            )
            await update.message.reply_text("User has been unmuted.")
        except BadRequest:
            await update.message.reply_text("Unable to unmute the user.")
    else:
        await update.message.reply_text("Reply to a user's message to unmute them.")

async def promote(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        try:
            await context.bot.promote_chat_member(
                update.message.chat_id, update.message.reply_to_message.from_user.id,
                can_change_info=True, can_delete_messages=True, can_invite_users=True,
                can_restrict_members=True, can_pin_messages=True, can_promote_members=True
            )
            await update.message.reply_text("User has been promoted to admin.")
        except BadRequest:
            await update.message.reply_text("Unable to promote the user.")
    else:
        await update.message.reply_text("Reply to a user's message to promote them.")

async def demote(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        try:
            await context.bot.promote_chat_member(
                update.message.chat_id, update.message.reply_to_message.from_user.id,
                can_change_info=False, can_delete_messages=False, can_invite_users=False,
                can_restrict_members=False, can_pin_messages=False, can_promote_members=False
            )
            await update.message.reply_text("User has been demoted from admin.")
        except BadRequest:
            await update.message.reply_text("Unable to demote the user.")
    else:
        await update.message.reply_text("Reply to a user's message to demote them.")

async def kick(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        try:
            await context.bot.kick_chat_member(update.message.chat_id, update.message.reply_to_message.from_user.id)
            await update.message.reply_text("User has been kicked.")
        except BadRequest:
            await update.message.reply_text("Unable to kick the user.")
    else:
        await update.message.reply_text("Reply to a user's message to kick them.")

async def setwelcome(update: Update, context: CallbackContext) -> None:
    global welcome_message
    if context.args:
        welcome_message = ' '.join(context.args)
        await update.message.reply_text(f"Welcome message set to: {welcome_message}")
    else:
        await update.message.reply_text("Please provide a welcome message after the command.")

async def showwelcome(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"Current welcome message: {welcome_message}")

async def clear(update: Update, context: CallbackContext) -> None:
    try:
        num_messages = int(context.args[0])
        for _ in range(num_messages):
            await context.bot.delete_message(update.message.chat_id, update.message.message_id - 1)
        await update.message.reply_text(f"Cleared {num_messages} messages.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /clear <number>")

async def info(update: Update, context: CallbackContext) -> None:
    chat = update.message.chat
    info_text = (
        f"Chat Title: {chat.title}\n"
        f"Chat ID: {chat.id}\n"
        f"Members: {chat.get_member_count()}"
    )
    await update.message.reply_text(info_text)

async def rules(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(rules_message)

def main():
    # Replace 'YOUR_TOKEN' with your bot's API token
    application = Application.builder().token("7749241813:AAHxOxxTdcSfBRnoDPdrE-hJJ0vVGt0sYrg").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ban", ban))
    application.add_handler(CommandHandler("unban", unban))
    application.add_handler(CommandHandler("delete", delete))
    application.add_handler(CommandHandler("mute", mute))
    application.add_handler(CommandHandler("unmute", unmute))
    application.add_handler(CommandHandler("promote", promote))
    application.add_handler(CommandHandler("demote", demote))
    application.add_handler(CommandHandler("kick", kick))
    application.add_handler(CommandHandler("setwelcome", setwelcome))
    application.add_handler(CommandHandler("showwelcome", showwelcome))
    application.add_handler(CommandHandler("clear", clear))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("rules", rules))

    application.run_polling()

if __name__ == '__main__':
    main()
