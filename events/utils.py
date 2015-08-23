# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern


def add_optional_trailing_slashes(urlpatterns):
    """
    Take a list of urls and add trailing slashes.
    If slashes already are in regex, make them optional.

    Based on Django REST Framework apply_suffix_patterns

    :return: list of urlpatterns
    :rtype: list[RegexURLPattern] | list[RegexURLResolver]
    """
    urls = list()
    for pattern in urlpatterns:
        # check whether URL is nested or not
        if isinstance(pattern, RegexURLResolver):
            regex = pattern.regex.pattern.rstrip('$').rstrip('/')
            patterns = add_optional_trailing_slashes(pattern.url_patterns)
            namespace = pattern.namespace
            app_name = pattern.app_name
            kwargs = pattern.default_kwargs
            urls.append(url(regex + '$', include(patterns, namespace, app_name), kwargs))
            urls.append(url(regex + '/$', include(patterns, namespace, app_name), kwargs))

        elif isinstance(pattern, RegexURLPattern):
            regex = pattern.regex.pattern.rstrip('$').rstrip('/')
            view = pattern._callback or pattern._callback_str
            kwargs = pattern.default_args
            name = pattern.name
            urls.append(url(regex + '$', view, kwargs, name))
            urls.append(url(regex + '/$', view, kwargs, name))
    return urls
