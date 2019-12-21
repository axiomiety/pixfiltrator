$File = "C:\Temp\Screenshot1.bmp"
Add-Type -AssemblyName System.Windows.Forms
Add-type -AssemblyName System.Drawing

$SOURCE = @"

using System;
using System.Runtime.InteropServices;
public class Window {
    [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
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
#Rect r = New-Object Rect();


#$r = New-Object My.Utils+Rect;
#$r = New-Object System.Drawing.Rectangle
$r = New-Object Rect;
#[My.Utils]::GetWindowRect(1706286, [ref]$r);
[Window]::GetWindowRect(1706286, [ref]$r);
Write-Host $r.Bottom;



#$width = 1000
#$height = 1000
#$bitmap = [System.Drawing.Bitmap]::new($width, $height)
#$graphic = [System.Drawing.Graphics]::FromImage($bitmap)
#$graphic.CopyFromScreen($Left, $Top, 0, 0, $bitmap.Size)
#$bitmap.Save($File)
#$bitmap.Dispose()
#$graphic.Dispose()
Write-Output "saved"
