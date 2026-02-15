# src/utils/pdf_generator.py
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io


class ReportPDFGenerator:
    """Generate professional PDF reports from analysis data"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Create custom paragraph styles"""
        self.styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=self.styles["Heading1"],
                fontSize=24,
                textColor=colors.HexColor("#1f77b4"),
                spaceAfter=30,
                alignment=TA_CENTER,
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="SectionHeader",
                parent=self.styles["Heading2"],
                fontSize=16,
                textColor=colors.HexColor("#2c3e50"),
                spaceAfter=12,
                spaceBefore=12,
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="MetricValue",
                parent=self.styles["Normal"],
                fontSize=14,
                textColor=colors.HexColor("#27ae60"),
                alignment=TA_CENTER,
            )
        )

    def generate_analysis_report(
        self, analysis: dict, platform: str = "Amazon"
    ) -> bytes:
        """
        Generate PDF from analysis data

        Args:
            analysis: Analysis dictionary from AI agent
            platform: Platform name (e.g., "Amazon")

        Returns:
            PDF file as bytes
        """
        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5 * inch)

        # Container for PDF elements
        story = []

        # Title
        title = Paragraph("📊 Retail Intelligence Report", self.styles["CustomTitle"])
        story.append(title)
        story.append(Spacer(1, 0.2 * inch))

        # Metadata
        metadata = f"<b>Platform:</b> {platform} | <b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        story.append(Paragraph(metadata, self.styles["Normal"]))
        story.append(Spacer(1, 0.3 * inch))

        # Key Metrics Section
        story.append(Paragraph("📈 Key Metrics", self.styles["SectionHeader"]))

        metrics_data = [
            ["Total Products", "Min Price", "Max Price", "Average Price"],
            [
                str(analysis.get("total_products", "N/A")),
                f"₹{analysis.get('price_range', {}).get('min', 0):,.0f}",
                f"₹{analysis.get('price_range', {}).get('max', 0):,.0f}",
                f"₹{analysis.get('price_range', {}).get('average', 0):,.0f}",
            ],
        ]

        metrics_table = Table(
            metrics_data, colWidths=[2 * inch, 1.5 * inch, 1.5 * inch, 1.5 * inch]
        )
        metrics_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3498db")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )

        story.append(metrics_table)
        story.append(Spacer(1, 0.3 * inch))

        # Top Rated Product
        story.append(Paragraph("🏆 Top Rated Product", self.styles["SectionHeader"]))
        top_product = analysis.get("top_rated_product", {})
        if top_product:
            top_text = f"""
            <b>Product:</b> {top_product.get('title', 'N/A')}<br/>
            <b>Rating:</b> {top_product.get('rating', 'N/A')} ⭐<br/>
            <b>Price:</b> ₹{top_product.get('price', 0):,.0f}
            """
            story.append(Paragraph(top_text, self.styles["Normal"]))
        story.append(Spacer(1, 0.2 * inch))

        # Best Value Product
        story.append(Paragraph("💎 Best Value Product", self.styles["SectionHeader"]))
        best_value = analysis.get("best_value_product", {})
        if best_value:
            value_text = f"""
            <b>Product:</b> {best_value.get('title', 'N/A')}<br/>
            <b>Reason:</b> {best_value.get('reason', 'N/A')}
            """
            story.append(Paragraph(value_text, self.styles["Normal"]))
        story.append(Spacer(1, 0.3 * inch))

        # Price Insights
        story.append(Paragraph("💡 Price Insights", self.styles["SectionHeader"]))
        insights = analysis.get("price_insights", [])
        for insight in insights:
            story.append(Paragraph(f"• {insight}", self.styles["Normal"]))
            story.append(Spacer(1, 0.1 * inch))

        story.append(Spacer(1, 0.2 * inch))

        # Recommendations
        story.append(
            Paragraph("📋 Strategic Recommendations", self.styles["SectionHeader"])
        )
        recommendations = analysis.get("recommendations", [])
        for i, rec in enumerate(recommendations, 1):
            story.append(Paragraph(f"{i}. {rec}", self.styles["Normal"]))
            story.append(Spacer(1, 0.1 * inch))

        # Footer
        story.append(Spacer(1, 0.5 * inch))
        footer = Paragraph(
            "<i>Generated by AI Retail Intelligence System | Powered by Gemini AI</i>",
            self.styles["Normal"],
        )
        story.append(footer)

        # Build PDF
        doc.build(story)

        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()

        return pdf_bytes
