def greet_skill(user_input):
    """
    Greet skill - responds to greetings from users
    """
    greetings = ['hello', 'hi', 'hey', 'greetings']
    user_input_lower = user_input.lower()
    
    for greeting in greetings:
        if greeting in user_input_lower:
            return "Hello! How can I help you today?"
    
    return None


def faq_skill(user_input):
    """
    FAQ skill - responds to frequently asked questions
    """
    faqs = {
        'what is your name': 'I am Vishal AI Bot, your virtual assistant.',
        'what can you do': 'I can help you with greetings, answer FAQs, and assist with various tasks.',
        'how are you': 'I am doing great! Thank you for asking. How can I assist you?',
        'who created you': 'I was created by Vishal Anand.'
    }
    
    user_input_lower = user_input.lower().strip()
    
    for question, answer in faqs.items():
        if question in user_input_lower:
            return answer
    
    return None
