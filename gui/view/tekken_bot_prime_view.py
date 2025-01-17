#!/usr/bin/env python3

# Copyright (c) 2019, Alchemy Meister
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice,this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
"""
import sys
import itertools
import tkinter as tk
import tkinter.scrolledtext as tkst

from constants.overlay import OverlayLayout, OverlayPosition, OverlaySettings

class TekkenBotPrimeView():
    """
    """
    def __init__(self, root, controller):
        self.controller = controller
        self.menu_bar = tk.Menu(root)

        tekken_bot_menu = tk.Menu(self.menu_bar, tearoff=0)
        tekken_bot_menu.add_command(
            label='Restart', command=self.controller.restart
        )

        preferences_submenu = tk.Menu(tekken_bot_menu, tearoff=0)
        is_save_to_file_enabled = tk.BooleanVar(
            value=self.controller.is_save_to_file_enabled()
        )
        preferences_submenu.add_checkbutton(
            label='Save Log',
            onvalue=True, offvalue=False,
            variable=is_save_to_file_enabled,
            command=lambda: self.controller.enable_save_to_file(
                is_save_to_file_enabled.get()
            )
        )
        is_auto_scroll_enabled = tk.BooleanVar(value=True)
        preferences_submenu.add_checkbutton(
            label='Scroll on Output',
            onvalue=True, offvalue=False,
            variable=is_auto_scroll_enabled,
            command=lambda: self.controller.enable_auto_scroll(
                is_auto_scroll_enabled.get()
            )
        )

        # TODO change command
        preferences_submenu.add_command(label='Settings', command=None)

        tekken_bot_menu.add_cascade(
            label='Preferences', menu=preferences_submenu
        )

        is_memory_overwrite_panel_visible = tk.BooleanVar()
        view = tk.Menu(self.menu_bar, tearoff=0)
        view.add_checkbutton(
            label='Toggle Memory Overwrite',
            variable=is_memory_overwrite_panel_visible,
            command=lambda: self.controller.show_memory_override(
                is_memory_overwrite_panel_visible.get()
            )
        )

        punish_alarm_menu = tk.Menu(self.menu_bar, tearoff=0)

        self.enable_punish_alarm = tk.BooleanVar(value=False)
        punish_alarm_menu.add_checkbutton(
            label='Enable',
            variable=self.enable_punish_alarm,
            command=lambda: self.controller.enable_punish_alarm(
                self.enable_punish_alarm.get()
            )
        )

        self.overlay_menu = tk.Menu(self.menu_bar, tearoff=0)

        self.enable_overlay = tk.BooleanVar(value=False)
        self.overlay_menu.add_checkbutton(
            label='Enable',
            variable=self.enable_overlay,
            command=lambda: self.controller.enable_overlay(
                self.enable_overlay.get()
            )
        )

        self.overlay_auto_hide = tk.BooleanVar(value=False)
        self.overlay_menu.add_checkbutton(
            label='Auto-hide',
            variable=self.overlay_auto_hide,
            command=lambda: self.controller.enable_overlay_auto_hide(
                self.overlay_auto_hide.get()
            )
        )

        self.overlay_layout = tk.StringVar()
        overlay_layout_submenu = TekkenBotPrimeView.__create_populated_menu(
            self.overlay_layout,
            self.controller.populate_overlay_layouts_submenu(),
            self.controller.overlay_layout_change
        )

        self.overlay_menu.add_cascade(
            label='Layout', menu=overlay_layout_submenu
        )
        self.overlay_number = 0
        self.__overlays_settings = [
            {} for _ in itertools.repeat(None, list(OverlayLayout).pop().value)
        ]
        for index in range(list(OverlayLayout).pop().value):
            self.__initialize_overlay_menu_variables(index)

        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(
            label='Check for Updates...',
            command=self.controller.check_for_updates
        )

        self.menu_bar.add_cascade(label='Tekken Bot', menu=tekken_bot_menu)
        self.menu_bar.add_cascade(label='View', menu=view)
        self.menu_bar.add_cascade(label='Punish Alarm', menu=punish_alarm_menu)
        self.menu_bar.add_cascade(label='Overlay', menu=self.overlay_menu)
        self.menu_bar.add_cascade(label='Help', menu=help_menu)

        root.config(menu=self.menu_bar)

        self.memory_overwride_panel = None

        self.console = tkst.ScrolledText(root, state='disabled')
        self.console.grid(column=0, row=1, sticky='NSEW')

        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

    def adapt_overlay_menu_to_overlay_number(
            self, overlay_number, refresh=False
    ):
        if overlay_number != self.overlay_number or refresh:
            self.overlay_number = overlay_number

            del_end_index = None
            if self.overlay_number == 1:
                try:
                    del_end_index = self.overlay_menu.index('Overlay 1') - 1
                except tk.TclError:
                    pass
            else:
                try:
                    del_end_index = self.overlay_menu.index('Mode') - 1
                except tk.TclError:
                    pass

            if del_end_index is not None:
                del_start_index = self.overlay_menu.index(tk.END)
                for del_index in range(del_start_index, del_end_index, -1):
                    try:
                        self.overlay_menu.delete(del_index)
                    except tk.TclError:
                        pass

            for index in range(list(OverlayLayout).pop().value):
                if self.overlay_number == 1:
                    target_overlay_menu = self.overlay_menu
                else:
                    target_overlay_menu = tk.Menu(tearoff=0)
                for (enum, menu) in self.__create_overlay_menu(index):
                    self.__overlays_settings[index]['parent'] = (
                        target_overlay_menu
                    )
                    if index < self.overlay_number:
                        target_overlay_menu.add_cascade(
                            label=getattr(enum, 'printable_name'),
                            menu=menu
                        )
                if self.overlay_number != 1 and index < self.overlay_number:
                    self.overlay_menu.add_cascade(
                        label='Overlay {}'.format(index + 1),
                        menu=target_overlay_menu
                    )

    def enable_overlay_position(self, str_position, enable):
        for overlay_settings in self.__overlays_settings:
            settings_dict = overlay_settings[OverlaySettings.POSITION]
            settings_dict['menu'].entryconfig(
                str_position, state='normal' if enable else 'disabled'
            )
            settings_dict['menu_state'][str_position] = (
                settings_dict['menu'].entryconfig(str_position)['state'][4]
            )

    def load_overlay_themes(self):
        for overlay_index, overlay_settings in enumerate(
                self.__overlays_settings
        ):
            if overlay_index < self.overlay_number:
                overlay_settings['parent'].delete(tk.END)
                overlay_theme_submenu = (
                    TekkenBotPrimeView.__create_populated_menu(
                        overlay_settings[OverlaySettings.THEME][
                            'variable'
                        ],
                        self.controller.populate_overlay_themes_submenu(
                            overlay_settings[OverlaySettings.MODE]['variable']
                            .get()
                        ),
                        self.controller.overlay_theme_change,
                        overlay_index=overlay_index
                    )
                )

                overlay_settings['parent'].add_cascade(
                    label=getattr(OverlaySettings.THEME, 'printable_name'),
                    menu=overlay_theme_submenu
                )

    def restore_previous_overlays_settings(self, setting_key):
        for overlay_index in range(len(self.__overlays_settings)):
            setting_variable = (
                self.__overlays_settings[overlay_index][setting_key]
            )
            setting_variable['variable'].set(setting_variable['previous_value'])

    def set_overlay_setting(
            self, overlay_index, setting_key, setting_value, set_previous=True
    ):
        setting_variable = (
            self.__overlays_settings[overlay_index][setting_key]
        )
        repeated_variable = self.__repeat_value_checker(
            overlay_index, setting_key, setting_value
        )
        if repeated_variable:
            repeated_variable.set(setting_variable['variable'].get())

        setting_variable['variable'].set(setting_value)
        if set_previous:
            setting_variable['previous_value'] = setting_value

    def set_in_all_overlay_settings(self, setting_key, setting_enum):
        for overlay_index in range(len(self.__overlays_settings)):
            self.set_overlay_setting(
                overlay_index, setting_key, setting_enum, set_previous=False
            )

    def show_memory_overwrite_panel(self, show):
        if self.memory_overwride_panel:
            if show:
                self.memory_overwride_panel.grid(column=0, row=0)
            else:
                self.memory_overwride_panel.grid_remove()

    def __create_overlay_menu(self, overlay_index):
        variables = self.__initialize_overlay_menu_variables(overlay_index)

        overlay_mode_submenu = self.__create_populated_integrity_menu(
            self.controller.populate_overlay_modes_submenu(),
            callback=self.__update_overlay_themes_swap,
            overlay_index=overlay_index,
            return_bool=False,
            setting_key=OverlaySettings.MODE,
            variable=variables[0],
        )

        overlay_position_submenu = self.__create_populated_integrity_menu(
            self.controller.populate_overlay_positions_submenu(),
            callback=self.controller.overlay_position_change,
            overlay_index=overlay_index,
            setting_key=OverlaySettings.POSITION,
            variable=variables[1]
        )

        overlay_theme_submenu = TekkenBotPrimeView.__create_populated_menu(
            variables[2],
            self.controller.populate_overlay_themes_submenu(variables[0].get()),
            self.controller.overlay_theme_change,
            overlay_index=overlay_index
        )

        menus = [
            overlay_mode_submenu,
            overlay_position_submenu,
            overlay_theme_submenu
        ]

        enums = list(OverlaySettings)
        for overlay_setting, menu in zip(enums, menus):
            self.__initialize_overlay_menu_state(
                overlay_index, overlay_setting, menu
            )

        return ((enum, menu) for (enum, menu) in zip(enums, menus))

    def __create_populated_integrity_menu(self, menu_list, **kwargs):
        menu = tk.Menu(master=None, tearoff=0)
        for value, label in menu_list:
            menu.add_radiobutton(
                label=label,
                variable=kwargs.get('variable'),
                value=value,
                command=lambda: self.__integrity_checker(
                    kwargs.get('callback'),
                    kwargs.get('overlay_index'),
                    kwargs.get('setting_key'),
                    return_bool=kwargs.get('return_bool', True)
                )
            )
        return menu

    def __initialize_overlay_menu_state(
            self, overlay_index, overlay_setting, menu
    ):
        settings_dict = (
            self.__overlays_settings[overlay_index][overlay_setting]
        )
        previous_menu_state = settings_dict.get('menu_state')
        last_entry = menu.index(tk.END)
        last_entry = last_entry + 1 if last_entry else 0
        if previous_menu_state is not None:
            for label, state in previous_menu_state.items():
                menu.entryconfig(label, state=state)
        settings_dict['menu'] = menu
        settings_dict['menu_state'] = {
            menu.entryconfig(index)['label'][4]:
            menu.entryconfig(index)['state'][4]
            for index in range(last_entry)
        }
        return menu

    def __initialize_overlay_menu_variables(self, overlay_index):
        variables = [tk.StringVar(), tk.StringVar(), tk.StringVar()]

        enums = list(OverlaySettings)

        sys.stdout.write(
            'GUI variable init - ENTER: Overlay Slot: {}'.format(
                overlay_index + 1
            )
        )

        for index, (var, enum) in enumerate(zip(variables, enums)):
            previous_dict = self.__overlays_settings[overlay_index].get(enum)
            previous_value = None

            if previous_dict:
                sys.stdout.write(
                    'GUI variable init - PREVIOUS DICT FOUND: '
                    'Variable: {}, Previous Value: {}'.format(
                        previous_dict['variable'].get(),
                        previous_dict['previous_value']
                    )
                )
                sys.stdout.write(
                    'GUI variable init - PREVIOUS DICT: {}'.format(
                        previous_dict
                    )
                )
                variables[index] = previous_dict['variable']
            else:
                self.__overlays_settings[overlay_index][enum] = {
                    'previous_value': previous_value,
                    'variable': var
                }
                sys.stdout.write(
                    'GUI variable init - NOT DICT, CREATING: '
                    'Variable: {}, Previous Value: {}'.format(
                        var.get(), previous_value
                    )
                )

        sys.stdout.write('Integrity checker - EXIT')
        return variables

    def __integrity_checker(
            self,
            callback,
            overlay_index,
            setting_key,
            return_bool=True
    ):
        setting_dict = self.__overlays_settings[overlay_index][setting_key]
        repeated_variable = self.__repeat_value_checker(
            overlay_index, setting_key, setting_dict['variable'].get()
        )
        sys.stdout.write(
            'Integrity checker - ENTER: Overlay Slot: '
            '{}, Setting Key: {}, Value: {}, Previous Value: {}'.format(
                overlay_index + 1,
                setting_key.name,
                setting_dict['variable'].get(),
                setting_dict['previous_value']
            )
        )
        if repeated_variable:
            sys.stdout.write(
                'Integrity checker - REPEATED FOUND: '
                'Value: {}, Previous Value: {}'.format(
                    repeated_variable['variable'].get(),
                    repeated_variable['previous_value']
                )
            )
            repeated_variable['variable'].set(
                setting_dict['previous_value']
            )
            repeated_variable['previous_value'] = setting_dict[
                'previous_value'
            ]
            sys.stdout.write(
                'Integrity checker - REPEATED UPDATED: '
                'Value: {}, Previous Value: {}'.format(
                    repeated_variable['variable'].get(),
                    repeated_variable['previous_value']
                )
            )

        setting_dict['previous_value'] = setting_dict['variable'].get()
        sys.stdout.write(
            'Integrity checker - EXIT: Overlay Slot: '
            '{}, Setting Key: {}, Value: {}, Previous Value: {}'.format(
                overlay_index + 1,
                setting_key.name,
                setting_dict['variable'].get(),
                setting_dict['previous_value']
            )
        )
        callback(
            setting_dict['variable'].get(),
            overlay_index,
            bool(repeated_variable) if return_bool else repeated_variable
        )

    def __repeat_value_checker(
            self,
            overlay_index,
            setting_key,
            reference,
            exclude_value=getattr(OverlayPosition.DRAGGABLE, 'name')
    ):
        repeated_variable = None
        reference_dict = self.__overlays_settings[overlay_index][setting_key]
        if(
                reference != exclude_value
                and reference_dict['variable'].get()
                != reference_dict['previous_value']
        ):
            repeated_variable = next(
                (
                    overlay_setting[setting_key]
                    for index, overlay_setting in enumerate(
                        self.__overlays_settings
                    )
                    if(
                        index != overlay_index
                        and overlay_setting[setting_key]['variable'].get()
                        == reference
                    )
                )
                , None
            )
        return repeated_variable

    def __update_overlay_themes_swap(
            self, overlay_mode_name, overlay_index, repeated_variable
    ):
        if repeated_variable:
            theme_menu = (
                self.__overlays_settings[overlay_index][OverlaySettings.THEME][
                    'menu'
                ]
            )
            previous_index, previous_theme_menu = next(
                (
                    (index, overlay_setting[OverlaySettings.THEME]['menu'])
                    for index, overlay_setting in enumerate(
                        self.__overlays_settings
                    )
                    if(
                        index != overlay_index
                        and overlay_setting[OverlaySettings.MODE][
                            'variable'
                        ].get()
                        == repeated_variable.get('variable').get()
                    )
                )
                , (None, None)
            )

            swap_index_menus = (
                [overlay_index, previous_theme_menu],
                [previous_index, theme_menu]
            )
            for index, (swap_index, menu) in enumerate(swap_index_menus):
                if index < self.overlay_number:
                    self.__overlays_settings[swap_index]['parent'].delete(
                        tk.END
                    )
                    last_index = menu.index(tk.END)
                    last_index = last_index + 1 if last_index is not None else 0
                    for menu_entry_index in range(last_index):
                        menu.entryconfig(
                            menu_entry_index,
                            command=(
                                lambda i=swap_index:
                                self.controller.overlay_theme_change(
                                    self.__overlays_settings[i][
                                        OverlaySettings.THEME
                                    ]['variable'].get(),
                                    i
                                )
                            )
                        )

                    self.__overlays_settings[swap_index]['parent'].add_cascade(
                        label=getattr(OverlaySettings.THEME, 'printable_name'),
                        menu=menu
                    )
            (
                self.__overlays_settings[overlay_index][OverlaySettings.THEME],
                self.__overlays_settings[previous_index][OverlaySettings.THEME]
            ) = (
                self.__overlays_settings[previous_index][OverlaySettings.THEME],
                self.__overlays_settings[overlay_index][OverlaySettings.THEME]
            )


        self.controller.overlay_mode_change(
            overlay_mode_name, overlay_index, bool(repeated_variable)
        )

    @staticmethod
    def __create_populated_menu(
            variable, menu_list, callback, overlay_index=None
    ):
        menu = tk.Menu(master=None, tearoff=0)
        for value, label in menu_list:
            menu.add_radiobutton(
                label=label,
                variable=variable,
                value=value,
                command=(
                    lambda: callback(variable.get()) if overlay_index is None
                    else callback(variable.get(), overlay_index)
                )
            )
        return menu
