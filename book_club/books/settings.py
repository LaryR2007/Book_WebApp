LOGIN_URL = 'login'  # Forces users to log in before accessing protected pages
LOGIN_REDIRECT_URL = 'books:genre_list'  # Redirects users to genre list after login
LOGOUT_REDIRECT_URL = 'books:login' 