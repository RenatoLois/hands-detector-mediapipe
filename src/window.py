import glfw


class Window:
    @classmethod
    def initialize_glfw(cls) -> None:
        if not glfw.init():
            raise RuntimeError("failed to initialize glfw")

    def __init__(self,
                 window_name: str,
                 width: int,
                 height: int,
                 visible: bool = False) -> None:
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        if visible:
            glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

        self.window = glfw.create_window(width,
                                         height,
                                         window_name,
                                         None,
                                         None)
        glfw.make_context_current(self.window)

    def visible(self, boolean_value):
        if boolean_value:
            glfw.show_window(self.window)
        else:
            glfw.hide_window(self.window)

    def swap_buffers(self):
        glfw.swap_buffers(self.window)

    def poll_events(self):
        glfw.poll_events()
