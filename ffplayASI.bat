@echo off
setlocal enableDelayedExpansion

rem 初始化变量
set "isFile=0"
set "isDir=0"

rem 遍历所有拖放的项目
for %%I in (%*) do (
    if exist "%%~fI\" (
        set isDir=1
    ) else (
        set isFile=1
    )
)

rem 根据拖放项目的类型调用相应的脚本
if %isFile%==1 (
call python "D:\Epic\Animesave\hev-ren1_20220312_0911.35401\main_script.py" %*
) 

if %isDir%==1 (
call python "D:\Epic\Animesave\hev-ren1_20220312_0911.35401\main_script.py" %*
)

endlocal