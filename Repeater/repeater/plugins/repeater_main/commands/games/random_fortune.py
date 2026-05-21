import random
import hashlib
from datetime import datetime
from ...assist import PersonaInfo, SendMsg, Namespace
from ...command_register import(
    CommandCaller,
    CommandPackage,
    CmdType
)

@CommandCaller.register
class RandomFortune(CommandPackage):
    cmd = "randomFortune"
    aliases = {
        "rf",
        "RF",
        "random_fortune",
        "Random_Fortune",
        "RandomFortune",
        "RANDOM_FORTUNE"
    }
    cmd_type = CmdType.GAMES
    documents = f"""
        Randomly generate daily fortunes.

        Usage:
          /{cmd} [@someone]
    """

    @staticmethod
    def daily_seed(time: datetime) -> int:
        return time.year ^ time.month ^ time.day
    
    def see_fortune(self, namespace: Namespace):
        now = datetime.now()
        hash_value = hashlib.pbkdf2_hmac(
            "sha256",
            str(namespace.user_id).encode("utf-8"),
            str(self.daily_seed(now)).encode("utf-8"),
            10 ** 5
        )
        seed = int.from_bytes(hash_value, "big")
        rand = random.Random(seed)
        fortunes: dict[str, float] = {
            "Money": rand.random(),
            "Love": rand.random(),
            "Work": rand.random(),
            "Health": rand.random(),
            "Social": rand.random(),
            "Study": rand.random(),
            "Travel": rand.random(),
        }
        total = sum(fortunes.values()) / len(fortunes)
        text_buffer = [f"{key} Fortune: {value:.2%}" for key, value in fortunes.items()]
        return f"Total Fortune: {total:.2%}\n" + "\n".join(text_buffer)
        
    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        at_list = persona_info.noself_at_list
        if not at_list:
            namespace = persona_info.namespace
        elif len(at_list) > 1:
            await send_msg.send_error("Too many people at once.")
        else:
            namespace = persona_info.namespace_from_this_group(at_list[0])
        
        fortune_text = self.see_fortune(namespace)
        await send_msg.send_prompt(fortune_text)