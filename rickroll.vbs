Set Sound = CreateObject("WMPlayer.OCX.7")
Sound.URL = "https://www.myinstants.com/media/sounds/ah-patiyo-kohomada.mp3"
Sound.controls.play
While Sound.playState <> 1
WScript.Sleep 100
Wend
WScript.Sleep(int(Sound.currentMedia.duration)+1)*1000
