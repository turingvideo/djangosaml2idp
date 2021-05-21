from typing import Dict
from djangosaml2idp.models import ServiceProvider
from djangosaml2idp.processors import BaseProcessor

from ..models import GroupSAMLRole, UserSAMLRole


class AWSProcessorMixin:

    def create_identity(self, user, sp_attribute_mapping: Dict[str, str]) -> Dict[str, str]:
        results = super().create_identity(user, sp_attribute_mapping)

        context = {}
        for key in list(sp_attribute_mapping.keys()):
            if key.startswith('_'):
                context[key] = sp_attribute_mapping.pop(key)

        sp = context.get('__sp__')
        if sp:
            aws_idp_arn = context.get('_aws_idp_arn')
            for user_attr, out_attr in sp_attribute_mapping.items():
                if user_attr == 'saml_roles':
                    saml_roles = get_saml_roles(user, sp)
                    if aws_idp_arn:
                        saml_roles = [f'{r},{aws_idp_arn}' for r in saml_roles]
                    results[out_attr] = saml_roles

        return results


class AWSProcessor(AWSProcessorMixin, BaseProcessor):
    pass


def get_saml_roles(user, sp: ServiceProvider) -> list:
    group_roles = (r.name for r in GroupSAMLRole.objects.filter(group__in=user.groups.all(), provider=sp))
    user_roles = (r.name for r in UserSAMLRole.objects.filter(user=user, provider=sp))
    return list(set(group_roles).union(user_roles))
