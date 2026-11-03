import os
import io
import pandas as pd
from datetime import datetime
from django.conf import settings
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from apps.constituencies.models import Constituency
from apps.elections.models import Election, ElectionResult
from apps.demographics.models import DemographicIndicator

def build_pdf_report(report):
    params = report.report_parameters or {}
    constituency_id = params.get('constituency_id')
    region_name = params.get('region_name', 'Haryana Region')

    filename = f"report_{report.id}_{int(datetime.now().timestamp())}.pdf"
    output_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, filename)

    doc = SimpleDocTemplate(full_path, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CivicTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#0F172A')
    )
    subtitle_style = ParagraphStyle(
        'CivicSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#64748B')
    )
    heading2_style = ParagraphStyle(
        'CivicH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=14,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'CivicBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155')
    )

    story = []

    # Header / Branding
    story.append(Paragraph("CIVICLENS INTELLIGENCE PLATFORM", subtitle_style))
    story.append(Paragraph(report.title, title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M IST')} | Coverage: {region_name}", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=15))

    # Executive Overview
    story.append(Paragraph("1. Executive Summary & Overview", heading2_style))
    exec_summary_text = (
        f"This intelligence dossier aggregates verified public-interest electoral, demographic, and socioeconomic "
        f"indicators for {region_name}. Prepared for researchers, public administrators, and analysts, all indicators "
        f"are normalized to official Election Commission of India (ECI) returns and statistical directorate archives."
    )
    story.append(Paragraph(exec_summary_text, body_style))
    story.append(Spacer(1, 12))

    # Historical Election Table
    story.append(Paragraph("2. Historical Election Analytics", heading2_style))
    election_qs = Election.objects.all()
    if constituency_id:
        election_qs = election_qs.filter(constituency_id=constituency_id)
    elections = election_qs.select_related('constituency').prefetch_related('results__candidate__party')[:6]

    election_table_data = [
        ["Constituency", "Year", "Winner", "Party", "Votes", "Vote Share %", "Margin"]
    ]
    for el in elections:
        res = list(el.results.all())
        w = res[0] if len(res) > 0 else None
        r = res[1] if len(res) > 1 else None
        margin = (w.votes_received - r.votes_received) if (w and r) else 0
        election_table_data.append([
            el.constituency.name,
            str(el.election_year),
            w.candidate.name if w else "N/A",
            w.candidate.party.abbreviation if (w and w.candidate.party) else "IND",
            f"{w.votes_received:,}" if w else "-",
            f"{w.vote_share}%" if w else "-",
            f"{margin:,}"
        ])

    if len(election_table_data) == 1:
        election_table_data.append(["No historical records matching filter", "-", "-", "-", "-", "-", "-"])

    t_elections = Table(election_table_data, colWidths=[90, 45, 120, 50, 65, 75, 75])
    t_elections.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_elections)
    story.append(Spacer(1, 14))

    # Demographic Indicators
    story.append(Paragraph("3. Demographic & Socioeconomic Indicators", heading2_style))
    demo_qs = DemographicIndicator.objects.all()
    if constituency_id:
        try:
            c = Constituency.objects.get(id=constituency_id)
            demo_qs = demo_qs.filter(region_identifier__in=[c.constituency_code, c.district.district_code if c.district else ''])
        except Constituency.DoesNotExist:
            pass
    indicators = demo_qs[:8]

    demo_table_data = [
        ["Indicator Name", "Category", "Level", "Value", "Unit", "Year"]
    ]
    for ind in indicators:
        demo_table_data.append([
            ind.name,
            ind.get_category_display(),
            ind.get_region_type_display(),
            f"{ind.value:,.1f}" if ind.value > 100 else f"{ind.value}",
            ind.unit,
            str(ind.reference_year)
        ])
    if len(demo_table_data) == 1:
        demo_table_data.append(["No indicators found for specified scope", "-", "-", "-", "-", "-"])

    t_demo = Table(demo_table_data, colWidths=[150, 110, 80, 65, 65, 50])
    t_demo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_demo)
    story.append(Spacer(1, 15))

    # Methodology & Disclaimer
    story.append(Paragraph("4. Methodology & Data Governance Statement", heading2_style))
    method_text = (
        "<b>Sources:</b> Election Commission of India (ECI) official gazettes, Census of India aggregates, "
        "and Haryana Directorate of Economics & Statistics surveys.<br/>"
        "<b>Data Privacy & Ethical Compliance:</b> CivicLens operates strictly on aggregate public datasets. "
        "No individual voter records, personally identifiable voter tracking, or targeted profiling is stored or utilized.<br/>"
        "<b>Limitations:</b> Demographic projections between national census cycles represent statistical estimates."
    )
    story.append(Paragraph(method_text, body_style))

    doc.build(story)

    report.file_path = full_path
    report.file_size_bytes = os.path.getsize(full_path)
    report.status = GeneratedReport.Status.READY
    report.save()
    return full_path

