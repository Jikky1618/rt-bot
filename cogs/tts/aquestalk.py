# RT TTS - AquesTalk

from aiofiles import open as async_open
import asyncio


SyntheError = type("SyntheError", (Exception,), {})
libs = {}


def load_libs(paths: dict) -> None:
    """AquesTalkのライブラリを読み込みます。  
    読み込んだライブラリは`libs`に名前と一緒に辞書形式で保存されます。  
    `synthe`を使用する前にこれを実行しておいてください。

    Parameters
    ----------
    paths : Dict[str, str]
        読み込むAquesTalkのライブラリの名前とパスの辞書です。"""
    for name, path in paths.items():
        libs[name] = path


async def synthe(
        voice: str, file_path: str, text: str, speed: int = 130
    ) -> None:
    """AquesTalkを使用して音声合成を行います。　　
    使用するライブラリは`load_libs`で読み込んだものが使われます。

    Parameters
    ----------
    voice : str
        `libs`に読み込まれているライブラリの指定です。  
        `load_libs`で読み込むことができます。  
        例：`f1` (ゆっくり霊夢)
    file_path : str
        生成した音声データを書き込むファイルのパスです。
    text : str
        音声合成する文字列です。
    speed : int, default 180
        文字列を読むスピードです。

    Raises
    ------
    KeyError
        ライブラリが見つからない際に発生します。
    SyntheError
        音声合成が何かしらの理由で失敗した際に発生します。"""
    aqtk = libs[voice]

    cmd = f"./{aqtk} {speed} > {file_path}"
    # コマンドを実行する。
    proc = await asyncio.create_subprocess_shell(
        cmd, stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    # 実行結果を取得する。
    _, stderr = await proc.communicate(
        bytes(text, encoding='utf-8')
    )
    # 実行結果を出力する。
    if stderr:
        raise SyntheError(f"音声合成に失敗しました。ERR:{stderr}")


if __name__ == "__main__":
    paths = {
        "f1": "cogs/tts/lib/AquesTalk/f1",
        "f2": "cogs/tts/lib/AquesTalk/f2"
    }
    load_libs(paths)
    asyncio.run(
        synthe(
            input("声種類："), "output.wav", input("文字列：")
        )
    )
