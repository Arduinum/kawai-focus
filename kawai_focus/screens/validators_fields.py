def validate_title(obj, text):
    """Валидатор поля title"""
    
    if not text:
        obj.ids.title_error.text = 'Введите название!'
