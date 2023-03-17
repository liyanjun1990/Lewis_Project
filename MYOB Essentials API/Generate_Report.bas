Attribute VB_Name = "Module1"
Sub generate_report()

Dim row_count As Integer

Dim s As Worksheet
' clear all
For Each s In ThisWorkbook.Worksheets
    If Right(s.Name, 2) = "BS" Or Right(s.Name, 2) = "PL" Then
        s.Range("A5:H1000").ClearContents
        s.Range("A5:H1000").ClearFormats
        s.Range("A:A").NumberFormat = "@"
        s.Range("C:C").NumberFormat = "$#,##0.00"
        s.Range("D:D").NumberFormat = "$#,##0.00"
        s.Range("E:E").NumberFormat = "$#,##0.00"
        s.Range("F:F").NumberFormat = "0.00%"
    End If
Next s

row_count = Sheet6.Cells(Rows.Count, 1).End(xlUp).Row

Dim row_count_temp As Integer

Dim b As Range

For Each b In Sheet6.Range("A2:A" & row_count)
    If b.Offset(0, 6) <> "" Then
        Account_Name = b.Offset(0, 1).Value
        Account_Code = b.Offset(0, 2).Value
        Account_Class = b.Offset(0, 4).Value
        Account_Company = b.Offset(0, 6).Value
        Month_Amount = b.Offset(0, 5).Value
        Yearly_Amount = b.Offset(0, 7).Value
        
'        If Month_Amount <> 0 Or Yearly_Amount <> 0 Then
        
            row_count_temp = Worksheets(Account_Company).Cells(Rows.Count, 1).End(xlUp).Row + 1
            Worksheets(Account_Company).Cells(row_count_temp, 1) = Account_Code
            Worksheets(Account_Company).Cells(row_count_temp, 2) = Account_Name
            Worksheets(Account_Company).Cells(row_count_temp, 3) = Month_Amount
            If Right(Account_Company, 2) = "PL" Then
                Worksheets(Account_Company).Cells(row_count_temp, 4) = Yearly_Amount
                Worksheets(Account_Company).Cells(row_count_temp, 5) = Month_Amount - Yearly_Amount
            
                If Month_Amount - Yearly_Amount <> 0 Then Worksheets(Account_Company).Cells(row_count_temp, 6) = (Month_Amount - Yearly_Amount) / Yearly_Amount
            End If
            
            Worksheets(Account_Company).Cells(row_count_temp, 7) = Account_Class
            Worksheets(Account_Company).Cells(row_count_temp, 8) = Application.WorksheetFunction.XLookup(Account_Class, Sheet8.Range("B:B"), Sheet8.Range("C:C"))
'        End If
        
    End If

Next b

' add YR


End Sub

Sub PL(worksheet_name As String)

Dim TS As Worksheet

Set TS = Worksheets(worksheet_name)

Dim row_count As Integer

row_count = TS.Cells(Rows.Count, 1).End(xlUp).Row

TS.Cells(4, 1).CurrentRegion.Sort Key1:=Range("H4"), Order1:=xlAscending, Header:=xlYes

' sort column first

Dim class_string As String

For Each i In Application.WorksheetFunction.Unique(TS.Range("G5:G" & row_count))
    class_string = i
    
    class_string_first = TS.Range("G:G").Find(What:=class_string, LookIn:=xlValues, LookAt:=xlWhole, SearchDirection:=xlNext).Row
    class_string_last = TS.Range("G:G").Find(What:=class_string, LookIn:=xlValues, LookAt:=xlWhole, SearchDirection:=xlPrevious).Row
    
    TS.Cells(class_string_last + 1, 1).EntireRow.Insert
    TS.Cells(class_string_last + 1, 1).EntireRow.Insert
    TS.Cells(class_string_last + 1, 2) = class_string & " Total"
    
    'add format
    With TS.Cells(class_string_last + 1, 1).Resize(1, 6).Borders(xlEdgeTop)
        .LineStyle = xlContinuous
        .ColorIndex = 0
        .TintAndShade = 0
        .Weight = xlThin
    End With
    
    sum_current = Application.WorksheetFunction.Sum(TS.Cells(class_string_first, 3).Resize(class_string_last - class_string_first + 1, 1))
    sum_ytd = Application.WorksheetFunction.Sum(TS.Cells(class_string_first, 4).Resize(class_string_last - class_string_first + 1, 1))
    TS.Cells(class_string_last + 1, 3) = sum_current
    TS.Cells(class_string_last + 1, 4) = sum_ytd
    TS.Cells(class_string_last + 1, 5) = "=R[0]C[-1] - R[0]C[-2]"
    TS.Cells(class_string_last + 1, 6) = "=iferror(R[0]C[-1]/R[0]C[-2],0)"

