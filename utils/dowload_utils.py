from pytubefix import YouTube
import instaloader


def load_audio(url):
        try:  
            yt = YouTube(url=url)
            audio_name = yt.title
            stream = yt.streams.filter(only_audio=True).first().download(
                                   output_path='static/audio', filename=f'{audio_name}.mp3')
            return stream
        except Exception:
              return f"Зараз завантаження не доступно спробуй пізніше"
        

def load_video(url):
      try:
           yt = YouTube(url=url)
           video_name = yt.title
           stream = yt.streams.get_highest_resolution().download(output_path='static/video', filename=f'{video_name}.mp4')
           return stream
      except Exception:
            return f"Зараз завантаження не доступно спробуй пізніше"
      

def load_insta_pic(prof):
      try:
            pic_loader = instaloader.Instaloader(dirname_pattern='static/instapic')
            prof = prof
            pic = pic_loader.download_profile(profile_name=prof, profile_pic_only=True)
            return pic
      except Exception:
            return f"Зараз завантаження не доступно спробуй пізніше"
      
# a = load_insta_pic(prof='tumoschuk_officiall')
# print(a)
