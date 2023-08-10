from flask import render_template, request

from website import create_app
# from website import .models

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


