import logging
import subprocess
import wave

logger = logging.getLogger('player')

def sample_width_to_string(sample_width):
    """Convert sample width (bytes) to ALSA format string."""
    return {1: 's8', 2: 's16', 4: 's32'}.get(sample_width, None)

class WavePlayer(object):
    """Plays short audio clips from a buffer or file."""

    def __init__(self, output_device='default'):
        self._output_device = output_device
        
        self._loaded_bytes = None
        self._loaded_samplerate = None
        self._loaded_samplewidth = None

    def play_bytes(self, audio_bytes, sample_rate=16000, sample_width=2):
        """Play audio from the given bytes-like object.

        Args:
          audio_bytes: audio data (mono)
          sample_rate: sample rate in Hertz (16 kHz by default)
          sample_width: sample width in bytes (eg 2 for 16-bit audio)
        """
        cmd = [
            'aplay',
            '-q',
            '-t', 'raw',
            '-D', self._output_device,
            '-c', '1',
            '-f', sample_width_to_string(sample_width),
            '-r', str(sample_rate),
        ]

        aplay = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        aplay.stdin.write(audio_bytes)
        aplay.stdin.close()
        retcode = aplay.wait()

        if retcode:
            logger.error('aplay failed with %d', retcode)

    def play_wav(self, wav_path):
        """Play audio from the given WAV file.

        The file should be mono and small enough to load into memory.
        Args:
          wav_path: path to the wav file
        """
        wav = wave.open(wav_path, 'r')
        if wav.getnchannels() != 1:
            raise ValueError(wav_path + ' is not a mono file')

        frames = wav.readframes(wav.getnframes())
        self.play_bytes(frames, wav.getframerate(), wav.getsampwidth())
        wav.close()

    def load_audio(self, wav_path):
        wav = wave.open(wav_path, 'r')
        if wav.getnchannels() != 1:
            raise ValueError(wav_path + ' is not a mono file')

        self._loaded_bytes = wav.readframes(wav.getnframes())
        self._loaded_samplerate = wav.getframerate()
        self._loaded_samplewidth = wav.getsampwidth()
        wav.close()

    def play_audio(self):
        if self._loaded_bytes is None:
            raise ValueError('No loaded audio file. load_audio() first.')
        self.play_bytes(self._loaded_bytes,
                        self._loaded_samplerate, self._loaded_samplewidth)


if __name__ == '__main__':

    player = WavePlayer()

    #player.play_wav("sample_sound.wav")

    player.load_audio("sample_sound.wav")
    player.play_audio()
