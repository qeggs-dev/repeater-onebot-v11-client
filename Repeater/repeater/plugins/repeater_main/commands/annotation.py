from ..command_register import(
    CommandCaller,
    CommandPackage,
    CmdTypes
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
    cmd_type = CmdTypes.RESERVED
    empty_handler = True

    async def handler(self, persona_info, send_msg):
        pass