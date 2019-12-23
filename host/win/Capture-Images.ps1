param(
    [string]$outDir = "C:\temp",
    [int32]$numPages = 2
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

    [DllImport("User32.dll")]
    public static extern int GetWindowThreadProcessId(IntPtr hWnd, out int lpdwProcessId);
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

function Count-Down {
    param(
        [int]$numSeconds
        )

    For ($i = $numSeconds; $i -gt 0; $i--) {
        Write-Host "$($i)..."
        Start-Sleep -Seconds 1;
    }
}

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

Write-Host "Please select your active window in"
Count-Down 3


$handle = [Utils]::GetForegroundWindow()
$myPid = New-Object System.Int32;
[Utils]::GetWindowThreadProcessId($handle, [ref]$myPid);

$proc = Get-Process -Id $myPid
Write-Host "Active window was selected to be $($proc.Name)/$($proc.Description) with PID $($myPid)"
Write-Host "Press Enter to continue"
Read-Host
Write-Host "Screenshots will be saved in $outDir"
Write-Host "Starting in"
Count-Down 4

For ($i=1; $i -le $numPages; $i++) {
    $fname = "$($outDir)\capture$($i).png"
    Write-Host $fname;
    # note how Powershell-defined functoins are called!
    Snap $handle $fname;
    Start-Sleep -Seconds 1;
}
