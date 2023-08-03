""" whisper wrapper for speech recognition """

import os
from loguru import logger

class WhisperWrapper(object):
    """ A wrapper for local whisper model, see whisper.cpp for details """
    def __init__(self, whisper_tool_dir: str, model_path: str, language: str = 'zh'):
        self.whisper_tool_dir = whisper_tool_dir
        self.model_path = model_path
        self.language = language
        assert os.path.isfile(self.model_path), "File not found: {}".format(self.model_path)

    def convert(self, audio_file: str, worksapce: str):
        assert os.path.isfile(audio_file), "File not found: {}".format(audio_file)
        # convert to wav file
        output_wav_file = os.path.join(worksapce, 'output.wav')
        cmd = (
            f"ffmpeg -i {audio_file}  -y -ar 16000 -ac 1 "
            f"-c:a pcm_s16le {output_wav_file}"
        )
        
        logger.info('Run command {} to convert audio...'.format(cmd))
        os.system(cmd)

        # run whisper
        basename = os.path.splitext(os.path.split(audio_file)[-1])[0]
        output_prefix = os.path.join(worksapce, basename + "_raw")
        cmd = (
            f"./main -m {self.model_path} -f {output_wav_file} "
            f"-pp -pc -ps -of {output_prefix} -osrt -otxt -l {self.language}"
        )
        cmd = f"cd {self.whisper_tool_dir} && " + cmd
        logger.info("Run command {} to do speech recognition...".format(cmd))
        os.system(cmd)

        assert os.path.isfile(output_prefix + '.txt'), "File not found: {}".format(output_prefix + '.txt')
        return output_prefix + '.txt'