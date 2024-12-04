import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivymd.uix import dialog
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)
from kivymd.uix.divider import MDDivider
from kivymd.uix.list import (
    MDListItem,
    MDListItemLeadingIcon,
    MDListItemSupportingText,
)

Builder.load_file(os.path.join(os.path.dirname(__file__), 'info_screen.kv'))


class InfoScreen(Screen):
    '''Handle actions for info screen'''
    def __init__(self, **kwargs):
        super(InfoScreen, self).__init__(**kwargs)
        self.info_dialog = None
        self.about_dialog = None
        self.parameters_dialog = None

    def show_info_dialog(self):
        self.info_dialog = MDDialog(
            # ----------------------------Icon-----------------------------
            MDDialogIcon(
                icon="bookmark",
            ),
            # -----------------------Headline text-------------------------
            MDDialogHeadlineText(
                text="Instrukcja obsługi",
            ),
            # -----------------------Supporting text-----------------------
            MDDialogSupportingText(
                text="Lorem ipsum dolor sit amet, consectetur adipiscing elit,"
                     "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"
                     "Ut enim ad minim veniam, quis nostrud exercitation"
                     "ullamco laboris nisi ut aliquip ex ea commodo consequat.",
            ),
            # ---------------------Button container------------------------
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Zamknij"),
                    style="text",
                    on_release=lambda *args: self.info_dialog.dismiss()
                ),
                spacing="8dp",
            ),
            # -------------------------------------------------------------
        )
        self.info_dialog.open()

    def show_about_dialog(self):
        self.about_dialog = MDDialog(
            # ----------------------------Icon-----------------------------
            MDDialogIcon(
                icon="information",
            ),
            # -----------------------Headline text-------------------------
            MDDialogHeadlineText(
                text="O aplikacji",
            ),
            # -----------------------Supporting text-----------------------
            MDDialogSupportingText(
                text="Aplikacja [b]LabResults[/b] to nowoczesne narzędzie wspierające zarządzanie zdrowiem.\n \n"
                     "Umożliwia: \n \n"
                     "• bezpieczne [b]przechowywanie wyników[/b] badań laboratoryjnych\n \n"
                     "• [b]wizualizacje[/b] najważniejszych parametrów krwi na przejrzystych wykresach\n \n"
                     "• [b]monitorowanie zmian[/b] w zdrowiu w czasie.\n \n"
                    "Łatwa w obsłudze, pozwala na szybkie dodawanie nowych wyników, aby mieć je zawsze pod ręką. ",
                halign="left",
            ),
            # ---------------------Button container------------------------
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Zamknij"),
                    style="text",
                    on_release=lambda *args: self.about_dialog.dismiss()
                ),
                spacing="8dp",
            ),
            # -------------------------------------------------------------
        )
        self.about_dialog.open()

    def show_parameters_dialog(self):
        self.parameters_dialog = MDDialog(
            # ----------------------------Icon-----------------------------
            MDDialogIcon(
                icon="water",
            ),
            # -----------------------Headline text-------------------------
            MDDialogHeadlineText(
                text="Badane parametry",
            ),
            # -----------------------Supporting text-----------------------
            MDDialogSupportingText(
                text="Lorem ipsum dolor sit amet, consectetur adipiscing elit,"
                     "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"
                     "Ut enim ad minim veniam, quis nostrud exercitation"
                    "ullamco laboris nisi ut aliquip ex ea commodo consequat.",
            ),
            # ---------------------Button container------------------------
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Zamknij"),
                    style="text",
                    on_release=lambda *args: self.parameters_dialog.dismiss()
                ),
                spacing="8dp",
            ),
            # -------------------------------------------------------------
        )
        self.parameters_dialog.open()

    def switch_to_main_screen(self):
        '''Switch to the main screen'''
        self.manager.current = 'main'
