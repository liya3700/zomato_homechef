from flask import redirect, render_template, request, url_for


def init_routes(app):
    
    @app.route('/')
    def initial():
        return redirect(url_for('index'))
    
    
    @app.route('/home')
    def index():
        return render_template('index.html')