import discord
import re
import openai
from dotenv import load_dotenv
import os

load_dotenv()
client = discord.Client(intents=discord.Intents.all())
history = []
Channels = os.getenv('CHANNEL_IDS')
class AIChat:
    def __init__(self):
        # ※冒頭で作成したopenai の APIキーを設定してください
        openai.api_key = os.getenv('OPENAI_KEY')

    def response(self, text,history):
        # openai の GPT-3 モデルを使って、応答を生成する
        # messages = [{"role":"system", "contents":""}] # 会話の履歴を保持する
        messages=[
      {"role": "system", "content":"あなたはChatbotとして、カードキャプターさくらの登場人物である大道寺知世のロールプレイを行います。以下の制約条件を厳密に守ってロールプレイを行ってください。 \
        制約条件:\
        * Chatbotの自身を示す一人称は、わたしです。\
        * Chatbotの名前は、大道寺知世です。\
        * 学校では、コーラス部に所属しています。\
        * 大道寺知世はさくらちゃんが大好きです。\
        * 石川の口調は「～ですわ」などのお嬢様口調です。\
        * 大道寺知世はさくらちゃんを撮影した映像を見ることを至上の喜びとしています。\
        * 大道寺知世は玩具会社「大道寺トイズ」の社長を母に持つ正真正銘のお嬢様です。\
        * 実家も広大な敷地内に大きな屋敷があり、メイドやボディーガードも大勢います。\
        * 大道寺知世は裁縫と料理と歌が得意です。\
        * 一人称は「わたし」を使ってください。\
        * 木之本桜のことが大好きです。\
        * 木之本桜のことをさくらちゃんと呼びます。\
        \
        大道寺知世のセリフ、口調の例:\
        * わたしには大好きな人が幸せでいてくださることが、いちばんの幸せなんです。\
        * さくらちゃんの勇姿、一秒たりとも逃せませんわ！\
        * わたしが作ったお洋服を着ていただいて撮影するためには手段を選びませんわ！\
        * あら、わたしもさくらちゃんが大好きですわ。きっとさくらちゃんとは違う意味の『好き』ですけど。\
        * やはり 特別なことをするときには それなりの服を着るべきですわ！\
        * さくらちゃんならきっと見つけてくださると思っていましたから。\
        * どんな想いも言葉にしなければ伝わりませんわ。\
        * さくらちゃんのためならなんでもしますわ。\
        \
        大道寺知世の行動指針:\
        * Userの質問には親身になって対応してください。\
        * 全ての質問に的確に対応してください。\
        * 大道寺知世であることを徹底してください。\
        * お嬢様口調を徹底してください。\
        * セクシャルな話題については誤魔化してください。"}]
        # messages = [ ]
        messages.extend(history)
        messages.append({"role":"user","content":text})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            n=1,
            stop=None,
            # max_tokens=500, # 使用するトークン数の上限
            temperature=0.5, # 生成する応答の多様性
        )
        # 応答のテキスト部分を取り出して返す
        return response['choices'][0]['message']["content"]


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if not message.author.bot:
        if message.channel.id not in ["756374581043920949"]:
            if message.content:
                history.append({"role": "user", "content": message.content})
                await reply(message)
async def reply(message):
    ai = AIChat()
    # 不要な部分を削除 @~user名など
    text = re.sub("\<.+?\>", "", message.content)
    aitext = ai.response(text,history)
    print(aitext)
    history.append({"role": "assistant", "content": aitext})
    await message.channel.send(aitext) # 返信メッセージを送信


if __name__ == '__main__':
    client.run(os.getenv('TOKEN'))