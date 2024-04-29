from django.http import HttpResponse, HttpRequest


def healthcheck(request: HttpRequest) -> HttpResponse:  # noqa: ARG001
    return HttpResponse("OK", content_type="text/plain")
