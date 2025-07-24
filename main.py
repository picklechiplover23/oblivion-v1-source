# Cracked by rafeed


import requests
import yaml
import logging
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base_path, relative_path)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OblivionGUI:
    """A GUI application for sending Discord webhook pings in Normal or Switch mode. Free Edition."""
    DEFAULT_CONFIG = {'message': '@everyone', 'username': 'Oblivion V1', 'avatar_url': 'https://cdn.discordapp.com/attachments/1397910466088665178/1397910550452899940/DarkSdsadsahard.png?ex=68837127&is=68821fa7&hm=ed4e1981b3495f49cf21015720071df8853a1ef1a40c3f7e378e78f177f72814&', 'delay': 2.5, 'rate_limit_backoff': 60, 'max_retries': 3, 'message_limit': 9000, 'total_pings': 450000}

    def __init__(self, root: tk.Tk, config_file: str):
        if sys.platform == 'win32':
            try:
                import ctypes
                myappid = 'oblivion.v1.free'
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            except Exception as e:
                pass  # postinserted
        else:  # inserted
            pass  # postinserted
        self.root = root
        self.root.title('Oblivion V1 - Free Edition')
        self.config_file = resource_path(config_file)
        self.config = self._load_config(self.config_file)
        self.webhook_groups = self._load_webhooks(resource_path(self.config['webhooks_file']))
        self.shard_status = {shard: False for shard in self.webhook_groups}
        self.message_counts = {}
        self.threads = {}
        self.mode = tk.StringVar(value='parallel')
        self.current_switch_shard = None
        self.rate_limit_backoff = self.config.get('rate_limit_backoff', self.DEFAULT_CONFIG['rate_limit_backoff'])
        self.max_retries = self.config.get('max_retries', self.DEFAULT_CONFIG['max_retries'])
        self.message_limit = self.config.get('message_limit', self.DEFAULT_CONFIG['message_limit'])
        self.total_pings = self.config.get('total_pings', self.DEFAULT_CONFIG['total_pings'])
        self._settings_fields = [('Message:', 'message_var', tk.StringVar, 'message'), ('Username:', 'username_var', tk.StringVar, 'username'), ('Avatar URL:', 'avatar_var', tk.StringVar, 'avatar_url'), ('Delay (seconds):', 'delay_var', tk.DoubleVar, 'delay'), ('Rate Limit Backoff (seconds):', 'backoff_var', tk.DoubleVar, 'rate_limit_backoff'), ('Max Retries:', 'retries_var', tk.IntVar, 'max_retries'), ('Message Limit per Webhook:', 'limit_var', tk.IntVar, 'message_limit'), ('Total Pings per Shard (Sequential Mode):', 'total_pings_var', tk.IntVar, 'total_pings')]
        for _, varname, vartype, key in self._settings_fields:
            value = self.config.get(key, self.DEFAULT_CONFIG[key])
            setattr(self, varname, vartype(value=value))
        self._set_window_icon(resource_path('icon.ico'))
        self.themes = self._load_themes(resource_path('themes.json'))
        self.theme_options = ['Default'] + sorted(self.themes.keys()) + ['Custom']
        self.theme_var = tk.StringVar(value='Default')
        self.config['theme'] = self.config.get('theme', 'Default')
        self._setup_gui()
                print(f'Warning: Could not set AppUserModelID: {e}')

    def _load_file_with_error_handling(self, path, loader, filetype):
        try:
            with open(path, 'r') as file:
                pass  # postinserted
        except FileNotFoundError:
                data = loader(file)
                if not data:
                    raise ValueError(f'Empty {filetype} file')
                return data
                logger.error(f'{filetype.capitalize()} file {path} not found')
                messagebox.showerror('Error', f'{filetype.capitalize()} file {path} not found')
                exit(1)
            except Exception as e:
                logger.error(f'Invalid {filetype} in {path}: {e}')
                messagebox.showerror('Error', f'Invalid {filetype} in {path}: {e}')
                exit(1)

    def _load_config(self, config_file):
        return self._load_file_with_error_handling(config_file, yaml.safe_load, 'config')

    def _load_webhooks(self, json_file):
        import json
        return self._load_file_with_error_handling(json_file, json.load, 'webhook')

    def _load_themes(self, path):
        import json
        try:
            with open(path, 'r') as f:
                pass  # postinserted
        except Exception as e:
                return json.load(f)
                logger.warning(f'Could not load themes from {path}: {e}')
                return {}

    def _set_window_icon(self, icon_path):
        try:
            if sys.platform == 'win32':
                self.root.iconbitmap(icon_path)
            else:  # inserted
                self.root.iconphoto(True, tk.PhotoImage(file=icon_path))
            logger.info(f'Loaded icon: {icon_path}')
        except Exception as e:
            logger.warning(f'Failed to load icon {icon_path}: {e}')
            messagebox.showwarning('Warning', f'Failed to load icon: {e}')

    def _setup_gui(self):
        self.main_frame = ttk.Frame(self.root, padding='10')
        self.main_frame.grid(row=0, column=0, sticky='nsew')
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=0, column=0, columnspan=3, sticky='nsew', pady=5)
        self.control_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.control_tab, text='Control')
        self._setup_control_tab()
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text='Settings')
        self._setup_settings_tab()
        self.info_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.info_tab, text='Info')
        self._setup_info_tab()
        self.log_text = scrolledtext.ScrolledText(self.main_frame, height=10, width=60, state='disabled')
        self.log_text.grid(row=1, column=0, columnspan=3, pady=10, sticky='ew')
        logger.addHandler(TextHandler(self.log_text))
        self.toggle_logs_button = ttk.Button(self.main_frame, text='Hide Logs', command=self._toggle_logs)
        self.toggle_logs_button.grid(row=2, column=0, columnspan=3, pady=2, sticky='ew')
        self.logs_visible = True
        footer_label = ttk.Label(self.main_frame, text='Cracked with ♥ by @rafeedthegay (discord) ')
        footer_label.grid(row=3, column=0, columnspan=3, pady=5, sticky=tk.S)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        theme = self.config.get('theme', 'Default')
        self._apply_theme(theme)

    def _setup_settings_tab(self):
        def add_row(frame, label, var, row, readonly=False):
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky=tk.W, pady=3, padx=5)
            entry = ttk.Entry(frame, textvariable=var, state='readonly' if readonly else 'normal')
            entry.grid(row=row, column=1, sticky='ew', pady=3, padx=5)
        ping_frame = ttk.LabelFrame(self.settings_tab, text='Ping Farm Settings', padding='10')
        ping_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=5, padx=5)
        essentials = [0, 1, 2, 3, 7]
        for idx, (label, varname, _, _) in enumerate(self._settings_fields):
            if idx in essentials:
                readonly = idx in (0, 1, 2)
                add_row(ping_frame, label, getattr(self, varname), idx, readonly=readonly)
        ping_frame.columnconfigure(1, weight=1)
        self.advanced_visible = tk.BooleanVar(value=False)

        def toggle_advanced():
            self.advanced_visible.set(not self.advanced_visible.get())
            if self.advanced_visible.get():
                advanced_frame.grid()
                adv_btn.config(text='Hide Advanced Options')
            else:  # inserted
                advanced_frame.grid_remove()
                adv_btn.config(text='Show Advanced Options')
        self = ttk.Button(self.settings_tab, text='Show Advanced Options', command=toggle_advanced)
        self.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        adv_btn = ttk.LabelFrame(self.settings_tab, text='Advanced Options', padding='10')
        adv_btn.grid(row=2, column=0, columnspan=2, sticky='ew', pady=5, padx=5)
        adv_btn.grid_remove()
        for i, idx in enumerate([4, 5, 6]):
            label, varname, _, _ = self._settings_fields[idx]
            add_row(adv_btn, label, getattr(self, varname), i)
        adv_btn.columnconfigure(1, weight=1)
        pref_frame = ttk.LabelFrame(self.settings_tab, text='Preferences', padding='10')
        pref_frame.grid(row=3, column=0, columnspan=2, sticky='ew', pady=5, padx=5)
        ttk.Label(pref_frame, text='Theme:').grid(row=0, column=0, sticky=tk.W, pady=3, padx=5)
        theme_combo = ttk.Combobox(pref_frame, textvariable=self.theme_var, state='readonly', values=self.theme_options)
        theme_combo.grid(row=0, column=1, sticky='ew', pady=3, padx=5)
        theme_combo.bind('<<ComboboxSelected>>', lambda e: self._on_theme_selected())
        pref_frame.columnconfigure(1, weight=1)
        self.custom_color_vars = {'bg': tk.StringVar(value=self.config.get('custom_theme', {}).get('bg', '#181818')), 'fg': tk.StringVar(value=self.config.get('custom_theme', {}).get('fg', '#f8f8f2')), 'accent': tk.StringVar(value=self.config.get('custom_theme', {}).get('accent', '#6c3483')), 'entry_bg': tk.StringVar(value=self.config.get('custom_theme', {}).get('entry_bg', '#23272e')), 'entry_fg': tk.StringVar(value=self.config.get('custom_theme', {}).get('entry_fg', '#f8f8f2'))}
        self.custom_color_labels = {}
        self.custom_color_entries = {}
        row = 1
        for key, label in zip(['bg', 'fg', 'accent', 'entry_bg', 'entry_fg'], ['Background', 'Foreground', 'Accent', 'Entry Background', 'Entry Foreground']):
            lbl = ttk.Label(pref_frame, text=label + ':')
            ent = ttk.Entry(pref_frame, textvariable=self.custom_color_vars[key], width=10)
            self.custom_color_labels[key] = lbl
            self.custom_color_entries[key] = ent
            lbl.grid(row=row, column=0, sticky=tk.W, pady=2, padx=5)
            ent.grid(row=row, column=1, sticky='ew', pady=2, padx=5)
            ent.bind('<KeyRelease>', lambda e: self._apply_custom_theme(save=True))
            row += 1
        self._show_hide_custom_colors()
        button_frame = ttk.Frame(self.settings_tab)
        button_frame.grid(row=4, column=1, sticky=tk.E, pady=10, padx=5)
        ttk.Button(button_frame, text='Save Config', command=self._save_config).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text='Reset to Default', command=self._reset_config).grid(row=0, column=1, padx=5)
        self.settings_tab.columnconfigure(1, weight=1)

    def _on_theme_selected(self):
        self._show_hide_custom_colors()
        self._apply_theme(self.theme_var.get(), save=True)

    def _show_hide_custom_colors(self):
        show = self.theme_var.get() == 'Custom'
        for key in self.custom_color_labels:
            if show:
                self.custom_color_labels[key].grid()
                self.custom_color_entries[key].grid()
            else:  # inserted
                self.custom_color_labels[key].grid_remove()
                self.custom_color_entries[key].grid_remove()
        if show:
            self._apply_custom_theme(save=False)

    def _apply_theme(self, theme_name, save=False):
        if theme_name == 'Default':
            self._apply_default_theme()
        else:  # inserted
            if theme_name == 'Custom':
                self._apply_custom_theme(save=save)
            else:  # inserted
                if theme_name in self.themes:
                    self._apply_json_theme(theme_name)
                else:  # inserted
                    self._apply_default_theme()
        if save:
            self.config['theme'] = theme_name
        self._refresh_theme_widgets()

    def _apply_json_theme(self, theme_name):
        style = ttk.Style()
        style.theme_use('clam')
        t = self.themes[theme_name]
        bg = t['bg']
        fg = t['fg']
        accent = t['accent']
        entry_bg = t['entry_bg']
        entry_fg = t['entry_fg']
        button_bg = t.get('button_bg', entry_bg)
        button_fg = t.get('button_fg', entry_fg)
        style.configure('.', background=bg, foreground=fg)
        style.configure('TFrame', background=bg)
        style.configure('TLabel', background=bg, foreground=fg)
        style.configure('TButton', background=button_bg, foreground=button_fg, borderwidth=1, focusthickness=2, focuscolor=accent)
        style.map('TButton', background=[('active', button_bg), ('pressed', accent), ('!active', button_bg)], foreground=[('active', button_fg), ('pressed', button_fg), ('!active', button_fg)])
        style.configure('TCheckbutton', background=bg, foreground=fg, indicatorcolor=accent, indicatordiameter=12, bordercolor=accent, focuscolor=accent)
        style.map('TCheckbutton', background=[('active', bg), ('selected', bg), ('!active', bg)], foreground=[('active', fg), ('selected', fg), ('!active', fg)])
        style.configure('TNotebook', background=bg)
        style.configure('TNotebook.Tab', background=button_bg, foreground=button_fg, lightcolor=accent, borderwidth=0)
        style.map('TNotebook.Tab', background=[('selected', accent), ('active', button_bg), ('!selected', button_bg)], foreground=[('selected', fg), ('active', fg), ('!selected', button_fg)])
        style.configure('TEntry', fieldbackground=entry_bg, foreground=entry_fg, background=entry_bg, bordercolor=accent, lightcolor=accent, darkcolor=bg, highlightcolor=accent, selectbackground=accent, selectforeground=button_fg)
        style.map('TEntry', fieldbackground=[('readonly', entry_bg), ('!readonly', entry_bg), ('active', entry_bg)], background=[('readonly', entry_bg), ('!readonly', entry_bg), ('active', entry_bg)], foreground=[('readonly', entry_fg), ('!readonly', entry_fg), ('active', entry_fg)], bordercolor=[('focus', accent), ('!focus', accent)], highlightcolor=[('focus', accent), ('!focus', accent)])
        style.configure('TCombobox', fieldbackground=entry_bg, foreground=entry_fg, background=entry_bg, selectbackground=entry_bg, selectforeground=entry_fg, bordercolor=accent, lightcolor=accent, darkcolor=bg, highlightcolor=accent)
        style.map('TCombobox', fieldbackground=[('readonly', entry_bg), ('!readonly', entry_bg), ('active', entry_bg)], background=[('readonly', entry_bg), ('!readonly', entry_bg), ('active', entry_bg)], foreground=[('readonly', entry_fg), ('!readonly', entry_fg), ('active', entry_fg)], bordercolor=[('focus', accent), ('!focus', accent)], highlightcolor=[('focus', accent), ('!focus', accent)])
        style.configure('Horizontal.TProgressbar', background=accent, troughcolor=bg)
        self.root.option_add('*TCombobox*Listbox.background', entry_bg)
        self.root.option_add('*TCombobox*Listbox.foreground', entry_fg)
        self.root.option_add('*Entry.background', entry_bg)
        self.root.option_add('*Entry.foreground', entry_fg)
        self.root.option_add('*Entry.highlightBackground', accent)
        self.root.option_add('*Entry.highlightColor', accent)
        self.root.option_add('*Text.background', entry_bg)
        self.root.option_add('*Text.foreground', entry_fg)
        self.root.option_add('*foreground', fg)
        self.root.option_add('*background', bg)
        if hasattr(self, 'log_text'):
            self.log_text.config(bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)

    def _apply_default_theme(self):
        style = ttk.Style()
        style.theme_use('default')
        self.root.option_clear()
        if hasattr(self, 'log_text'):
            self.log_text.config(bg='white', fg='black', insertbackground='black')

    def _apply_custom_theme(self, save=False):
        style = ttk.Style()
        style.theme_use('clam')
        bg = self.custom_color_vars['bg'].get()
        fg = self.custom_color_vars['fg'].get()
        accent = self.custom_color_vars['accent'].get()
        entry_bg = self.custom_color_vars['entry_bg'].get()
        entry_fg = self.custom_color_vars['entry_fg'].get()
        button_bg = entry_bg
        button_fg = entry_fg
        style.configure('.', background=bg, foreground=fg)
        style.configure('TFrame', background=bg)
        style.configure('TLabel', background=bg, foreground=fg)
        style.configure('TButton', background=button_bg, foreground=button_fg, borderwidth=1, focusthickness=2, focuscolor=accent)
        style.map('TButton', background=[('active', button_bg), ('pressed', accent), ('!active', button_bg)], foreground=[('active', button_fg), ('pressed', button_fg), ('!active', button_fg)])
        style.configure('TCheckbutton', background=bg, foreground=fg, indicatorcolor=accent, indicatordiameter=12, bordercolor=accent, focuscolor=accent)
        style.map('TCheckbutton', background=[('active', bg), ('selected', bg), ('!active', bg)], foreground=[('active', fg), ('selected', fg), ('!active', fg)])
        style.configure('TNotebook', background=bg)
        style.configure('TNotebook.Tab', background=button_bg, foreground=button_fg, lightcolor=accent, borderwidth=0)
        style.map('TNotebook.Tab', background=[('selected', accent), ('active', button_bg), ('!selected', button_bg)], foreground=[('selected', fg), ('active', fg), ('!selected', button_fg)])
        style.configure('TEntry', fieldbackground=entry_bg, foreground=entry_fg, background=entry_bg, bordercolor=accent, lightcolor=accent, darkcolor=bg, highlightcolor=accent, selectbackground=accent, selectforeground=button_fg)
        style.map('TEntry', fieldbackground=[('readonly', entry_bg), ('!readonly', entry_bg), ('active', entry_bg)], background=[('readonly', entry_bg), ('!readonly', entry_bg), ('active', entry_bg)], foreground=[('readonly', entry_fg), ('!readonly', entry_fg), ('active', entry_fg)], bordercolor=[('focus', accent), ('!focus', accent)], highlightcolor=[('focus', accent), ('!focus', accent)])
        style.configure('TCombobox', fieldbackground=entry_bg, foreground=entry_fg, background=entry_bg, selectbackground=entry_bg, selectforeground=entry_fg, bordercolor=accent, lightcolor=accent, darkcolor=bg, highlightcolor=accent)
        style.map('TCombobox', fieldbackground=[('readonly', entry_bg), ('!readonly', entry_bg), ('active', entry_bg)], background=[('readonly', entry_bg), ('!readonly', entry_bg), ('active', entry_bg)], foreground=[('readonly', entry_fg), ('!readonly', entry_fg), ('active', entry_fg)], bordercolor=[('focus', accent), ('!focus', accent)], highlightcolor=[('focus', accent), ('!focus', accent)])
        style.configure('Horizontal.TProgressbar', background=accent, troughcolor=bg)
        self.root.option_add('*TCombobox*Listbox.background', entry_bg)
        self.root.option_add('*TCombobox*Listbox.foreground', entry_fg)
        self.root.option_add('*Entry.background', entry_bg)
        self.root.option_add('*Entry.foreground', entry_fg)
        self.root.option_add('*Entry.highlightBackground', accent)
        self.root.option_add('*Entry.highlightColor', accent)
        self.root.option_add('*Text.background', entry_bg)
        self.root.option_add('*Text.foreground', entry_fg)
        self.root.option_add('*foreground', fg)
        self.root.option_add('*background', bg)
        if hasattr(self, 'log_text'):
            self.log_text.config(bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
        if save:
            self.config['custom_theme'] = {k: v.get() for k, v in self.custom_color_vars.items()}

    def _setup_control_tab(self):
        ttk.Label(self.control_tab, text='Mode:').grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.mode_display_map = {'Parallel': 'parallel', 'Sequential': 'sequential'}
        self.mode_reverse_map = {v: k for k, v in self.mode_display_map.items()}
        self = ttk.Combobox(self.control_tab, textvariable=tk.StringVar(value=self.mode_reverse_map[self.mode.get()]), state='readonly', values=list(self.mode_display_map.keys()))
        self.grid(row=0, column=1, sticky='ew', pady=5, padx=5)

        def on_mode_selected(event):
            selected_display = mode_combo.get()
            self.mode.set(self.mode_display_map[selected_display])
            self._update_shard_ui()
        self.bind('<<ComboboxSelected>>', on_mode_selected)
        self.set(self.mode_reverse_map[self.mode.get()])
        self.mode_combo = self
        self.shard_frame = ttk.LabelFrame(self.control_tab, text='Shards', padding='5')
        self.shard_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=5, padx=5)
        self.switch_status_var = tk.StringVar(value='Sequential Mode: Idle')
        self.switch_status_label = ttk.Label(self.control_tab, textvariable=self.switch_status_var)
        self.switch_status_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5, padx=5)
        self.start_button = ttk.Button(self.control_tab, text='Start', command=self._start_action)
        self.start_button.grid(row=3, column=0, pady=10, padx=5)
        self.stop_button = ttk.Button(self.control_tab, text='Kill', command=self._kill_action, state='disabled')
        self.stop_button.grid(row=3, column=1, pady=10, padx=5)
        self._update_shard_ui()
        self.control_tab.columnconfigure(1, weight=1)

    def _set_start_stop_state(self, start_enabled: bool, stop_enabled: bool):
        self.start_button.config(state='normal' if start_enabled else 'disabled')
        self.stop_button.config(state='normal' if stop_enabled else 'disabled')

    def _update_shard_ui(self):
        for widget in self.shard_frame.winfo_children():
            widget.destroy()
        if self.mode.get() == 'parallel':
            self.shard_states = {shard: tk.BooleanVar(value=False) for shard in self.webhook_groups}
            self.shard_checkbuttons = {}
            for row, (shard, var) in enumerate(self.shard_states.items()):
                cb = ttk.Checkbutton(self.shard_frame, text=shard, variable=var)
                cb.grid(row=row, column=0, sticky=tk.W, pady=2, padx=5)
                self.shard_checkbuttons[shard] = cb
            self.switch_status_label.grid_remove()
            self.switch_shard_combo = None
        else:  # inserted
            ttk.Label(self.shard_frame, text='Starting Shard:').grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
            self.switch_shard_var = tk.StringVar()
            combo = ttk.Combobox(self.shard_frame, textvariable=self.switch_shard_var, state='readonly')
            combo['values'] = list(self.webhook_groups.keys())
            combo.grid(row=0, column=1, sticky='ew', pady=5, padx=5)
            if combo['values']:
                combo.current(0)
            self.switch_status_label.grid()
            self.switch_shard_combo = combo

    def _save_config(self):
        try:
            for _, varname, _, key in self._settings_fields:
                self.config[key] = getattr(self, varname).get()
            self.config['theme'] = self.theme_var.get()
            if self.theme_var.get() == 'Custom':
                self.config['custom_theme'] = {k: v.get() for k, v in self.custom_color_vars.items()}
        except Exception as e:
            with open(self.config_file, 'w') as file:
                yaml.safe_dump(self.config, file)
                    messagebox.showinfo('Success', 'Configuration saved successfully')
                    self.rate_limit_backoff = getattr(self, 'backoff_var').get()
                logger.error(f'Failed to save config: {e}')
                messagebox.showerror('Error', f'Failed to save config: {e}')

    def _send_webhook(self, webhook_url: str, message: str, username: str, avatar_url: str, shard_name: str) -> bool:
        payload = {'content': message, 'username': username, 'avatar_url': avatar_url}
        headers = {'Content-Type': 'application/json'}
        for attempt in range(self.max_retries):
            try:
                import requests
                response = requests.post(webhook_url, json=payload, headers=headers)
                if response.status_code == 204:
                    self.message_counts[webhook_url] = self.message_counts.get(webhook_url, 0) + 1
                    logger.info(f'Sent message (Count: {self.message_counts[webhook_url]})')
                    if self.mode.get() == 'sequential' and shard_name == self.current_switch_shard:
                        self._update_switch_status()
            except Exception as e:
                else:  # inserted
                    return True
                if response.status_code == 429:
                    retry_after = response.json().get('retry_after', self.rate_limit_backoff) / 1000
                    logger.warning(f'Rate limited on {webhook_url}. Waiting {retry_after}s')
                    import time
                    time.sleep(retry_after)
                else:  # inserted
                    logger.error(f'Failed to send to {webhook_url}. Status: {response.status_code}, Response: {response.text}')
                else:  # inserted
                    return False
        else:  # inserted
            logger.error(f'Max retries reached for {webhook_url}')
            return False
            logger.error(f'Error sending to {webhook_url}: {e}')
            if attempt < self.max_retries - 1:
                import time
                time.sleep(self.rate_limit_backoff)

    def _webhook_loop(self, webhook_url: str, message: str, username: str, avatar_url: str, delay: float, shard_name: str):
        import time
        while self.shard_status.get(shard_name, False) and self.message_counts.get(webhook_url, 0) < self.message_limit:
            self._send_webhook(webhook_url, message, username, avatar_url, shard_name)
            time.sleep(delay)

    def _start_shard(self, shard_name: str):
        self.shard_status[shard_name] = True
        self.threads[shard_name] = []
        webhook_urls = self.webhook_groups[shard_name]
        message = getattr(self, 'message_var').get()
        username = getattr(self, 'username_var').get()
        avatar_url = getattr(self, 'avatar_var').get()
        delay = getattr(self, 'delay_var').get()
        for webhook_url in webhook_urls:
            self.message_counts[webhook_url] = self.message_counts.get(webhook_url, 0)
            import threading
            thread = threading.Thread(target=self._webhook_loop, args=(webhook_url, message, username, avatar_url, delay, shard_name), daemon=False)
            self.threads[shard_name].append(thread)
            thread.start()
        logger.info(f'Started shard: {shard_name}')

    def _stop_shard(self, shard_name: str):
        if not self.shard_status.get(shard_name, False):
            return
        self.shard_status[shard_name] = False
        threads = self.threads.get(shard_name, [])
        for thread in threads:
            if thread.is_alive():
                thread.join(timeout=5)
        self.threads[shard_name] = []
        logger.info(f'Stopped shard: {shard_name}')

    def _start_action(self):
        if self.mode.get() == 'parallel':
            self._start_parallel_mode()
        else:  # inserted
            self._start_sequential_mode()

    def _start_parallel_mode(self):
        selected_shards = [shard for shard, var in self.shard_states.items() if var.get()]
        if not selected_shards:
            messagebox.showerror('Error', 'Select at least one shard')
            return
        if any((self.shard_status.get(shard, False) for shard in selected_shards)):
            messagebox.showwarning('Warning', 'One or more selected shards are already running')
            return
        for shard in selected_shards:
            self._start_shard(shard)
        self._set_start_stop_state(False, True)
        self._set_shard_checkboxes_state(False)

    def _start_sequential_mode(self):
        if any(self.shard_status.values()):
            messagebox.showwarning('Warning', 'A shard is already running')
            return
        shard_name = self.switch_shard_var.get()
        if not shard_name:
            messagebox.showerror('Error', 'Select a starting shard')
            return
        self.current_switch_shard = shard_name
        self._start_shard(shard_name)
        import threading
        threading.Thread(target=self._monitor_sequential_mode, daemon=True).start()
        self._set_start_stop_state(False, True)
        self._set_switch_combo_state(False)

    def _monitor_sequential_mode(self):
        import time
        shard_names = list(self.webhook_groups.keys())
        while self.shard_status.get(self.current_switch_shard, False):
            webhook_urls = self.webhook_groups[self.current_switch_shard]
            total_messages = sum((self.message_counts.get(url, 0) for url in webhook_urls))
            if total_messages >= self.total_pings:
                if self.current_switch_shard is not None:
                    self._stop_shard(self.current_switch_shard)
                current_idx = shard_names.index(self.current_switch_shard)
                next_idx = (current_idx + 1) % len(shard_names)
                self.current_switch_shard = shard_names[next_idx]
                self._start_shard(self.current_switch_shard)
                logger.info(f'Switched to shard: {self.current_switch_shard}')
            time.sleep(5)

    def _update_switch_status(self):
        if self.current_switch_shard:
            webhook_urls = self.webhook_groups[self.current_switch_shard]
            total_messages = sum((self.message_counts.get(url, 0) for url in webhook_urls))
            self.switch_status_var.set(f'Sequential Mode: {self.current_switch_shard} ({total_messages}/{self.total_pings} pings)')

    def _stop_action(self):
        if self.mode.get() == 'parallel':
            self._stop_parallel_mode()
        else:  # inserted
            self._stop_sequential_mode()

    def _stop_parallel_mode(self):
        selected_shards = [shard for shard, var in self.shard_states.items() if var.get()]
        if not any((self.shard_status.get(shard, False) for shard in selected_shards)):
            messagebox.showwarning('Warning', 'No selected shards are running')
            return
        for shard in selected_shards:
            self._stop_shard(shard)
        if not any(self.shard_status.values()):
            self._set_start_stop_state(True, False)
            self._set_shard_checkboxes_state(True)
        else:  # inserted
            return None

    def _stop_sequential_mode(self):
        if not self.shard_status.get(self.current_switch_shard, False):
            messagebox.showwarning('Warning', 'No shard is running')
            return
        if self.current_switch_shard is not None:
            self._stop_shard(self.current_switch_shard)
        self.current_switch_shard = None
        self.switch_status_var.set('Sequential Mode: Idle')
        self._set_start_stop_state(True, False)
        self._set_switch_combo_state(True)

    def _set_shard_checkboxes_state(self, enabled: bool):
        if hasattr(self, 'shard_checkbuttons'):
            state = 'normal' if enabled else 'disabled'
            for cb in self.shard_checkbuttons.values():
                cb.config(state=state)

    def _set_switch_combo_state(self, enabled: bool):
        if hasattr(self, 'switch_shard_combo') and self.switch_shard_combo is not None:
            state = 'readonly' if enabled else 'disabled'
            self.switch_shard_combo.config(state=state)

    def _kill_action(self):
        try:
            self.root.destroy()
        except Exception:
            pass  # postinserted
        else:  # inserted
            os._exit(0)
            pass
        else:  # inserted
            pass

    def _toggle_logs(self):
        if self.logs_visible:
            self.log_text.grid_remove()
            self.toggle_logs_button.config(text='Show Logs')
            self.logs_visible = False
        else:  # inserted
            self.log_text.grid()
            self.toggle_logs_button.config(text='Hide Logs')
            self.logs_visible = True

    def _refresh_theme_widgets(self):
        self.root.update_idletasks()
        if hasattr(self, 'log_text'):
            theme = self.theme_var.get() if hasattr(self, 'theme_var') else self.config.get('theme', 'Default')
            if theme == 'Default':
                self.log_text.config(bg='white', fg='black', insertbackground='black')
            else:  # inserted
                if theme == 'Custom':
                    c = self.config.get('custom_theme', {})
                    self.log_text.config(bg=c.get('entry_bg', '#23272e'), fg=c.get('entry_fg', '#f8f8f2'), insertbackground=c.get('entry_fg', '#f8f8f2'))
                else:  # inserted
                    if theme in self.themes:
                        t = self.themes[theme]
                        self.log_text.config(bg=t['entry_bg'], fg=t['entry_fg'], insertbackground=t['entry_fg'])
                    else:  # inserted
                        self.log_text.config(bg='white', fg='black', insertbackground='black')

    def _reset_config(self):
        for _, varname, _, key in self._settings_fields:
            getattr(self, varname).set(self.DEFAULT_CONFIG[key])
        self.theme_var.set('Default')
        self._apply_theme('Default', save=True)
        messagebox.showinfo('Success', 'Configuration reset to default values')

    def _setup_info_tab(self):
        for widget in self.info_tab.winfo_children():
            widget.destroy()
        banner = ttk.Frame(self.info_tab)
        banner.grid(row=0, column=0, sticky='ew', padx=0, pady=(0, 10))
        banner.columnconfigure(0, weight=1)
        title_label = ttk.Label(banner, text='Oblivion V1 - Free Edition', font=('Segoe UI', 20, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, sticky='ew', pady=0)
        subtitle = ttk.Label(banner, text='@everyone pings for everyone!', font=('Segoe UI', 14, 'italic'))
        subtitle.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 5))
        info = ttk.Label(self.info_tab, text='This tool is for sending messages to Discord webhooks in bulk. Because this is the free version some customization is limited. The use of this tool might break Discord\'s Terms of Service, so use it at your own risk.', font=('Segoe UI', 11), wraplength=520, justify='left')
        info.grid(row=1, column=0, sticky='w', padx=10, pady=5)
        dev = ttk.Label(self.info_tab, text='Developer: @Sewaeth (but cracked by rafeed)', font=('Segoe UI', 10, 'italic'))
        dev.grid(row=2, column=0, sticky='w', padx=10, pady=(0, 2))

        def open_discord():
            import webbrowser
            webbrowser.open_new('https://fbi.pet')
        discord_btn = ttk.Button(self.info_tab, text='Join Official Website', command=open_discord)
        discord_btn.grid(row=3, column=0, sticky='w', padx=10, pady=(0, 8))
        tos = ttk.Label(self.info_tab, text='Reminder: Do not use this tool to raid discord servers. You are responsible for your actions.', font=('Segoe UI', 10, 'bold'), foreground='#a94442', wraplength=520, justify='left')
        tos.grid(row=4, column=0, sticky='w', padx=10, pady=(0, 2))

class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.see(tk.END)
        self.text_widget.configure(state='disabled')
if __name__ == '__main__':
    root = tk.Tk()
    app = OblivionGUI(root, 'config.yaml')
    root.mainloop()
