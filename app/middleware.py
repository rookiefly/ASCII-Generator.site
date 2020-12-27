from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.conf import settings
from django.utils import translation


class ForceDefaultLanguageMiddleware(MiddlewareMixin):
    """
    Ignore Accept-Language HTTP headers

    This will force the I18N machinery to always choose settings.LANGUAGE_CODE
    as the default initial language, unless another one is set via sessions or cookies

    Should be installed *before* any middleware that checks request.META['HTTP_ACCEPT_LANGUAGE'],
    namely django.middleware.locale.LocaleMiddleware
    """

    def process_request(self, request):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            del request.META['HTTP_ACCEPT_LANGUAGE']


class LanguageURLRedirectMiddleware(MiddlewareMixin):
    """
    Checks if url is containing language code like "domain.com/ru/something/",
    and then middleware is activating this language for user
    with redirecting him to url without language code like "domain.com/something/".

    Made for SEO purposes, normal use of website will not trigger this.
    """

    def process_request(self, request):
        path_split = request.path.split('/')
        if path_split and len(path_split) >= 2:
            language = path_split[1]  # ex. "ru"
            if language in settings.LANGUAGES_SHORT_CODES:
                translation.activate(language)
                if len(path_split) == 2:
                    return redirect('/')
                return redirect('/' + '/'.join(path_split[2:]))

    def process_response(self, request, response):
        path_split = request.path.split('/')
        if path_split and len(path_split) >= 2:
            language = path_split[1]  # ex. "ru"
            if language in settings.LANGUAGES_SHORT_CODES:
                translation.activate(language)
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        return response
