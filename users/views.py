
from django.utils.translation import gettext as _
from oidc_provider.lib.claims import ScopeClaims

from users.models import Role


class OpenIDScopeClaims(ScopeClaims):
    info_roles = (_('Roles'),
                  _('Access to your current group roles.'))

    def scope_roles(self):
        return openid_userinfo_roles(self.user)

    info_groups = (_('Groups'),
                   _('Access to the list of groups of which you\'re a member.'))

    def scope_groups(self):
        return openid_userinfo_groups(self.user)


def openid_userinfo(claims, user):
    """
    Populate the response for the UserInfo endpoint.

    Should conform to OpenID Connect Core 1.0 specification, see
     https://openid.net/specs/openid-connect-core-1_0.html#rfc.section.5.1

    :param claims: Existing claims.
    :param user: The authenticated user.
    :return: All claims to include in the response.
    """

    claims['given_name'] = user.given_name
    claims['family_name'] = user.family_name
    claims['name'] = user.full_name
    claims['nickname'] = user.preferred_name
    claims['email'] = user.email
    claims['email_verified'] = False  # TODO
    claims['locale'] = user.locale
    claims['updated_at'] = user.date_updated.isoformat()

    if user.date_of_birth is not None:
        claims['birthdate'] = user.date_of_birth.isoformat()

    return claims


def openid_userinfo_groups(user):
    groups = [membership.group for membership in user.memberships.all()]
    groups = [group.get_fields() for group in groups]
    return {"groups": groups}


def openid_userinfo_roles(user):
    roles = Role.objects.filter(membership__user=user)
    roles = [role.get_fields() for role in roles]
    return {"roles": roles}

