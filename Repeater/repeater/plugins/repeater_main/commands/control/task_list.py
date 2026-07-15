from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)

@CommandCaller.register
class TaskList(CommandPackage):
    cmd = "taskList"
    aliases = {
        "tl",
        "TL",
        "task_list",
        "TaskList",
        "Tast_List",
        "TASK_LIST",
    }
    cmd_type = CmdTypes.CONTROL
    documents = f"""
    Show all tasks.

    Usage: 
        /{cmd}
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        task_list = CommandCaller.get_user_runnings(persona_info.namespace)
        if task_list:
            text_buffer: list[str] = []
            for task in task_list:
                text_buffer.append(f"[{task.task_id}] - {task.package.component}")
            await send_msg.send_check_length_prompt("\n".join(text_buffer))
        else:
            await send_msg.send_error("No running tasks.")