import os
import pathlib
import tkinter as tk
from tkinter import ttk
from loguru import logger
from shutil import copyfile

from pathlib import Path
from typing import Union, Literal, Optional

# CONFIGURATION & CONSTANTS
LEVEL = "INFO"
logger.level(LEVEL)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.style = ttk.Style(master)
        self.style.theme_use("alt")
        self.app_background = "#192734"
        self.app_foreground = "gold"
        self.game_folder = str(pathlib.Path('C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\Game'))
        self.EAC_enabled: bool = False
        self.VKD3D_enabled: bool = False
        # https://github.com/soupstream/EldenRingStutterFix     (modified VKD3D)

        self.eac_status_indicator_var: tk.StringVar = tk.StringVar(
            master=self.master,
            value=self.eac_status_msg())
        self.eac_status_indicator = tk.Entry(
            master=self.master,
            # name='eac_status_indicator',
            width=40,
            textvariable=self.eac_status_indicator_var,
            foreground='green' if self.EAC_enabled else 'red',
            background=self.app_background,
            cursor='arrow',
            highlightthickness=2,
            bd=0,
            highlightcolor=self.app_background,
            highlightbackground=self.app_background,
            state=tk.DISABLED,
            disabledforeground="#20bebe",
            disabledbackground=self.app_background,
        )
        # self.eac_status_indicator_var.trace("r", lambda name, index, mode, sv=self.eac_status_indicator_var: self.eac_status_msg())
        self.eac_status_indicator.bind('<Button-1>', lambda i: self.toggle_eac())

        self.vkd3d_status_indicator_var = tk.StringVar(
            master=self.master,
            name='vkd3d_status_indicator_var',
            value=self.vkd3d_status_msg())
        self.vkd3d_status_indicator = tk.Entry(
            master=self.master,
            # name='vkd3d_status_indicator',
            width=40,
            textvariable=self.vkd3d_status_indicator_var,
            foreground='green' if not self.vkd3d_is_disabled() else 'red',
            background=self.app_background,
            cursor='arrow',
            highlightthickness=2,
            bd=0,
            highlightcolor=self.app_background,
            highlightbackground=self.app_background,
            state=tk.DISABLED,
            disabledforeground="#20bebe",
            disabledbackground=self.app_background,
        )
        self.vkd3d_status_indicator.bind('<Button-1>', lambda i: self.toggle_vkd3d())

        self.eac_status_indicator.grid()
        self.vkd3d_status_indicator.grid()

        toggle_eac_button_text = tk.StringVar(
            master=self.master,
            name='toggle_eac_button_text',
            value='Toggle EAC')
        self.toggle_EAC_button = tk.Button(
            master=self.master,
            textvariable=toggle_eac_button_text,
            foreground=self.app_foreground,
            background=self.app_background,
            command=self.toggle_eac
        )

        enable_vkd3d_button_text = tk.StringVar(
            master=self.master,
            name='enable_vkd3d_button_text',
            value='Enable VKD3D tweak by soupstream')
        self.enable_vkd3d_button = tk.Button(
            master=self.master,
            textvariable=enable_vkd3d_button_text,
            foreground=self.app_foreground,
            background=self.app_background,
            command=self.enable_vkd3d
        )

        disable_vkd3d_button_text = tk.StringVar(
            master=self.master, name='disable_vkd3d_button_text', value='Disable VKD3D tweak by soupstream')
        self.disable_vkd3d_button = tk.Button(
            master=self.master,
            textvariable=disable_vkd3d_button_text,
            foreground=self.app_foreground,
            background=self.app_background,
            command=self.disable_vkd3d
        )

        self.warring_var = tk.StringVar(
            master=self.master,
            name='warring_var',
            value=self.warning_msg()
        )
        self.warring_indicator = tk.Entry(
            master=self.master,
            name='warring',
            width=68,
            textvariable=self.warring_var,
            foreground='red',
            background=self.app_background,
            cursor='xterm',
            highlightthickness=2,
            bd=0,
            highlightcolor=self.app_background,
            highlightbackground=self.app_background,
            state=tk.DISABLED,
            disabledforeground="red",
            disabledbackground=self.app_background,
        )
        self.warring_indicator.grid()

        self.toggle_EAC_button.grid()
        self.enable_vkd3d_button.grid()
        self.disable_vkd3d_button.grid()

        self.set_current_status_of_elden()

    def game_folder_contents(self) -> list[str]:
        return os.listdir(self.game_folder)

    def warning_msg(self) -> str:
        return '⚠️ EAC may REPORT or BAN you for using VKD3D tweak in online mode ⚠️' \
            if self.EAC_enabled and self.VKD3D_enabled else ''
    
    def vkd3d_status_msg(self, overide: Optional[bool] = None) -> str:
        return f"VKD3D by soupstream Status: {'ENABLED' if (self.VKD3D_enabled if not isinstance(overide, bool) else overide) else 'DISABLED'}"

    def eac_status_msg(self, overide: Optional[bool] = None) -> str:
        return f"Easy Anti-Cheat Status: {'ENABLED' if (self.EAC_enabled if not isinstance(overide, bool) else overide) else 'DISABLED'}"

    def toggle_eac(self) -> None:
        self.disable_eac() if not self.eac_is_disabled()\
            else self.enable_eac() if self.eac_is_disabled() else logger.error('toggle failed')
        self.set_current_status_of_elden()

    def toggle_vkd3d(self) -> None:
        self.disable_vkd3d() if not self.vkd3d_is_disabled()\
            else self.enable_vkd3d() if self.vkd3d_is_disabled() else logger.error('toggle failed')
        self.set_current_status_of_elden()

    def set_current_status_of_elden(self) -> None:
        self.EAC_enabled = not self.eac_is_disabled()
        self.VKD3D_enabled = not self.vkd3d_is_disabled()

        self.eac_status_indicator.configure(
            foreground='green' if self.EAC_enabled else 'red',
            disabledforeground='green' if self.EAC_enabled else 'red',
        )

        self.vkd3d_status_indicator.configure(
            foreground='green' if self.VKD3D_enabled else 'red',
            disabledforeground='green' if self.VKD3D_enabled else 'red',
        )

        self.warring_var.set(value=self.warning_msg())

        self.eac_status_indicator.update_idletasks()
        self.vkd3d_status_indicator.update_idletasks()
        self.warring_indicator.update_idletasks()

        logger.debug(self.eac_status_indicator_var.get())
        logger.debug(self.vkd3d_status_indicator_var.get())
        logger.warning(self.warring_var.get())

    def eac_is_disabled(self):
        return len({'start_protected_game_original.exe', 'start_protected_game.exe'}.intersection(
            self.game_folder_contents())) == 2

    def vkd3d_is_disabled(self):
        return 'd3d12.dll' not in self.game_folder_contents()

    def disable_eac(self) -> None:
        if not self.eac_is_disabled():
            try:
                copyfile(self.game_folder + r'\start_protected_game.exe',
                         self.game_folder + r'\start_protected_game_original.exe')
                os.remove(self.game_folder + r'\start_protected_game.exe')
                copyfile(self.game_folder + r'\eldenring.exe',
                         self.game_folder + r'\start_protected_game.exe')
                if self.eac_is_disabled():
                    self.EAC_enabled = False
                    eac_status = self.eac_status_msg(overide=False)
                    logger.info(f"eac_status: {eac_status}")
                    self.eac_status_indicator_var.set(value=eac_status)
                else:
                    logger.error('start_protected_game_original.exe not detected after conversion')
            except FileNotFoundError:
                err_message = 'PLEASE VERIFY INTEGRITY OF GAME FILES, EAC NEEDS TO REGENERATE'
                self.eac_status_indicator_var.set(value=err_message)
                self.EAC_enabled = False
                self.eac_status_indicator_var.set(value=self.eac_status_msg(overide=False))
                logger.error(err_message)
        else:
            logger.info('Easy Anti-Cheat Already Disabled for Elden Ring')
        # self.EAC_enabled = False
        self.set_current_status_of_elden()

    def enable_eac(self) -> None:
        if 'start_protected_game_original.exe' in os.listdir(self.game_folder):
            os.remove(self.game_folder + r'\start_protected_game.exe')
            copyfile(self.game_folder + r'\start_protected_game_original.exe',
                     self.game_folder + r'\start_protected_game.exe')
            os.remove(self.game_folder + r'\start_protected_game_original.exe')

            if not self.eac_is_disabled():
                eac_status = self.eac_status_msg(overide=True)
                logger.info(f"eac_status: {eac_status}")
                self.eac_status_indicator_var.set(value=eac_status)
        else:
            logger.info('Easy Anti-Cheat Already Enabled for Elden Ring')
        self.EAC_enabled = True
        self.eac_status_indicator_var.set(value=self.eac_status_msg(overide=True))

        self.set_current_status_of_elden()

    def enable_vkd3d(self) -> None:
        # for safty ensure Easy Anti-Cheat is Disabled
        if self.EAC_enabled:
            self.disable_eac()
        if not self.VKD3D_enabled:
            copyfile(r'assets\d3d12.dll', self.game_folder + r'\d3d12.dll')
        if not self.vkd3d_is_disabled():
            self.VKD3D_enabled = True
            vkd3d_status = self.vkd3d_status_msg(overide=True)
            logger.info(f"vkd3d_status: {vkd3d_status}")
            self.vkd3d_status_indicator_var.set(value=vkd3d_status)
        self.set_current_status_of_elden()

    def disable_vkd3d(self) -> None:
        if self.VKD3D_enabled:
            os.remove(self.game_folder + r'\d3d12.dll')
        if self.vkd3d_is_disabled():
            self.VKD3D_enabled = False
            vkd3d_status = self.vkd3d_status_msg(overide=False)
            logger.info(f"vkd3d_status: {vkd3d_status}")
            self.vkd3d_status_indicator_var.set(value=vkd3d_status)
        self.set_current_status_of_elden()

    def disable_vkd3d_and_enable_eac(self) -> None:
        if self.VKD3D_enabled:
            os.remove(self.game_folder + r'\d3d12.dll')
        self.enable_eac()
        self.set_current_status_of_elden()

    @staticmethod
    def copy_save() -> None:
        app_data_path = os.environ.get('APPDATA', None)
        ...


@logger.catch()
def run_application():
    root = tk.Tk()
    root.config(bg='#474444', )
    root.resizable(True, True)
    # tracker = Tracker(root)
    app = Application(master=root)
    app.master.title("DeLag & EAC Manager")
    app.master.minsize(340, 100)
    # tracker.bind_config()
    app.mainloop()


if __name__ == "__main__":
    run_application()
