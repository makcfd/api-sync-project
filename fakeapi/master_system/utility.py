from requests import request
from django.conf import settings


def synchronize_to_external_api(type, instance, created=False, delete=False):
    base_url = (
        settings.BASE_JSON_PH_URL + "posts"
        if type == "post"
        else settings.BASE_JSON_PH_URL + "comments"
    )
    url = base_url + "/" + str(instance.id)
    if delete:
        response = request(
            method="DELETE",
            url=url,
        )
    elif created:
        response = request(
            method="POST",
            url=base_url,
            data=instance.json(),
        )
    else:
        response = request(method="PUT", url=url, data=instance.json())
    return response.status_code
