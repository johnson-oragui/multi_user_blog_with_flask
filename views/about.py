from views import views

@views.route('/about')
def about():
    
    return f'<p>about page</p>'