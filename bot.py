import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

# إعداد السجلات لمتابعة الأخطاء أو التشغيل
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# ضع الـ Token الخاص بك هنا
TOKEN = "8238988174:AAHsh12G_l0PajtQN1RM7rsNR4qMQhS0UgY"


# 1. دالة أمر /start (ترحيب + أزرار الأزواج)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  keyboard = [
    [
      InlineKeyboardButton("EUR/USD", callback_data="pair_eurusd"),
      InlineKeyboardButton("GBP/USD", callback_data="pair_gbpusd"),
    ],
    [
      InlineKeyboardButton("BTC/USD", callback_data="pair_btcusd"),
      InlineKeyboardButton("XAU/USD (Gold)", callback_data="pair_xauusd"),
    ],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  await update.message.reply_text(
      "🤖 أهلاً بك في بوت التحليل وإشارات التداول الذكي.\n\n"
      "الرجاء اختيار **زوج العملات** المراد تحليله:",
      reply_markup=reply_markup,
      parse_mode="Markdown",
  )


# 2. دالة التعامل مع الأزرار (اختيار الزوج ثم الانتقال للوقت)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  data = query.data

  # إذا اختار المستخدم زوج عملات، نعرض له خيارات الوقت
  if data.startswith("pair_"):
    selected_pair = data.split("_")[1].upper()
    context.user_data["selected_pair"] = selected_pair  # حفظ الزوج مؤقتاً

    time_keyboard = [
      [
        InlineKeyboardButton("1 دقيقة (1M)", callback_data="time_1m"),
        InlineKeyboardButton("3 دقائق (3M)", callback_data="time_3m"),
      ],
      [InlineKeyboardButton("5 دقائق (5M)", callback_data="time_5m")],
    ]
    reply_markup = InlineKeyboardMarkup(time_keyboard)

    await query.edit_message_text(
        text=f"📊 لقد اخترت الزوج: **{selected_pair}**\n\n"
        "الآن، اختر **الإطار الزمني (وقت الصفقة)**:",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )

  # إذا اختار المستخدم الوقت، نبدأ مرحلة تحليل السوق وهمياً أو فعلياً
  elif data.startswith("time_"):
    selected_time = data.split("_")[1].upper()
    pair = context.user_data.get("selected_pair", "EUR/USD")

    await query.edit_message_text(
        text=f"⏳ جاري فحص السوق وتحليل المؤشرات لـ **{pair}** على فريم **{selected_time}**...\n"
        "الرجاء الانتظار قليلاً تطبيق فلاتر الأخبار والشموع..."
    )

    # هنا سنقوم لاحقاً بربط محرك التحليل الفني (RSI + الشموع + الأخبار) وإرسال النتيجة النهائية!


# تشغيل البوت الرئيسي
if __name__ == "__main__":
  app = ApplicationBuilder().token(TOKEN).build()

  # إضافة الأوامر ومعالجات الأزرار
  app.add_handler(CommandHandler("start", start))
  app.add_handler(CallbackQueryHandler(button_handler))

  print("🚀 البوت يعمل الآن بنجاح ويستمع للرسائل...")
  app.run_polling()
