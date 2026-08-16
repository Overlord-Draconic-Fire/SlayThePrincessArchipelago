init -1500 python:
    import hashlib

    def __newest_slot():
        return renpy.newest_slot(r'\d+')

    def __slotname(name, page=None, slot=False):
        if slot:
            return name

        if page is None:
            page = persistent._file_page

        try:
            page = int(page)
            page = page + persistent._file_folder * config.file_pages_per_folder
        except ValueError:
            pass

        if config.linear_saves_page_size is not None:
            try:
                page = int(page)
                name = int(name)
                return str((page - 1) * config.linear_saves_page_size + name)
            except ValueError:
                pass

        return str(page) + "-" + str(name) + "-" + hashlib.sha256(archipelago.slot_key.encode("utf-8")).hexdigest()

    def FileActionArchipelago(name, page=None, **kwargs):
        if renpy.current_screen().screen_name[0] == "load":
            return FileLoadArchipelago(name, page=page, **kwargs)
        else:
            return FileSaveArchipelago(name, page=page, **kwargs)

    def FileScreenshotArchipelago(name, empty=None, page=None, slot=False):
        screenshot = renpy.slot_screenshot(__slotname(name, page, slot=slot))
        if screenshot is not None:
            return screenshot

        if empty is not None:
            return empty
        else:
            return Null(config.thumbnail_width, config.thumbnail_height)

    def FileTimeArchipelago(name, format=_("%b %d, %H:%M"), empty="", page=None, slot=False):
        mtime = renpy.slot_mtime(__slotname(name, page, slot))
        if mtime is None:
            return empty

        import time

        format = renpy.translation.translate_string(format)
        return _strftime(format, time.localtime(mtime))

    def FileSaveNameArchipelago(name, empty="", page=None, slot=False):
        return FileJson(name, "_save_name", empty=empty, missing=empty, page=page, slot=slot)

    class FileSaveArchipelago(Action, DictEquality):
        alt = "Save slot [text]"
        slot = None

        def __init__(self, name, confirm=True, newest=True, page=None, cycle=False, slot=False):
            if name is None:
                name = __unused_slot_name(page)

            self.name = name
            self.confirm = confirm
            self.page = page
            self.cycle = cycle
            self.slot = slot

            try:
                self.alt = __("Save slot %s: [text]") % (name,)
            except Exception:
                self.alt = "Save slot %s: [text]" % (name,)

        def __call__(self):
            if not self.get_sensitive():
                return
            
            fn = __slotname(self.name, self.page, self.slot)

            if renpy.scan_saved_game(fn):
                if self.confirm:
                    layout.yesno_screen(layout.OVERWRITE_SAVE, FileSaveArchipelago(self.name, False, False, self.page, cycle=self.cycle, slot=self.slot))
                    return
            
            if self.cycle:
                renpy.renpy.loadsave.cycle_saves(self.page + "-", config.quicksave_slots)

            renpy.save(fn, extra_info=save_name)

            renpy.restart_interaction()

        def get_sensitive(self):
            if _in_replay:
                return False
            elif main_menu:
                return False
            elif (self.page or persistent._file_page) == "auto":
                return False
            else:
                return True

        def get_selected(self):
            if not self.confirm:
                return False

            return __newest_slot() == __slotname(self.name, self.page, self.slot)

    class FileLoadArchipelago(Action, DictEquality):
        alt = "Load slot [text]"
        slot = None

        def __init__(self, name, confirm=True, page=None, newest=True, cycle=False, slot=False):
            if name is None:
                name = __unused_slot_name(page)

            self.name = name
            self.confirm = confirm
            self.page = page
            self.newest = newest
            self.slot = slot

            try:
                self.alt = __("Load slot %s: [text]") % (name,)
            except Exception:
                self.alt = "Load slot %s: [text]" % (name,)

        def __call__(self):
            if not self.get_sensitive():
                return

            fn = __slotname(self.name, self.page, self.slot)

            if not main_menu:
                if self.confirm:
                    if config.autosave_on_quit and not fn.startswith("auto-"):
                        renpy.loadsave.force_autosave()
                    layout.yesno_screen(layout.LOADING, FileLoadArchipelago(self.name, False, self.page, slot=self.slot))
                    return

            renpy.load(fn)

        def get_sensitive(self):
            if _in_replay:
                return False

            return renpy.can_load(__slotname(self.name, self.page, self.slot))

        def get_selected(self):
            if not self.confirm or not self.newest:
                return False

            return __newest_slot() == __slotname(self.name, self.page, self.slot)

    class FilePagePrevious(Action, DictEquality):
        alt = _("Previous file page.")

        def __init__(self, max=None, wrap=False, auto=True, quick=True):
            page = persistent._file_page
            if page == "1":
                page = None
            else:
                page = str(int(page) - 1)

            self.page = page

        def __call__(self):
            if not self.get_sensitive():
                return

            persistent._file_page = self.page
            renpy.restart_interaction()

        def get_sensitive(self):
            return self.page

        def predict(self):
            _predict_file_page(self.page)

    class FilePageNext(Action, DictEquality):
        alt = _("Next file page.")

        def __init__(self, max=None, wrap=False, auto=True, quick=True):
            page = persistent._file_page
            page = int(page) + 1
            if max is not None and page > max:
                page = None

            if page is not None:
                page = str(page)
            
            self.page = page

        def __call__(self):
            if not self.get_sensitive():
                return

            persistent._file_page = self.page
            renpy.restart_interaction()

        def get_sensitive(self):
            return self.page is not None

        def predict(self):
            _predict_file_page(self.page)
