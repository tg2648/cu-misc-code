; Excel

; CapsLock + C: Clear filter (Alt+H+S+C)
#IfWinActive ahk_exe Excel.exe
CapsLock & c::
SendInput, !hsc 
return

; CapsLock + F: Toggle filter (Alt+H+S+F)
#IfWinActive ahk_exe Excel.exe
CapsLock & f::
SendInput, !hsf 
return
