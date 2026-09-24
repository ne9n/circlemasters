import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_resume():
    doc = docx.Document()

    # Set margins
    for section in doc.sections:
        section.top_margin = Inches(0.55)
        section.bottom_margin = Inches(0.55)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)

    # Style definitions
    doc.styles['Normal'].font.name = 'Arial'
    doc.styles['Normal'].font.size = Pt(9.5)
    doc.styles['Normal'].font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    def add_section_header(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title.upper())
        run.bold = True
        run.font.size = Pt(10.5)
        run.font.color.rgb = RGBColor(0x0B, 0x3C, 0x5D)
        
        pPr = p._p.get_or_add_pPr()
        pBdr = parse_xml(r'<w:pBdr %s><w:bottom w:val="single" w:sz="6" w:space="2" w:color="0B3C5D"/></w:pBdr>' % nsdecls('w'))
        pPr.append(pBdr)

    def add_role_header(title_or_company, dates, is_bold_title=True, is_bold_dates=True, space_before=5):
        table = doc.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        col_widths = [Inches(5.0), Inches(2.2)]
        for i, width in enumerate(col_widths):
            table.columns[i].width = width

        cell_left = table.cell(0, 0)
        cell_right = table.cell(0, 1)

        p_left = cell_left.paragraphs[0]
        p_left.paragraph_format.space_before = Pt(space_before)
        p_left.paragraph_format.space_after = Pt(1)
        p_left.paragraph_format.keep_with_next = True
        run_l = p_left.add_run(title_or_company)
        run_l.bold = is_bold_title
        run_l.font.size = Pt(10) if is_bold_title else Pt(9.5)
        run_l.font.color.rgb = RGBColor(0x11, 0x11, 0x11)

        p_right = cell_right.paragraphs[0]
        p_right.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_right.paragraph_format.space_before = Pt(space_before)
        p_right.paragraph_format.space_after = Pt(1)
        p_right.paragraph_format.keep_with_next = True
        run_r = p_right.add_run(dates)
        run_r.bold = is_bold_dates
        run_r.font.size = Pt(9.5)
        run_r.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

        for cell in (cell_left, cell_right):
            tcPr = cell._tc.get_or_add_tcPr()
            tcMar = parse_xml(r'<w:tcMar %s><w:top w:w="0" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:left w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tcMar>' % nsdecls('w'))
            tcPr.append(tcMar)

    def add_job_description(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.italic = True
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    def add_bullet(text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1.5)
        r_text = p.add_run(text)
        r_text.font.size = Pt(9)
        r_text.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # --- Header / Contact Info ---
    p_name = doc.add_paragraph()
    p_name.paragraph_format.space_before = Pt(0)
    p_name.paragraph_format.space_after = Pt(1)
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_name = p_name.add_run("DAVID SIEGLER")
    r_name.bold = True
    r_name.font.size = Pt(16)
    r_name.font.color.rgb = RGBColor(0x0B, 0x3C, 0x5D)

    p_contact = doc.add_paragraph()
    p_contact.paragraph_format.space_before = Pt(0)
    p_contact.paragraph_format.space_after = Pt(4)
    p_contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_contact = p_contact.add_run("New Berlin, WI  •  (262) 278-3232  •  dwsiegler@gmail.com  •  linkedin.com/in/davidsiegler  •  github.com/ne9n")
    r_contact.font.size = Pt(9)
    r_contact.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    # --- Summary ---
    add_section_header("Professional Summary")
    p_sum = doc.add_paragraph()
    p_sum.paragraph_format.space_before = Pt(2)
    p_sum.paragraph_format.space_after = Pt(3)
    r_sum = p_sum.add_run(
        "Technical Leader with 25+ years directing embedded systems, motor drives, power electronics, and edge computing programs. Proven track record managing global teams of up to 148 engineers, implementing Agile/Scrum processes, and delivering IEC 61508 functional safety compliant hardware and firmware. Holder of 7 US patents."
    )
    r_sum.font.size = Pt(9)

    # --- Technical Skills ---
    add_section_header("Technical Skills & Core Competencies")
    p_skills = doc.add_paragraph()
    p_skills.paragraph_format.space_before = Pt(1)
    p_skills.paragraph_format.space_after = Pt(2)
    
    def add_skill_line(cat, details):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0.5)
        p.paragraph_format.space_after = Pt(1)
        r_cat = p.add_run(f"• {cat}: ")
        r_cat.bold = True
        r_cat.font.size = Pt(9)
        r_det = p.add_run(details)
        r_det.font.size = Pt(9)

    add_skill_line("Engineering Leadership", "Global Team Management (up to 148 engineers), Multi-site Operations, Agile/Scrum/Kanban, Product Roadmapping, Budget & Resource Planning.")
    add_skill_line("Embedded Software", "C, MATLAB, PLC / Ladder / Function Block, V-Model, Automated Testing Frameworks, HW/SW Integration, DeviceLogix, ISaGRAF.")
    add_skill_line("Power & Motion", "Variable Frequency Drives (2 hp–5000 hp), Power Conversion, Inverters, Converters, Regenerative Units, BMS, PCBA Design.")
    add_skill_line("Industrial IoT & Networks", "Edge Computing Platforms, BMC/BIOS, CIP, Industrial Ethernet, TCP/IP, CAN, RS-485.")
    add_skill_line("Compliance & Safety", "IEC 61508 Functional Safety, UL, CSA.")

    # --- Experience ---
    add_section_header("Professional Experience")

    # Briggs & Stratton
    add_role_header("Briggs & Stratton — Milwaukee, WI", "March 2023 – Present", is_bold_title=True, is_bold_dates=True, space_before=4)
    add_role_header("Senior R&D Manager – Electronics", "March 2023 – Present", is_bold_title=False, is_bold_dates=False, space_before=1)
    add_job_description("Directed R&D electronics, embedded software, and electrical engineering for a $1.5B business, leading electrification platforms, battery management systems (BMS), and motor drives.")
    add_bullet("Built a shared-services engineering organization overseeing advanced platform technology assessment, IoT initiatives, and continuous engineering support.")
    add_bullet("Standardized engineering workflows across PCB development and embedded software, cutting cycle times and improving cross-functional handoffs.")
    add_bullet("Led IEC 61508 functional safety compliance and engineering governance across next-generation electrification platforms.")
    add_bullet("Managed contractor and engineering service partner deliverables to achieve on-schedule program execution.")

    # Milwaukee Electric Tool
    add_role_header("Milwaukee Electric Tool — Milwaukee, WI", "January 2019 – November 2022", is_bold_title=True, is_bold_dates=True, space_before=5)
    add_role_header("Chief Engineer – Batteries, Chargers & Portable Power", "January 2019 – November 2022", is_bold_title=False, is_bold_dates=False, space_before=1)
    add_job_description("Led electrical architecture, embedded software, and functional safety engineering for cordless power tools, portable power equipment, and battery/charger platforms.")
    add_bullet("Architected embedded networking and object-data abstraction layers within core tool infrastructure, enabling smart-tool connectivity and diagnostics.")
    add_bullet("Deployed formal firmware requirements and automated verification frameworks, improving battery and charger firmware reliability.")
    add_bullet("Recruited and scaled Agile/Scrum engineering teams, establishing standard quality metrics and coaching frameworks.")
    add_bullet("Delivered multiple high-volume product programs from concept to mass production within budget and target release dates.")

    # Foxconn
    add_role_header("Foxconn — Milwaukee, WI", "May 2018 – April 2019", is_bold_title=True, is_bold_dates=True, space_before=5)
    add_role_header("Senior Firmware Manager – BMC & Industrial Edge Computing", "May 2018 – April 2019", is_bold_title=False, is_bold_dates=False, space_before=1)
    add_job_description("Recruited and led the regional firmware organization developing baseboard management controllers (BMC), BIOS, and industrial edge computing systems.")
    add_bullet("Hired and structured an embedded engineering team from the ground up dedicated to BMC and BIOS development.")
    add_bullet("Integrated edge IoT telemetry with cloud AI and SaaS data analytics pipelines, partnering with regional enterprise clients to expand market adoption.")

    # Rockwell Automation
    add_role_header("Rockwell Automation — Milwaukee, WI (Total Tenure: 28 Years)", "1990 – November 2018", is_bold_title=True, is_bold_dates=True, space_before=5)

    # Role 1: Firmware Architect
    add_role_header("Firmware Architect", "January 2017 – November 2018", is_bold_title=False, is_bold_dates=False, space_before=2)
    add_job_description("Defined long-term firmware architecture roadmaps, evaluated emerging technologies, and aligned cross-business technical runways.")
    add_bullet("Established enterprise-level firmware architecture roadmaps, enabling parallel development streams across multiple Agile teams.")
    add_bullet("Aligned cross-business value streams for system-level releases, integrating drive platforms with enterprise automation software.")

    # Role 2: Interim Director
    add_role_header("Interim Firmware / Software Director", "January 2016 – December 2017", is_bold_title=False, is_bold_dates=False, space_before=3)
    add_job_description("Directed global embedded firmware and software engineering operations developing variable frequency drive (VFD) product lines across 5 global design centers.")
    add_bullet("Managed 148 engineers, 7 engineering managers, and 11 senior technical leads across 3 US and 2 international sites.")
    add_bullet("Assumed schedule ownership for at-risk programs, deploying automated testing frameworks to expand test coverage and recover critical delivery dates.")

    # Role 3: Engineering Manager
    add_role_header("Firmware Engineering Manager", "January 2010 – December 2016", is_bold_title=False, is_bold_dates=False, space_before=3)
    add_job_description("Managed engineering teams developing reusable embedded firmware components and control architectures for industrial drives.")
    add_bullet("Led recovery and accelerated release of the PowerFlex 750 drive family (2 hp–5000 hp) across converters, inverters, and regen units (Rockwell Automation Team Award winner).")
    add_bullet("Introduced, trained, and launched 5 Scrum teams; served as product owner for initial backlogs and doubled team size in 6 months.")
    add_bullet("Directed HW/SW integration, IEC 61508 functional safety, PLC motion integration, and embedded logic engines across a 1.2M+ LOC codebase.")

    # Role 4: Team Leader / Lead Engineer
    add_role_header("Firmware Team Leader / Lead Engineer – Drive Logic Controllers", "2006 – 2012", is_bold_title=False, is_bold_dates=False, space_before=3)
    add_job_description("Led engineering team developing modular firmware components, logic controllers, and communication interfaces for industrial drives.")
    add_bullet("Managed 11 firmware engineers across hiring, mentorship, and delivery of system logic and communication products.")
    add_bullet("Implemented embedded logic engines into VFD product architectures to expand drive programmability.")

    # Earlier roles
    p_early = doc.add_paragraph()
    p_early.paragraph_format.space_before = Pt(3)
    p_early.paragraph_format.space_after = Pt(2)
    p_early.paragraph_format.keep_with_next = True
    r_ep = p_early.add_run("Earlier Roles (Rockwell Automation): ")
    r_ep.bold = True
    r_ep.font.size = Pt(9)
    r_et = p_early.add_run("Senior Software/Firmware Engineer  •  Senior Developer Lead Engineer  •  Supervisor, Performance Engineering  •  Development Engineer")
    r_et.font.size = Pt(9)

    # --- Patents & Education ---
    add_section_header("Patents & Education")
    p_pat = doc.add_paragraph()
    p_pat.paragraph_format.space_before = Pt(1)
    p_pat.paragraph_format.space_after = Pt(1)
    r_pt = p_pat.add_run("• Patents: ")
    r_pt.bold = True
    r_pt.font.size = Pt(9)
    r_pt_text = p_pat.add_run("7 Granted US Patents in industrial control, power conversion, and embedded logic.")
    r_pt_text.font.size = Pt(9)

    add_role_header("Bachelor of Science (B.S.) in Physics", "University of Wisconsin–Parkside", is_bold_title=True, is_bold_dates=False, space_before=2)
    p_edu = doc.add_paragraph()
    p_edu.paragraph_format.space_before = Pt(0.5)
    p_edu.paragraph_format.space_after = Pt(1)
    r_ed = p_edu.add_run("Concentration: Control Systems, Computer Science, and Electrical Engineering — Kenosha, WI")
    r_ed.font.size = Pt(9)

    doc.save("C:\\circlemasters\\david_new.docx")
    print("Regenerated C:\\circlemasters\\david_new.docx successfully.")

if __name__ == "__main__":
    create_resume()
