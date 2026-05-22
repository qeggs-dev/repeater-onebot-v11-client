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
          /{cmd} [@someone]...
    """

    @staticmethod
    def daily_seed(time: datetime) -> int:
        return time.year ^ time.month ^ time.day
    
    def see_fortune(self, user_ids: list[str]):
        now = datetime.now()
        hash_value = hashlib.pbkdf2_hmac(
            "sha256",
            ("\n".join(user_ids)).encode("utf-8"),
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
        average = sum(fortunes.values()) / len(fortunes)
        text_buffer = [f"{key} Fortune: {value:.2%}" for key, value in fortunes.items()]
        extreme_luck_factor = ((average-0.5)**2) / 0.25
        return (
            f"Extreme Luck Factor: {extreme_luck_factor:.2%}\n"
            f"Average Fortune: {average:.2%}\n" +
            "\n".join(text_buffer)
        )
        
    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        at_list = persona_info.noself_at_list
        user_ids = [str(persona_info.user_id)] + at_list
        
        fortune_text = self.see_fortune(user_ids)
        await send_msg.send_prompt(fortune_text)