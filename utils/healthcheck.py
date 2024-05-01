from django.http import HttpRequest, HttpResponse


def healthcheck(request: HttpRequest) -> HttpResponse:  # noqa: ARG001
    return HttpResponse("OK", content_type="text/plain")
