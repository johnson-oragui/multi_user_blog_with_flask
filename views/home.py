from views import views


@views.get('/')
def index():
    return f'INDEX'
