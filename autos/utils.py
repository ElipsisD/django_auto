
menu = [{"title": "ГЛАВНАЯ", "url_name": "home"},
        {"title": "АВТОМОБИЛИ", "url_name": "autos"},
        {"title": "ЗАПЧАСТИ", "url_name": "spares"},
        ]

left_menu = [{"title": "НОВАЯ ЗАПЧАСТЬ", "url_name": "add_spare"}]


class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        context["menu"] = menu
        context["left_menu"] = left_menu
        return context
