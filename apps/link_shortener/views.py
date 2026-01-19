from django.contrib import messages
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from apps.link_shortener.models import ShortLink


class CreateShortLinkView(CreateView):
    model = ShortLink
    fields = ["url"]
    template_name = "create_short_link.html"
    
    def get_success_url(self):
        return reverse(
            "link_shortener:create_link_success",
            kwargs={"link_alias": self.object.alias}  
        )

class ShortLinkSuccessView(DetailView):
    model = ShortLink
    template_name = "create_link_success.html"
    context_object_name = "short_link"

    def get_object(self):
        alias = self.kwargs.get("link_alias")
        return get_object_or_404(ShortLink, alias=alias)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['short_url'] = self.request.build_absolute_uri(self.object.get_absolute_url())
        return context

@method_decorator(csrf_exempt, name='dispatch')
class RedirectByAliasView(View):
    def get(self, request: HttpRequest, link_alias: str):
        try:
            short_link = ShortLink.objects.get(alias=link_alias)
        except ShortLink.DoesNotExist:
            return error_view(request, code=404, message="This short link does not exist.")

        if not short_link.is_active:
            return error_view(request, code=403, message="This link is inactive.")

        if short_link.is_expired():
            return error_view(request, code=410, message="This link has expired.")
        
        short_link.increment_clicks()
        return redirect(short_link.url)
    
def error_view(request, code=404, message="An error occurred"):
    return render(
        request,
        "error.html",
        context={
            "code": code,
            "message": message
        },
        status=code
    )

