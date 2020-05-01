; -----
; Excel
; -----

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

; CapsLock + T: Toggle table (Alt+H+T+Enter+Enter)
#IfWinActive ahk_exe Excel.exe
CapsLock & t::
SendInput, !ht{Enter}{Enter}
return

; -------
; Outlook
; -------

; CapsLock + S: Add signature
#IfWinActive ahk_exe Outlook.exe
CapsLock & s::
SendInput, !eas{Enter}
return