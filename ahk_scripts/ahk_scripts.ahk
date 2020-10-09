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

; -------
; OneNote
; -------

; Capslock + C: Change text style to Code (ALT + H + L + Arrow Up + Enter)
#IfWinActive ahk_exe ONENOTE.EXE
CapsLock & c::
SendInput, !hl{Up}{Enter}
return

; -------
; Chrome
; -------

; CapsLock + S: Toggle repeated left-mouse clicking
#IfWinActive ahk_exe chrome.exe
Started = 0

CapsLock & s::
     If (Started == 0)
     {
          Started = 1
          SetTimer, Clicking, 1
     }
     Else
     {
          Started = 0
          SetTimer, Clicking, Off
     }
Return

Clicking:
     Click
Return