# Fixing Unicode error by switching to a library that supports Unicode: reportlab
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

pdf_path = "/mnt/data/プログラミング言語_カテゴリ一覧.pdf"

# Combine all table data
data = [
    ["英語", "日本語訳", "補足"],
    ["Imperative Languages", "命令型言語", "処理手順を逐一指示するスタイル。"],
    ["Declarative Languages", "宣言型言語", "結果や目的を記述するスタイル。"],
    ["Functional Languages", "関数型言語", "関数を中心に構成、状態変化を避ける。"],
    ["Object-Oriented Languages", "オブジェクト指向言語", "オブジェクトやクラスで構造化。"],
    ["Logic Programming", "論理型言語", "論理ルールに基づいて解を導出する。"],
    ["Procedural Languages", "手続き型言語", "命令型の中でも「手続き・関数」を重視。"],
    ["Scripting Languages", "スクリプト言語", "簡易な記述でタスク自動化などに使う。"],
    ["Bytecode-Based Languages", "バイトコード系言語", "仮想マシン上でバイトコードを実行。"],
    ["Concurrent / Parallel Languages", "並行／並列処理言語", "並行性を意識した言語（例：Erlang, Go）"],
    ["Reactive Languages", "リアクティブ言語", "イベント駆動型（例：Elm, RxJS）"],
    ["Dataflow Languages", "データフロー言語", "データの流れを明示的に記述（例：LabVIEW）"],
    ["Hardware Description Languages", "ハードウェア記述言語", "ハードウェア構成を記述（例：VHDL）"],
]

# Create PDF
c = canvas.Canvas(pdf_path, pagesize=A4)
width, height = A4

# Add title
c.setFont("Helvetica-Bold", 16)
c.drawCentredString(width / 2, height - 40, "プログラミング言語のカテゴリ一覧")

# Create table
table = Table(data, colWidths=[160, 130, 230])
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.grey),
    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
]))

# Render table
table.wrapOn(c, width, height)
table_height = len(data) * 18
table.drawOn(c, 40, height - 80 - table_height)

c.save()
pdf_path
