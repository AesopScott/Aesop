# One-shot: append 5 military-academy rows to both trackers and validate JS.
import os, re, subprocess, sys, tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

TAP_ROWS = '''
  { tier: 6, abbr: "USMA", name: "U.S. Military Academy (West Point)", branch: "army",
    location: "West Point, NY", population: "~4,400 cadets + ~6,000 permanent party",
    skillBridge: "no",
    cspName: "West Point Garrison ACS / SFL-TAP (staff)",
    cspPhone: "845-938-4621", cspEmail: "",
    detail: "Cadets commission INTO the Army at graduation - academies do not run traditional out-bound TAP for the cadet population. Permanent-party soldiers assigned to USMA access SFL-TAP through the garrison Army Community Service office. A separate cadet-resignation process is handled by the Department of Military Instruction and the Dean office when rare early separations occur.",
    actions: ["Contact West Point Garrison ACS for permanent-party SFL-TAP liaison", "Separately reach Department of Military Instruction for cadet career-path education"],
    links: ["https://www.westpoint.edu/", "https://home.army.mil/westpoint/"],
    notes: "Transition audience here is PERM-PARTY staff, not cadets. Different profile than line bases. Verify phone before outreach."
  },
  { tier: 6, abbr: "USNA", name: "U.S. Naval Academy (Annapolis)", branch: "navy",
    location: "Annapolis, MD", population: "~4,500 midshipmen + ~6,000 staff",
    skillBridge: "no",
    cspName: "NSA Annapolis Fleet & Family Support Center",
    cspPhone: "410-293-2641", cspEmail: "",
    detail: "Midshipmen commission INTO the Navy or Marine Corps at graduation. USNA permanent-party access TAP through the Fleet & Family Support Center at Naval Support Activity Annapolis, which hosts the academy. FFSC provides transition classes, resume workshops, and career counseling to separating service members, retirees, and dependents.",
    actions: ["Contact NSA Annapolis FFSC for staff TAP liaison", "Coordinate with USNA career services if engaging mid-career civilian faculty"],
    links: ["https://www.usna.edu/", "https://cnrma.cnic.navy.mil/Installations/NSA-Annapolis/"],
    notes: "Verify FFSC phone. Academy staff rotations vary widely by service affiliation."
  },
  { tier: 6, abbr: "USAFA", name: "U.S. Air Force Academy", branch: "air_force",
    location: "Colorado Springs, CO", population: "~4,400 cadets + ~4,500 staff",
    skillBridge: "no",
    cspName: "10 ABW Airman & Family Readiness Center",
    cspPhone: "719-333-3444", cspEmail: "",
    detail: "Cadets commission INTO the Air Force or Space Force. TAP services for permanent-party airmen and guardians at USAFA are run by the 10th Air Base Wing Airman & Family Readiness Center (A&FRC). Colorado Springs proximity to Peterson SFB, Schriever SFB, and Fort Carson creates a strong multi-service transition-event ecosystem.",
    actions: ["Contact 10 ABW A&FRC for TAP coordination", "Leverage Colorado Springs multi-base joint TAP events (Fort Carson, Peterson, Schriever, USAFA)"],
    links: ["https://www.usafa.edu/", "https://www.usafa.af.mil/"],
    notes: "Tightly connected to Peterson/Schriever/Fort Carson ecosystem. Consider a Colorado-Springs regional approach rather than academy-only."
  },
  { tier: 6, abbr: "USCGA", name: "U.S. Coast Guard Academy", branch: "coast_guard",
    location: "New London, CT", population: "~1,000 cadets + ~500 staff",
    skillBridge: "no",
    cspName: "USCGA Work-Life Office / USCG Transition Assistance (service-level)",
    cspPhone: "860-444-8444", cspEmail: "",
    detail: "Smallest of the five federal academies. Cadets commission INTO the Coast Guard at graduation. Active-duty CG members access the Coast Guard own Transition Assistance Program through service-level channels rather than DOD TAP; the USCGA Work-Life office provides local support and referrals. Nearby CG Base New London offers fuller transition services for staff.",
    actions: ["Contact USCGA Work-Life office for staff transitions", "Route USCG-wide TAP inquiries to CG HQ Transition Relocation Manager, not academy-level"],
    links: ["https://www.uscga.edu/"],
    notes: "Complement rather than replace USCG HQ-level transition outreach. Small population, service-specific TAP process."
  },
  { tier: 6, abbr: "USMMA", name: "U.S. Merchant Marine Academy", branch: "merchant_marine",
    location: "Kings Point, NY", population: "~950 midshipmen + ~400 staff",
    skillBridge: "no",
    cspName: "USMMA Career Services Office",
    cspPhone: "516-773-5000", cspEmail: "",
    detail: "Federal academy under the Maritime Administration (U.S. Department of Transportation), not DOD. Midshipmen graduate with a USCG license and a reserve commission in one of the uniformed services - the career path is unique, and traditional DOD TAP does not apply. Permanent-party civilian staff use Career Services and federal civilian employee channels for transition support.",
    actions: ["Contact USMMA Career Services for staff and alumni outreach", "Explore partnerships around AI-in-maritime (supply chain, port operations, logistics)"],
    links: ["https://www.usmma.edu/"],
    notes: "DOT-funded, not DOD. Unique hybrid civilian-maritime/reserve-military audience. AI-for-maritime is the natural angle."
  }'''

