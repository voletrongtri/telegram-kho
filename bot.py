from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# GOOGLE SHEETS
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
    scope
)

client = gspread.authorize(creds)

sheet = client.open("KHO_AO_THUN").sheet1


# NHAP HANG
async def nhap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        product = context.args[0]
        qty = int(context.args[1])

        data = sheet.get_all_records()

        found = False

        for i, row in enumerate(data, start=2):
            if row["Product"] == product:
                current = int(row["Quantity"])
                sheet.update_cell(i, 2, current + qty)
                found = True
                break

        if not found:
            sheet.append_row([product, qty])

        await update.message.reply_text(
            f"✅ Đã nhập {qty} {product}"
        )

    except:
        await update.message.reply_text(
            "Sai cú pháp: /nhap ten_sp so_luong"
        )


# XUAT HANG
async def xuat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        product = context.args[0]
        qty = int(context.args[1])

        data = sheet.get_all_records()

        for i, row in enumerate(data, start=2):
            if row["Product"] == product:

                current = int(row["Quantity"])

                if current < qty:
                    await update.message.reply_text(
                        "❌ Không đủ hàng"
                    )
                    return

                sheet.update_cell(i, 2, current - qty)

                await update.message.reply_text(
                    f"✅ Đã xuất {qty} {product}"
                )

                return

        await update.message.reply_text(
            "❌ Không tìm thấy sản phẩm"
        )

    except:
        await update.message.reply_text(
            "Sai cú pháp: /xuat ten_sp so_luong"
        )


# XEM KHO
async def kho(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = sheet.get_all_records()

    text = "📦 TỒN KHO:\n\n"

    for row in data:
        text += f"{row['Product']}: {row['Quantity']}\n"

    await update.message.reply_text(text)


# MAIN
app = ApplicationBuilder().token("8094188029:AAEENf9zEie6_l6q7ySYIygvsOgxBqRFYRg").build()

app.add_handler(CommandHandler("nhap", nhap))
app.add_handler(CommandHandler("xuat", xuat))
app.add_handler(CommandHandler("kho", kho))

print("BOT ĐANG CHẠY...")

app.run_polling()