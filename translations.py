def translate(key: str, lang: str = "uz") -> str:
    messages = {
        "intro": {
            "uz": "Assalomu alaykum! Men Chatul-Hikma AI botman.",
            "ru": "Ассаламу алейкум! Я бот Chatul-Hikma AI.",
            "en": "Peace be upon you! I am Chatul-Hikma AI bot.",
            "kg": "Салам! Мен Chatul-Hikma AI боту болом."
        },
        "choose_action": {
            "uz": "Quyidagilardan birini tanlang:",
            "ru": "Выберите одно из следующих:",
            "en": "Choose one of the following:",
            "kg": "Төмөнкүлөрдүн бирин тандаңыз:"
        },
        "send_question": {
            "uz": "Iltimos, savolingizni yozing:",
            "ru": "Пожалуйста, напишите ваш вопрос:",
            "en": "Please write your question:",
            "kg": "Сураныч, сурооңузду жазыңыз:"
        }
    }
    return messages.get(key, {}).get(lang, "")