MWR_ROWS = '''
  { tier: 6, abbr: "USMA", name: "U.S. Military Academy (West Point)", branch: "army",
    location: "West Point, NY", population: "~4,400 cadets + ~6,000 permanent party",
    mwrActive: "yes",
    mwrName: "West Point Family & MWR (DMWR)",
    mwrPhone: "845-938-7433", mwrEmail: "",
    detail: "West Point Family & MWR operates recreational, educational, and quality-of-life programs for cadets, permanent party, and families. Portfolio includes Leisure Travel Services, Arvin Cadet Physical Development Center, West Point Ski Slope, Round Pond recreation area, youth centers, and Army Continuing Education System (ACES) classes. Separate from cadet athletic programs run by the academy directly.",
    actions: ["Contact West Point Family & MWR education programs", "Propose AI literacy classes through ACES"],
    links: ["https://westpoint.armymwr.com/"],
    notes: "High year-round population density; MWR runs robust family and youth programming alongside ACES adult-education."
  },
  { tier: 6, abbr: "USNA", name: "U.S. Naval Academy (Annapolis)", branch: "navy",
    location: "Annapolis, MD", population: "~4,500 midshipmen + ~6,000 staff",
    mwrActive: "yes",
    mwrName: "NSA Annapolis MWR",
    mwrPhone: "410-293-9200", mwrEmail: "",
    detail: "Naval Support Activity Annapolis MWR serves the USNA installation with fitness centers, a robust sailing and boating program (leveraging the Navy sailing tradition), golf courses, marinas, youth programs, and family services. Separate from the Brigade-of-Midshipmen extracurricular activities run by the academy itself.",
    actions: ["Contact NSA Annapolis MWR Community Recreation", "Explore Navy MWR Library/Education for professional-development AI content"],
    links: ["https://annapolis.navylifema.com/"],
    notes: "Distinctive boating and sailing footprint; an AI-in-maritime angle is natural."
  },
  { tier: 6, abbr: "USAFA", name: "U.S. Air Force Academy", branch: "air_force",
    location: "Colorado Springs, CO", population: "~4,400 cadets + ~4,500 staff",
    mwrActive: "yes",
    mwrName: "USAFA 10 FSS (Air Force Services - MWR equivalent)",
    mwrPhone: "719-333-4636", mwrEmail: "",
    detail: "Air Force labels its MWR equivalent Services or Force Support Squadron (FSS). USAFA 10 FSS runs Arnold Hall community center, fitness and outdoor-recreation programs on the sizable Front Range acreage, child development, education/library services, and family programs. Integrates with Peterson SFB and Schriever SFB FSS ecosystems.",
    actions: ["Contact 10 FSS Community Services", "Partner with Academy Library for digital-literacy and AI curricula"],
    links: ["https://www.usafaservices.com/"],
    notes: "Air Force FSS terminology, same concept as MWR. Large education-services footprint."
  },
  { tier: 6, abbr: "USCGA", name: "U.S. Coast Guard Academy", branch: "coast_guard",
    location: "New London, CT", population: "~1,000 cadets + ~500 staff",
    mwrActive: "limited",
    mwrName: "USCGA Morale Fund / Cadet Activities (CG MWR-equivalent)",
    mwrPhone: "860-444-8444", mwrEmail: "",
    detail: "The Coast Guard does not use the DOD MWR brand - equivalent services fall under CG Work-Life and morale-support programs. USCGA itself operates a small cadet-activities and morale-fund program; fuller recreational services for staff come from CG Base New London next door. Scale reflects the academy small footprint.",
    actions: ["Contact USCGA Morale Fund / Cadet Activities office", "Coordinate with CG Base New London MWR for staff-oriented programming"],
    links: ["https://www.uscga.edu/"],
    notes: "Smallest academy; treat MWR outreach as combined with CG Base New London when feasible."
  },
  { tier: 6, abbr: "USMMA", name: "U.S. Merchant Marine Academy", branch: "merchant_marine",
    location: "Kings Point, NY", population: "~950 midshipmen + ~400 staff",
    mwrActive: "limited",
    mwrName: "USMMA Athletic & Recreation Department",
    mwrPhone: "516-726-5889", mwrEmail: "",
    detail: "USMMA sits under the Department of Transportation (Maritime Administration), not DOD - there is no military MWR program in the DOD sense. The academy runs an Athletic & Recreation department for midshipmen (fitness, sailing, intercollegiate athletics), and staff welfare is handled through civilian federal-employee channels. Kings Point facilities include the athletic complex, sailing program, and limited on-base family services.",
    actions: ["Contact USMMA Athletic & Recreation for midshipman programming", "Explore federal-civilian employee wellness for faculty/staff"],
    links: ["https://www.usmma.edu/"],
    notes: "DOT-funded civilian-track academy. MWR framing does not map cleanly - approach as a distinct category."
  }'''


