
def _patch_build_authn_response():
    from django.contrib.auth import get_user_model
    from djangosaml2idp import views
    from djangosaml2idp.models import ServiceProvider

    User = get_user_model()

    class PatchedServiceProvider(ServiceProvider):
        attribute_mapping = None

        class Meta:
            proxy = True

    _build_authn_response = views.build_authn_response

    def build_authn_response(user: User, authn, resp_args, service_provider: ServiceProvider) -> list:  # type: ignore
        attribute_mapping = service_provider.attribute_mapping
        clazz = service_provider.__class__
        attribute_mapping['__sp__'] = service_provider
        service_provider.__class__ = PatchedServiceProvider
        service_provider.attribute_mapping = attribute_mapping
        try:
            return _build_authn_response(user, authn, resp_args, service_provider)
        finally:
            service_provider.__class__ = clazz

    views.build_authn_response = build_authn_response


_patch_build_authn_response()
