# RTの基本データ。

from typing import Optional

from discord.ext import commands


class Colors:
    normal = 0x0066ff
    unknown = 0x80989b
    error = 0xeb6ea5
    player = 0x2ca9e1
    queue = 0x007bbb


data = {
    "prefixes": {
        "test": [
            "r2!", "R2!", "r2.", "R2.",
            "りっちゃん２　", "りっちゃん2 ", "r2>"
        ],
        "production": [
            "rt!", "Rt!", "RT!", "rt.", "Rt.",
            "RT.", "りつ！", "りつ."
        ],
        "sub": [
            "rt#", "りつちゃん ", "りつたん ", "りつ ",
            "りつちゃん　", "りつたん　", "りつ　", "Rt#", "RT#"
        ],
        "alpha": ["r3!", "r3>"]
    },
    "colors": {name: getattr(Colors, name) for name in dir(Colors)},
    "admins": [
        634763612535390209, 266988527915368448,
        667319675176091659, 693025129806037003
    ]
}


RTCHAN_COLORS = {
    "normal": 0xa6a5c4,
    "player": 0x84b9cb,
    "queue": 0xeebbcb
}


def is_admin(user_id: Optional[int] = None):
     "管理者かチェックをする関数です。"
     def check(ctx):
         if isinstance(user_id, int):
             return user_id in data["admins"]
         else:
             return ctx.author.id in data["admins"]
     if user_id is None:
         return commands.check(check)
     else:
         return check(user_id)


PERMISSION_TEXTS = {
    "administrator": "管理者",
    "view_audit_log": "監査ログを表示",
    "manage_guild": "サーバー管理",
    "manage_roles": "ロールの管理",
    "manage_channels": "チャンネルの管理",
    "kick_members": "メンバーをキック",
    "ban_members": "メンバーをBAN",
    "create_instant_invite": "招待を作成",
    "change_nickname": "ニックネームの変更",
    "manage_nicknames": "ニックネームの管理",
    "manage_emojis": "絵文字の管理",
    "manage_webhooks": "ウェブフックの管理",
    "manage_events": "イベントの管理",
    "manage_threads": "スレッドの管理",
    "use_slash_commands": "スラッシュコマンドの使用",
    "view_guild_insights": "テキストチャンネルの閲覧＆ボイスチャンネルの表示",
    "send_messages": "メッセージを送信",
    "send_tts_messages": "TTSメッセージを送信",
    "manage_messages": "メッセージの管理",
    "embed_links": "埋め込みリンク",
    "attach_files": "ファイルを添付",
    "read_message_history": "メッセージ履歴を読む",
    "mention_everyone": "@everyone、@here、全てのロールにメンション",
    "external_emojis": "外部の絵文字の使用",
    "add_reactions": "リアクションの追加",
    "connect": "接続",
    "speak": "発言",
    "stream": "動画",
    "mute_members": "メンバーをミュート",
    "deafen_members": "メンバーのスピーカーをミュート",
    "move_members": "メンバーを移動",
    "use_voice_activation": "音声検出を使用",
    "priority_speaker": "優先スピーカー"
}