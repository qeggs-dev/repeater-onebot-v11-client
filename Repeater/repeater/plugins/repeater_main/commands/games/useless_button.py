import random
from ...assist import PersonaInfo, SendMsg
from ...command_register import(
    CommandCaller,
    CommandPackage,
    CmdType
)
from ...client_net_configs import storage_configs

@CommandCaller.register
class UselessButton(CommandPackage):
    cmd = "uselessButton"
    aliases = {
        "ub",
        "UB",
        "useless_button",
        "Useless_Button",
        "UselessButton",
        "USELESS_BUTTON"
    }
    cmd_type = CmdType.GAMES

    @staticmethod
    def button():
        button_hit = (random.randint(0, 50) == 25)
        if button_hit:
            word = random.choice(storage_configs.useless_button_words)
            return word
        else:
            return storage_configs.useless_button_missing
    
    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        msg = persona_info.message_striped_str
        try:
            times = int(msg)
        except ValueError:
            times = 1
        
        if times == 1:
            results = [self.button()]
        elif times > 1:
            results = [f"{i}. {self.button()}" for i in range(1, times + 1)]
        else:
            results = ["The number of times cannot be less than 1."]

        await send_msg.send_check_length("\n".join(results))