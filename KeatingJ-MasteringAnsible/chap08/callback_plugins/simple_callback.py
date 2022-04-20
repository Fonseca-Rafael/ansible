from ansible.plugins.callback import CallbackBase

class CallbackModule(CallbackBase):
    def on_any(self, *args, **kwargs):
        msg = '...something from callback plugin... '
        self._display.display(msg * 3)
