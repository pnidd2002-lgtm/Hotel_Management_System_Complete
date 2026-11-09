param(
    [string]$DocPath,
    [string]$PdfPath
)

$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($DocPath)
    # 17 represents wdFormatPDF
    $doc.SaveAs([ref]$PdfPath, [ref]17)
    $doc.Close()
    Write-Output "SUCCESS"
} catch {
    Write-Output "ERROR: $($_.Exception.Message)"
} finally {
    $word.Quit()
}
