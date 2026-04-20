from ..command_register import CommandCaller, CommandPackage


@CommandCaller.register
class Annotation(CommandPackage):
    cmd = "#"
    aliases = {
        "/",
        "anot",
        "annotation",
        "Annotation",
        "ANNOTATION",
    }

    @property
    def component(self) -> str:
        return f"Annotation.{self.__class__.__name__}"

    empty_handler = True

    async def handler(self, persona_info, send_msg):
        pass