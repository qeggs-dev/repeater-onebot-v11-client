from ..command_register import(
    CommandCaller,
    CommandPackage,
    CmdType
)

@CommandCaller.register
class Annotation(CommandPackage):
    cmd = "#"
    aliases = {
        "/",
        "anot",
        "ANOT",
        "annotation",
        "Annotation",
        "ANNOTATION",
    }
    type = CmdType.RESERVED
    empty_handler = True

    async def handler(self, persona_info, send_msg):
        pass