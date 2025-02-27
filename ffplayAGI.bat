@echo off
setlocal enabledelayedexpansion

rem 获取传入的参数（可以是多个文件或文件夹）
:process_arguments
if "%~1"=="" goto :end_arguments

set "arg=%~1"

rem 检查参数是文件还是文件夹
if exist "%arg%\*" (
    rem 参数是文件夹，处理文件夹下的所有视频文件
    for %%F in ("%arg%\*.*") do (
        call :process_video "%%F"
    )
) else (
    rem 参数是单个文件，直接处理该文件
    call :process_video "%arg%"
)

shift
goto :process_arguments

:end_arguments

REM pause
goto :eof

:process_video
rem 获取视频文件路径
set "video_path=%~1"

rem 使用 ffprobe 获取视频的时长信息（时长可能带小数）
for /f "delims=." %%A in ('ffprobe -v error -show_entries format^=duration -of default^=noprint_wrappers^=1:nokey^=1 "%video_path%"') do (
    set "duration_rounded=%%A"
    goto :found_duration
)
:found_duration

rem 将视频时长转换为整数（秒数）
set /a duration_int=!duration_rounded!

rem 比较视频时长，如果小于5分钟（300秒），使用 ffplay 播放器
if !duration_int! lss 300 (
    echo Playing with ffplay: "!video_path!"
    "C:\Users\Administrator\Desktop\ffplayAI.bat" "!video_path!"
) else (
    echo Playing with anyi1.8x: "!video_path!"
    "C:\Users\Administrator\Desktop\anyi1.8x.bat" "!video_path!"
)

goto :eof
