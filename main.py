from website import create_app

# ready for myslq
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
