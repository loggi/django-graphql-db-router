try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    class MiddlewareMixin(object):
        """Dummy class not to break compatibility with django 1.8"""
        pass

from .pinning import pin_this_thread, unpin_this_thread


class PinningGraphqlDbMiddleware(MiddlewareMixin):
    """Middleware that helps in redirecting databases based on the type of
    action that graphql is performing
    """
    def process_request(self, request):
        """Set the thread's pinning flag according to the presence of the
        incoming graphql."""
        if (
            'graphql' in request.path and
            'query' in request.body and 'mutation' not in request.body
        ):
            pin_this_thread()
        else:
            unpin_this_thread()
