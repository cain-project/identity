from django.shortcuts import render


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

