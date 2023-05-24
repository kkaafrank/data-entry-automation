#SingleInstance, Force
SendMode Input
SetWorkingDir, %A_ScriptDir%

^F1::
Send 83{Tab}1{Tab}3{Tab}1{Tab}0
Send {Click 1250 1000}
Return

^F2::
Send x{Enter}
Sleep 250
Send {Tab}1265636823
Sleep 250
Send {Tab}xinqing
Sleep 250
Send {tab}{tab}fan
Sleep 250
Send {Click 1420 1000}
Return

^F3::
Send 0490{Tab}h{Tab}{Enter}
Sleep 100
Send 45380
Sleep 1500
Send {Enter}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}2000{Tab}1{Tab}u
Send {RShift down}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}{RShift up}
Return

^F4::
Send 0490{Tab}h{Tab}{Enter}
Sleep 100
Send 45385
Sleep 1500
Send {Enter}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}2000{Tab}1{Tab}u
Send {RShift down}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}{RShift up}
Return

^F5::
Send 0490{Tab}h{Tab}{Enter}
Sleep 100
Send 43239
Sleep 1500
Send {Enter}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}1500{Tab}1{Tab}u
Send {RShift down}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}{RShift up}
Return

^F6::
Send {Click 1250 1000}
Return

#SingleInstance, Force
SendMode Input
SetWorkingDir, %A_ScriptDir%

!F1::
Send {CtrlUp}
Click -1550 140
Sleep, 500
Click
Sleep, 1000
MouseMove, 0, 360, 0, R
Click, WheelDown, 4
Sleep, 1000
Click
Sleep, 250
Click
Send ^a
Sleep 100
Send ^c
Send {ALT DOWN}{TAB}{ALT UP}
Sleep, 500
Send ^v
Sleep, 500
Send {ALT DOWN}{TAB}{ALT UP}
Sleep, 500
Send ^a
Sleep, 500
Send {Tab}{Tab}^c
Sleep, 500
Send {ALT DOWN}{TAB}{ALT UP}
Sleep, 500
Send {Tab}{Tab}^v
Sleep, 500
Send {ALT DOWN}{TAB}{ALT UP}
Sleep, 500
Send {Tab}{Tab}
Sleep, 500
Send ^a
Sleep, 100
Send ^c
Sleep, 100
Send {ALT DOWN}{TAB}{ALT UP}
Sleep, 500
Send {Tab}tx{Tab}^v{Tab}us{Tab}999999999{Tab}
Return

!F2::
Click -1450 140
Sleep, 500
Click
Sleep, 1500
MouseMove, 0, 360, 0, R
Click, WheelDown, 8
Sleep, 500
Send {ALT DOWN}{TAB}{ALT UP}
Return