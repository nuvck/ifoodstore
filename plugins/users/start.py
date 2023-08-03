from typing import Union

from pyrogram import Client, filters
from pyrogram.errors import BadRequest
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from database import cur, save
from utils import create_mention, get_info_wallet


@Client.on_message(filters.command(["start", "menu"]))
@Client.on_callback_query(filters.regex("^start$"))
async def start(c: Client, m: Union[Message, CallbackQuery]):
    user_id = m.from_user.id

    rt = cur.execute(
        "SELECT id, balance, balance_diamonds, refer FROM users WHERE id=?", [user_id]
    ).fetchone()

    if isinstance(m, Message):
        refer = (
            int(m.command[1])
            if (len(m.command) == 2)
            and (m.command[1]).isdigit()
            and int(m.command[1]) != user_id
            else None
        )

        if rt[3] is None:
            if refer is not None:
                mention = create_mention(m.from_user, with_id=False)

                cur.execute("UPDATE users SET refer = ? WHERE id = ?", [refer, user_id])
                try:
                    await c.send_message(
                        refer,
                        text=f"<b>O usuário {mention} se tornou seu referenciado.</b>",
                    )
                except BadRequest:
                    pass

    kb = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton("💸 ADD SALDO", callback_data="add_saldo_manual"),
                InlineKeyboardButton("🛍 COMPRAR CC", callback_data="comprar_cc"),
            ],
            [
                InlineKeyboardButton("👤 PERFIL", callback_data="user_info"),
                InlineKeyboardButton("☎️ SUP", url='https://t.me/lzccs'),
                InlineKeyboardButton("⚙️ DEV", url='https://t.me/lzccs'),
            ],
            [
                    InlineKeyboardButton("⚙ Desenvolvemento da Store", callback_data="dv")
            ] 
        ]
    )

    bot_logo, news_channel, support_user = cur.execute(
        "SELECT main_img, channel_user, support_user FROM bot_config WHERE ROWID = 0"
    ).fetchone()

    start_message = f"""🎉 <b>Seja bem vindo a LZ STORE {m.from_user.first_name}!</b>
=================================
✅ Checkadas na hora pelo bot!
👤 Todas com nome e CPF!
💰 Faça recargas rapidamente pelo /pix!
=================================
ℹ️ grupo oficial 
@tropadolzz

[⚙️] Desenvolvedor Do Bot @lzccs
=================================
⚠️ LEMBRE-SE DE QUE AS TROCAS SÃO EXCLUSIVAMENTE FEITAS NO BOT.
⚠️ NÃO GARANTO APROVAÇÃO 
⚠️ NÃO GARANTO QUE A INFO SERÁ VINCULADA EM NENHUM APLICATIVO 
⚠️ GARANTO APENAS LIVE 
=================================
{get_info_wallet(user_id)}

"""

    if isinstance(m, CallbackQuery):
        send = m.edit_message_text
    else:
        send = m.reply_text
    save()
    await send(start_message, reply_markup=kb)
