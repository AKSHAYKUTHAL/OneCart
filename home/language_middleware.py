# from django.utils.translation import activate

# class LanguageMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         selected_language = request.session.get('selected_language', 'en')  # Default language is English
#         print(f"Selected Language: {selected_language}")

#         activate(selected_language)
#         response = self.get_response(request)
#         return response
