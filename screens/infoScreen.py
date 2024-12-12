import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
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
                text="• Prześlij zdjęcie lub plik pdf z wynikami badań laboratoryjnych oraz podaj datę wykonania badania\n"
                "• Analizuj wyniki odrazu po dodaniu lub z ekranu Przeglądaj wyniki\n"
                "• Możesz także śledzić zmianę parametrów w czasie\n \n"
                "[color=#FF0000][b]UWAGA![/b][/color]: Interpretacja wyników badań krwi zawsze powinna odbywać się w konsultacji z lekarzem. "
                "Pamiętaj, że nawet jeśli któryś z parametrów odbiega od normy, "
                "nie zawsze oznacza to poważny problem – czasem to tylko sygnał, że warto lepiej zadbać o organizm.",
                halign="left",
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
                text="• [b]Erytrocyty (RBC)[/b]: Czerwone krwinki, które przenoszą tlen w Twoim ciele\n"
                     "• [b]Leukocyty (WBC)[/b]: Białe krwinki, które walczą z infekcjami i chorobami\n"
                     "• [b]Hemoglobina (HGB)[/b]: Białko w czerwonych krwinkach, które łapie tlen i roznosi go po organizmie\n"
                     "• [b]Hematokryt (HCT)[/b]: Procentowy udział krwinek czerwonych we krwi\n"
                     "• [b]MCV[/b]: Średnia objętość krwinki czerwonej, pozwala ocenić typ anemii\n"
                     "• [b]MCH[/b]: Średnia masa hemoglobiny w erytrocycie pomaga diagnozować zaburzenia czerwonych krwinek\n"
                     "• [b]MCHC[/b]: Średnie stężenie hemoglobiny w erytrocytach, ocenia ich jakość\n"
                     "• [b]MPV[/b]: Średnia objętość płytek krwi pomaga w ocenie ich funkcji\n",
                halign="left",
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
