' Start music 
Set Sound = CreateObject("WMPlayer.OCX.7")
Sound.settings.volume = 100
Sound.URL = "https://www.myinstants.com/media/sounds/dbcd142d-1ef2-4879-bd06-1a8c893fbc5d.mp3"
Sound.controls.play

' Set system volume to 100% quickly
Set WshShell = CreateObject("WScript.Shell")
For i = 1 To 50
    WshShell.SendKeys(Chr(&hAF)) ' Volume up key
    WScript.Sleep 2
Next

' Wait for playback to start
While Sound.playState <> 3
    WScript.Sleep 10
Wend

' Keep volume at 100% while playing
While Sound.playState = 3
    Sound.settings.volume = 100
    WshShell.SendKeys(Chr(&hAF)) ' Keep pressing volume up
    WScript.Sleep 50
Wend

'full rick roll - https://s3.eu-central-1.wasabisys.com/audio.com.audio/transcoding/63/71/1800796468257163-1800796468286551-1800796481495351.mp3?X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=W7IA3NSYSOQIKLY9DEVC%2F20251028%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Date=20251028T071034Z&X-Amz-SignedHeaders=host&X-Amz-Expires=518400&X-Amz-Signature=8132396ff26ea6cbee50d78cdc638d1cb8ec5a866209f4b7f87e5918d6968b65
'13 second rick roll - https://www.myinstants.com/media/sounds/dbcd142d-1ef2-4879-bd06-1a8c893fbc5d.mp3