def insert_rows(path: Path, new_rows_block: str) -> None:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"(const\s+BASES\s*=\s*\[)(.*?)(\n\];)", text, re.DOTALL)
    if not m:
        raise RuntimeError(f"BASES array not found in {path}")
    if 'abbr: "USMA"' in m.group(2):
        print(f"{path.name}: already contains academy rows, skipping")
        return
    body = m.group(2)
    if not body.rstrip().endswith(","):
        body = body.rstrip() + ","
    new_body = body + "\n" + new_rows_block.strip() + "\n"
    new_text = text[:m.start(2)] + new_body + text[m.end(2):]
    path.write_text(new_text, encoding="utf-8")
    print(f"{path.name}: appended 5 academy rows")


def validate_js(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"const\s+BASES\s*=\s*(\[.*?\n\]);", text, re.DOTALL)
    if not m:
        print(f"{path.name}: could not re-extract BASES for validation")
        return
    js = m.group(1)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write("const BASES = " + js + ";\nconsole.log('OK, ' + BASES.length + ' entries');\n")
        fn = f.name
    r = subprocess.run(["node", fn], capture_output=True, text=True)
    os.unlink(fn)
    out = (r.stdout or r.stderr).strip()
    print(f"{path.name}: {out}")


if __name__ == "__main__":
    insert_rows(REPO / "ai-academy/admin/military-base-tracker.html", TAP_ROWS)
    insert_rows(REPO / "ai-academy/admin/mwr-tracker.html", MWR_ROWS)
    validate_js(REPO / "ai-academy/admin/military-base-tracker.html")
    validate_js(REPO / "ai-academy/admin/mwr-tracker.html")