Next i

Dim agg_end_column As Integer
sum_result_current = 0
sum_result_YTD = 0

' agg
For Each i In Worksheets("Agg").Range("B1:B3")
    
    agg_end_column = i.End(xlToRight).Column
    For j = 3 To agg_end_column Step 2
        class_string = i.Offset(0, j - 2).Value
        If Application.WorksheetFunction.CountIf(TS.Range("B:B"), class_string) > 0 Then
            class_string_row = TS.Range("B:B").Find(What:=class_string, LookIn:=xlValues, LookAt:=xlWhole, SearchDirection:=xlNext).Row
            sum_result_current = sum_result_current + TS.Cells(class_string_row, 3).Value * i.Offset(0, j - 1).Value
            sum_result_YTD = sum_result_YTD + TS.Cells(class_string_row, 4).Value * i.Offset(0, j - 1).Value
        End If
    Next j
    
    TS.Cells(class_string_row + 1, 1).EntireRow.Insert
    TS.Cells(class_string_row + 1, 1).EntireRow.Insert
    TS.Cells(class_string_row + 2, 2) = i.Value
    TS.Cells(class_string_row + 2, 3) = sum_result_current
    TS.Cells(class_string_row + 2, 4) = sum_result_YTD
    TS.Cells(class_string_row + 2, 5) = sum_result_current - sum_result_YTD
    TS.Cells(class_string_row + 2, 6) = "=iferror(R[0]C[-1]/R[0]C[-2],0)"
    sum_result_current = 0
    sum_result_YTD = 0

    'add format
        With TS.Cells(class_string_row + 2, 1).Resize(1, 6).Borders(xlEdgeTop)
        .LineStyle = xlContinuous
        .ColorIndex = 0
        .TintAndShade = 0
        .Weight = xlThin
    End With
    With TS.Cells(class_string_row + 2, 1).Resize(1, 6).Borders(xlEdgeBottom)
        .LineStyle = xlContinuous
        .ColorIndex = 0
        .TintAndShade = 0
        .Weight = xlMedium
    End With
    
Next i

End Sub

Sub BS(worksheet_name As String)

Dim TS As Worksheet

Set TS = Worksheets(worksheet_name)

Dim row_count As Integer

row_count = TS.Cells(Rows.Count, 1).End(xlUp).Row

' sort

TS.Cells(4, 1).CurrentRegion.Sort Key1:=Range("H4"), Order1:=xlAscending, Header:=xlYes

Dim class_string As String

For Each i In Application.WorksheetFunction.Unique(TS.Range("G5:G" & row_count))
    class_string = i
    
    class_string_first = TS.Range("G:G").Find(What:=class_string, LookIn:=xlValues, LookAt:=xlWhole, SearchDirection:=xlNext).Row
    class_string_last = TS.Range("G:G").Find(What:=class_string, LookIn:=xlValues, LookAt:=xlWhole, SearchDirection:=xlPrevious).Row
    
    TS.Cells(class_string_last + 1, 1).EntireRow.Insert
    TS.Cells(class_string_last + 1, 1).EntireRow.Insert
    TS.Cells(class_string_last + 1, 2) = class_string & " Total"
    
    'add format
    With TS.Cells(class_string_last + 1, 1).Resize(1, 6).Borders(xlEdgeTop)
        .LineStyle = xlContinuous
        .ColorIndex = 0
        .TintAndShade = 0
        .Weight = xlThin
    End With
    
    sum_current = Application.WorksheetFunction.Sum(TS.Cells(class_string_first, 3).Resize(class_string_last - class_string_first + 1, 1))
    sum_ytd = Application.WorksheetFunction.Sum(TS.Cells(class_string_first, 4).Resize(class_string_last - class_string_first + 1, 1))
    TS.Cells(class_string_last + 1, 3) = sum_current
