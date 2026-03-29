@echo off
chcp 65001 >nul
REM 从脚本所在目录回到项目根：scripts -> svg-flowchart -> skills -> .cursor -> 项目根
set "SCRIPT_DIR=%~dp0"
set "ROOT=%SCRIPT_DIR%..\..\..\.."
set "FLOWS=%ROOT%\论文章节\figures\flows"
set "PY=%SCRIPT_DIR%svg2pdf.py"

echo 将 论文章节\figures\flows 下所有 .svg 转为同名的 .pdf
echo 项目根: %ROOT%
echo.

if not exist "%FLOWS%" (
    echo 错误: 未找到目录 %FLOWS%
    exit /b 1
)

for %%f in ("%FLOWS%\*.svg") do (
    echo 转换: %%~nxf
    python "%PY%" "%%f" 2>nul || echo   跳过（需安装 cairosvg 或 Inkscape）
)

echo.
echo 完成。若部分未转换，请安装 cairosvg 或 Inkscape 后重试。
