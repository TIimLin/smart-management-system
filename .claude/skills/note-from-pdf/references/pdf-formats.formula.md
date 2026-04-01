# PDF Formats Formula

$$\text{PDFStrategy} = \text{TypeDetect}(\text{pdf}) \to \text{ExtractionMethod}$$

## PDF 類型與策略

$$\text{PDFType} = \begin{cases} \text{text-based} & \to \text{pdfplumber（主力）} \\ \text{multi-column} & \to \text{pdfplumber + column bbox detection} \\ \text{table-heavy} & \to \text{pdfplumber.extract\_tables()} \\ \text{image-heavy} & \to \text{偵測 + 警告，文字提取有限} \\ \text{hybrid} & \to \text{text + table 組合策略} \end{cases}$$

## 工具優先級

$$\text{Priority} = \text{pdfplumber} > \text{pypdf}(\text{fallback})$$

- `pdfplumber`：支援表格提取、column detection、座標定位
- `pypdf`：純文字提取，速度快，無表格支援

## 圖片偵測

$$(\text{avg chars per page} < 100) \to \text{image-heavy 判定}$$

提示使用者：此 PDF 主要為圖片，未來可用 OCR skill 處理（Wave 5+）。

## 輸出格式化

| PDF 內容 | Markdown 轉換 | 說明 |
|---------|--------------|------|
| 純文字段落 | 保留段落換行 | - |
| 表格 | markdown table | - |
| 標題（大字/粗體） | `#` / `##` 對應層次 | - |
| 列表 | `- item` | - |
| 頁碼數字 | `<!-- Page N -->` | 保留：品質驗證 + 抽樣比對錨點 |
| 重複頁首/頁尾文字 | 略過 | 連續 3 頁以上相同文字 |

## 頁碼保留的必要性

$$\text{PageMarker} = \texttt{<!-- Page N -->} \to \text{品質驗證錨點} + \text{抽樣比對基準}$$

- 可比對「原始 PDF 第 N 頁」vs「提取後 Page N 段落」，驗證轉換品質
- 長文件（100+ 頁）沒有頁碼標記，抽樣檢查無從下手
- 後續參照筆記時可標注「見 PDF Page 42」

## 重複頁首/頁尾的判定

$$(\text{連續} \geq 3 \text{ 頁出現相同文字}) \to \text{判定為重複} \to \text{略過}$$

$$(\text{唯一或偶發文字}) \to \text{保留}$$

典型重複：公司名稱、文件標題、機密等級標記、版權聲明。

## 輸出結構範例

```markdown
<!-- Page 1 -->
# 第一章：系統架構概述

本文件描述系統的整體架構設計...

<!-- Page 2 -->
## 1.1 核心組件

| 組件 | 功能 |
|------|------|
| API Gateway | 請求路由 |
```
