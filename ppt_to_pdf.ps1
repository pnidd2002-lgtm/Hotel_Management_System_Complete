param(
    [string]$PptPath,
    [string]$PdfPath
)

$ppt = New-Object -ComObject PowerPoint.Application
try {
    # Open presentation without window (WithWindow = 0)
    $pres = $ppt.Presentations.Open($PptPath, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
    # 32 represents ppSaveAsPDF
    $pres.SaveAs($PdfPath, 32)
    $pres.Close()
    Write-Output "SUCCESS"
} catch {
    Write-Output "ERROR: $($_.Exception.Message)"
} finally {
    $ppt.Quit()
}
