param(
    [string]$outDir = "C:\temp",
    [int32]$numPages = 5
)

#https://stackoverflow.com/questions/2969321/how-can-i-do-a-screen-capture-in-windows-powershell#2970339

Add-Type -AssemblyName System.Windows.Forms, System.Drawing


$SOURCE = @"

using System;
using System.Runtime.InteropServices;

public class Utils {
    [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);

    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
}
public struct RECT
{
    public int Left;
    public int Top;
    public int Right;
    public int Bottom;
}

"@

Add-Type $SOURCE;

function Snap {
    param(
        [System.IntPtr]$handle,
        [string]$fname
    )
    $r = New-Object RECT;
    [Utils]::GetWindowRect($handle, [ref]$r);
    Write-Host $r.Top, $r.Bottom, $r.Left, $r.Right;
    
    $width = $r.Right - $r.Left;
    $height = $r.Bottom - $r.Top;
    $bitmap = [System.Drawing.Bitmap]::new($width, $height)
    $graphic = [System.Drawing.Graphics]::FromImage($bitmap)

    #https://docs.microsoft.com/en-us/dotnet/api/system.drawing.graphics.copyfromscreen?view=netframework-4.8
    $graphic.CopyFromScreen($r.Left, $r.Top, 0, 0, $bitmap.Size)
    # are there any advantages to saving this as a png instead of bmp? size is about the same
    $bitmap.Save($fname, [System.Drawing.Imaging.ImageFormat]::Png)
    $bitmap.Dispose()
    $graphic.Dispose()
    Write-Output "saved"
}

$handle = [Utils]::GetForegroundWindow();

Write-Host "Screenshots will be saved in $outDir $($handle.GetType())"

For ($i=1; $i -le $numPages; $i++) {
    $fname = "$($outDir)\capture$($i).png"
    Write-Host $fname;
   
    Snap $handle $fname;
    Start-Sleep -Seconds 1;
}