'    TS.Cells(class_string_last + 1, 4) = sum_ytd
'    TS.Cells(class_string_last + 1, 5) = "=R[0]C[-1] - R[0]C[-2]"
'    TS.Cells(class_string_last + 1, 6) = "=iferror(R[0]C[-1]/R[0]C[-2],0)"

Next i

Dim agg_end_column As Integer
sum_result_current = 0
sum_result_YTD = 0

For Each i In Worksheets("Agg").Range("B4:B6")
    
    agg_end_column = i.End(xlToRight).Column
    For j = 3 To agg_end_column Step 2
        class_string = i.Offset(0, j - 2).Value
        If Application.WorksheetFunction.CountIf(TS.Range("B:B"), class_string) > 0 Then
            class_string_row = TS.Range("B:B").Find(What:=class_string, LookIn:=xlValues, LookAt:=xlWhole, SearchDirection:=xlNext).Row
            sum_result_current = sum_result_current + TS.Cells(class_string_row, 3).Value * i.Offset(0, j - 1).Value
            sum_result_YTD = sum_result_YTD + TS.Cells(class_string_row, 4).Value * i.Offset(0, j - 1).Value
        End If
    Next j
    
    TS.Cells(class_string_row + 1, 1).EntireRow.Insert
    TS.Cells(class_string_row + 1, 1).EntireRow.Insert
    TS.Cells(class_string_row + 2, 2) = i.Value
    TS.Cells(class_string_row + 2, 3) = sum_result_current
'    TS.Cells(class_string_row + 2, 4) = sum_result_YTD
'    TS.Cells(class_string_row + 2, 5) = sum_result_current - sum_result_YTD
'    TS.Cells(class_string_row + 2, 6) = "=iferror(R[0]C[-1]/R[0]C[-2],0)"
    sum_result_current = 0
    sum_result_YTD = 0
    
    'add format
        With TS.Cells(class_string_row + 2, 1).Resize(1, 6).Borders(xlEdgeTop)
        .LineStyle = xlContinuous
        .ColorIndex = 0
        .TintAndShade = 0
        .Weight = xlThin
    End With
    With TS.Cells(class_string_row + 2, 1).Resize(1, 6).Borders(xlEdgeBottom)
        .LineStyle = xlContinuous
        .ColorIndex = 0
        .TintAndShade = 0
        .Weight = xlMedium
    End With
    
Next i

End Sub


Sub generate_individual()

Dim sheetname As String

sheetname = ActiveSheet.Name

If Right(sheetname, 2) = "BS" Then Call BS(sheetname)

If Right(sheetname, 2) = "PL" Then Call PL(sheetname)


End Sub

Sub generate_all()

Dim Date_string As String

Date_string = InputBox("The Period for the Report")

Dim s As Worksheet
Dim sheetname As String
Dim row_count As Integer

For Each s In ThisWorkbook.Worksheets
    s.Activate
    sheetname = s.Name
    
    If Right(sheetname, 2) = "BS" Then
        Call BS(sheetname)
        s.Cells(3, 1) = Date_string
        row_count = s.Cells(Rows.Count, 1).End(xlUp).Row
        For i = row_count To 5 Step -1
            If s.Cells(i, 3) = 0 And s.Cells(i, 1) <> "" Then s.Cells(i, 3).EntireRow.Delete
        Next i
    End If
    
    If Right(sheetname, 2) = "PL" Then
        Call PL(sheetname)
        s.Cells(3, 1) = Date_string
        row_count = s.Cells(Rows.Count, 1).End(xlUp).Row
        For i = row_count To 5 Step -1
            If s.Cells(i, 3) = 0 And s.Cells(i, 4) = 0 And s.Cells(i, 1) <> "" Then s.Cells(i, 3).EntireRow.Delete
        Next i
    End If
Next s

End Sub