def build_excel_report(report):
    params = report.report_parameters or {}
    filename = f"report_{report.id}_{int(datetime.now().timestamp())}.xlsx"
    output_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, filename)

    with pd.ExcelWriter(full_path, engine='openpyxl') as writer:
        # Sheet 1: Elections
        elections = Election.objects.all().select_related('constituency', 'state')
        el_rows = []
        for e in elections:
            w = e.results.filter(position=1).select_related('candidate__party').first()
            el_rows.append({
                'Election Year': e.election_year,
                'Constituency': e.constituency.name,
                'State': e.state.name,
                'Electors': e.total_electors,
                'Votes Polled': e.total_votes_polled,
                'Turnout %': e.turnout_percentage,
                'Winner': w.candidate.name if w else 'N/A',
                'Party': w.candidate.party.abbreviation if (w and w.candidate.party) else 'IND',
                'Winner Votes': w.votes_received if w else 0,
                'Vote Share %': w.vote_share if w else 0
            })
        df_el = pd.DataFrame(el_rows)
        df_el.to_excel(writer, sheet_name='Elections', index=False)

        # Sheet 2: Demographics
        demo = DemographicIndicator.objects.all()
        demo_rows = [
            {
                'Indicator': d.name,
                'Category': d.category,
                'Region Level': d.region_type,
                'Region Identifier': d.region_identifier,
                'Region Name': d.region_name,
                'Value': d.value,
                'Unit': d.unit,
                'Reference Year': d.reference_year,
                'Source': str(d.source) if d.source else 'Official Surveys'
            }
            for d in demo
        ]
        df_demo = pd.DataFrame(demo_rows)
        df_demo.to_excel(writer, sheet_name='Demographics', index=False)

    report.file_path = full_path
    report.file_size_bytes = os.path.getsize(full_path)
    report.status = GeneratedReport.Status.READY
    report.save()
    return full_path

def build_csv_report(report):
    params = report.report_parameters or {}
    filename = f"report_{report.id}_{int(datetime.now().timestamp())}.csv"
    output_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, filename)

    elections = Election.objects.all().select_related('constituency')
    rows = []
    for e in elections:
        w = e.results.filter(position=1).select_related('candidate__party').first()
        rows.append({
            'Year': e.election_year,
            'Constituency': e.constituency.name,
            'Constituency Code': e.constituency.constituency_code,
            'Turnout %': e.turnout_percentage,
            'Winner': w.candidate.name if w else 'N/A',
            'Party': w.candidate.party.abbreviation if (w and w.candidate.party) else 'IND',
            'Votes': w.votes_received if w else 0,
            'Vote Share %': w.vote_share if w else 0
        })
    df = pd.DataFrame(rows)
    df.to_csv(full_path, index=False)

    report.file_path = full_path
    report.file_size_bytes = os.path.getsize(full_path)
    report.status = GeneratedReport.Status.READY
    report.save()
    return full_path

