from kivy.utils import hex_colormap
from kivy.uix.widget import Widget
from materialyoucolor.utils.platform_utils import SCHEMES
from kivymd.uix.menu import MDDropdownMenu


class MenuApp:
    """Класс для меню приложения"""
    
    menu: MDDropdownMenu = None

    def open_menu(self, menu_button) -> None:
        """Открывает выпадающее меню"""

        menu_items = []
        
        for item, method in {
            'Цвет темы': lambda: self.set_palette(),
            'Стиль темы': lambda: self.switch_theme(),
            'Тип схемы': lambda: self.set_scheme_type(),
            'Новый таймер': None
        }.items():
            menu_items.append(
                {
                    'text': item,
                    'on_release': method,
                }
            )
        
        self.menu = MDDropdownMenu(
            caller=menu_button,
            items=menu_items,
        )
        self.menu.open()

    def switch_palette(self, selected_palette: str) -> None:
        """Переключает основной цвет темы"""
        
        self.theme_cls.primary_palette = selected_palette

    def switch_theme(self) -> None:
        """Переключает светлую/тёмную тему"""
        
        self.theme_cls.switch_theme()

    def set_palette(self) -> None:
        """Формирует и открывает меню выбора палитры"""
        
        instance_from_menu = self.get_instance_from_menu('Set palette')
        available_palettes = [
            name_color.capitalize() for name_color in hex_colormap.keys()
        ]

        menu_items = []
        for name_palette in available_palettes:
            menu_items.append(
                {
                    'text': name_palette,
                    'on_release': lambda x=name_palette: self.switch_palette(x),
                }
            )
        MDDropdownMenu(
            caller=instance_from_menu,
            items=menu_items,
        ).open()

    def set_scheme_type(self) -> None:
        """Формирует и открывает меню выбора типа цветовой схемы"""
        
        instance_from_menu = self.get_instance_from_menu("Switch scheme type")

        menu_items = []
        for scheme_name in SCHEMES.keys():
            menu_items.append(
                {
                    'text': scheme_name,
                    'on_release': lambda x=scheme_name: self.update_scheme_name(x),
                }
            )
        MDDropdownMenu(
            caller=instance_from_menu,
            items=menu_items,
        ).open()

    def update_scheme_name(self, scheme_name: str) -> None:
        """Обновляет тип цветовой схемы"""
        
        self.theme_cls.dynamic_scheme_name = scheme_name

    def get_instance_from_menu(self, name_item: str) -> Widget:
        """Возвращает экземпляр элемента меню по его названию"""
        
        index = 0
        rv = self.menu.ids.md_menu
        opts = rv.layout_manager.view_opts
        datas = rv.data[0]

        for data in rv.data:
            if data.get('text') == name_item:
                index = rv.data.index(data)
                break

        instance = rv.view_adapter.get_view(
            index, datas, opts[index].get('viewclass')
        )
        return instance

    def disabled_widgets(self) -> None:
        """Переключает активность виджетов (блокирует/разблокирует)"""
        
        for widget in self.root.ids.widget_box.children:
            widget.disabled = not widget.disabled

        for widget in self.root.ids.custom_widget_box.children:
            widget.disabled = not widget.disabled
