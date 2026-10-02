from moviepy import (
    AudioFileClip,
    VideoFileClip,
    concatenate_videoclips,
    vfx,
)


def ajusta_video_e_audio(
    dados_cena: list[dict], caminho_saida: str
) -> str:
    """Recebe uma lista de dicionários contendo os caminhos de audio e video
    de cada cena, ajusta a sincronia milissegundo a milissegundo e exporta o vídeo.
    """
    clips_prontos = []

    for scene in dados_cena:
        clip_audio = AudioFileClip(scene["audio_path"])
        clip_video = VideoFileClip(scene["video_path"])

        duracao_audio = clip_audio.duration

        # Ajuste de tempo usando a nova sintaxe do vfx.Loop e subclipped
        if clip_video.duration < duracao_audio:
            clip_video = clip_video.with_effects([vfx.Loop(duration=duracao_audio)])
        else:
            clip_video = clip_video.subclipped(0, duracao_audio)

        # Anexa o áudio da cena e redimensiona para 1080x1920
        clip_video = clip_video.with_audio(clip_audio)
        clip_video = clip_video.resized(new_size=(1080, 1920))
        clips_prontos.append(clip_video)

    # Concatena todas as cenas
    clip_final = concatenate_videoclips(clips_prontos, method="compose")

    # Renderização via FFmpeg
    clip_final.write_videofile(
        caminho_saida,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        threads=4,
    )

    return caminho_saida
