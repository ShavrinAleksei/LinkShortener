from django.urls import path

from apps.link_shortener import views

app_name = 'link_shortener'

urlpatterns = [
    path('create/', views.CreateShortLinkView.as_view(), name="create_short_link"),
    path('<str:link_alias>/', views.RedirectByAliasView.as_view(), name="redirect"),
    path("success/<str:link_alias>/", views.ShortLinkSuccessView.as_view(), name="create_link_success"),
]
