rem -af atempo=1.25,volume=2 -vf setpts=PTS-STARTPTS,scale=-1:1000 -sync video
@echo off
setlocal enableDelayedExpansion

rem 检查是否提供了文件夹路径
if "%~1"=="" (
    echo 请提供一个包含视频文件的文件夹路径。
    exit /b
)

rem 遍历所有拖放的项目
for %%I in (%*) do (
    if exist "%%~fI\" (
        rem 处理文件夹
        for %%J in ("%%~fI\*.*") do (
            set name=%%~nJ
            set ext=%%~xJ
            call :process_file "%%~fJ"
        )
    ) else (
        rem 处理单个文件
        set name=%%~nI
        set ext=%%~xI
        call :process_file "%%~fI"
    )
)

goto :eof

:process_file
set file=%~1

for /f "usebackq delims=" %%A in (`ffprobe_vvceasy -v error -select_streams v:0 -show_entries stream^=height -of csv^=p^=0 "%file%"`) do set height=%%A

if !height! gtr 1000 (
    vvcplay -i "%file%" -af atempo=1.75,volume=2 -vf "setpts=PTS/1.75,scale=-1:1000" -framedrop
) else if !height! gtr 720 (
    vvcplay -i "%file%" -af atempo=1.75,volume=2 -vf "setpts=PTS/1.75,scale=-1:720" -framedrop
) else (
    vvcplay -i "%file%" -af atempo=1.75,volume=2 -vf "setpts=PTS/1.75" -framedrop
)
goto :eof

endlocal
