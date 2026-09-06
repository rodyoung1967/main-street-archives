#!/usr/bin/env python3
from pathlib import Path

MARKER = "Floyd Morton route family lead — 2026-09-06"

PATHS = {
    "chronology": Path("evidence/source-captures/lafarlette-morton-chronology-controls-2026-09-06.md"),
    "online": Path("evidence/source-captures/morton-wheel-1945-1947-online-access-and-lafarlette-control-pass-2026-09-06.md"),
    "bridge": Path("evidence/source-captures/morton-wheel-to-oregon-city-wheel-ownership-bridge-pass-2026-09-05.md"),
    "floyd": Path("people/profiles/floyd-lafarlette.md"),
    "request": Path("registers/research-requests/morton-wheel-and-oregon-city-wheel-pre-raye-ownership-bridge-request-2026-09-05.md"),
    "manual": Path("MANUAL-FOLLOWUP.md"),
}


def append_once(path: Path, text: str) -> None:
    current = path.read_text(encoding="utf-8")
    if MARKER in current:
        print(f"{path}: already integrated")
        return
    path.write_text(current.rstrip() + "\n\n" + text.strip() + "\n", encoding="utf-8")


def main() -> None:
    append_once(PATHS["chronology"], f"""
## Project-steward route clarification — Floyd route may have stopped at/near Morton
<!-- {MARKER} -->

On **6 September 2026**, Rodney Young added another family-history recollection: he **believes Floyd LaFarlette's trucking route stopped at Morton, Washington, or close to Morton**.

Classification: **PROJECT-STEWARD / FAMILY ORAL-HISTORY LEAD**. Rodney expressed this as a belief, not as a documented route schedule or a certain dated recollection.

This must remain separate from the route already documented in contemporary Coos County evidence. The archive directly establishes **Anderson and LaFarlette** in the **Coos Bay–Powers mail/freight business by 7 August 1947**, with later evidence identifying Floyd as the LaFarlette partner. No contemporary record yet establishes that this same business, an earlier Floyd operation, or Carl Anderson's earlier Washington bus operation served Morton.

The new recollection creates three specific tests:

1. Did **Floyd LaFarlette himself** operate, drive, own, partner in, or work for a Washington truck/bus/freight line serving Morton or eastern Lewis County before the Coos County operation?
2. Did **Carl A. Anderson's Washington passenger-carrier route** stop at Morton, Mineral, Mossyrock, Packwood, Randle, Centralia/Chehalis, or another nearby eastern Lewis County point, and if so was Floyd connected to that operation?
3. Could the remembered family presence in Morton have been tied to a **transportation stop/route assignment** rather than a long-term residence?

Do not infer that the proven Coos Bay–Powers route physically continued to Washington. A contemporary permit, timetable, carrier application, directory listing, newspaper notice, employment record, or route certificate is required before connecting the Oregon and Washington route histories.
""")

    append_once(PATHS["online"], f"""
## Floyd trucking-route family lead — Morton or nearby stop
<!-- {MARKER} -->

Rodney Young now additionally recalls/believes that **Floyd LaFarlette's trucking route stopped at Morton, Washington, or close to Morton**. This is retained as **PROJECT-STEWARD / FAMILY ORAL-HISTORY LEAD**, not route proof.

This materially sharpens the existing Washington transportation-record search. The State Archives query should not be limited to Carl A. Anderson: it should also ask for **Floyd LaFarlette / La Farlette** as an operator, employee, partner, assignee, applicant, transferee, or named person in passenger-carrier, truck/freight, motor-carrier, route-certificate, permit, docket and Commission-order records. Geographic priorities should include **Morton, Mineral, Mossyrock, Packwood, Randle, eastern Lewis County, Centralia and Chehalis**.

The existing documented **Coos Bay–Powers** route remains a separate Oregon route unless contemporary evidence explicitly bridges it to a Washington carrier or stop. The family recollection can guide discovery but cannot be used to extend that proven route northward.
""")

    append_once(PATHS["bridge"], f"""
## Floyd route may have stopped near Morton — family lead
<!-- {MARKER} -->

Rodney Young additionally believes **Floyd LaFarlette's trucking route stopped at Morton, Washington, or nearby**. Preserve this as **FAMILY / ORAL-HISTORY LEAD**.

This creates a potentially important alternative explanation for the Morton recollection: the family's Morton connection may have involved Floyd's transportation work, whether or not a long-term residence is ultimately proved. Search transportation records for Floyd directly as well as Carl A. Anderson, and search eastern Lewis County localities around Morton rather than requiring the exact city name.

Do not conflate this with the documented **Coos Bay–Powers** mail/freight route. No contemporary source currently proves that the Oregon route extended to Washington or that the Washington and Oregon carrier operations were the same enterprise.
""")

    append_once(PATHS["floyd"], f"""
## Family lead — possible Morton-area trucking stop
<!-- {MARKER} -->

Rodney Young states that he **believes Floyd's trucking route stopped at Morton, Washington, or close to Morton**. This is **PROJECT-STEWARD / FAMILY ORAL-HISTORY EVIDENCE** and should be used as a discovery lead only.

The archive already documents Floyd in the later **Anderson-LaFarlette Coos Bay–Powers** freight/mail operation. That Oregon route must not be projected into Washington. The open question is whether Floyd had an earlier or separate Washington transportation role, or whether a partner/employer's route through Morton explains the family's Morton recollection. Search Floyd/LaFarlette directly in Washington carrier permits, dockets, order books, route certificates, directories and the *Morton Journal*.
""")

    append_once(PATHS["request"], f"""
## Supplemental search instruction — Floyd / Morton-area trucking-route lead
<!-- {MARKER} -->

Rodney Young now additionally states from family memory that he **believes Floyd LaFarlette's trucking route stopped at Morton, Washington, or close to Morton**.

Classification: **FAMILY / ORAL-HISTORY LEAD — NOT DOCUMENTED ROUTE FACT**.

Please incorporate this into the Washington transportation-record lookup. In addition to **Carl Anderson / Carl A. Anderson**, search **Floyd LaFarlette / Floyd La Farlette / LaFarlette / La Farlette** for approximately **1944–1949**, extending earlier if carrier indexes suggest it, as any of the following:

- carrier/operator or permit holder;
- driver/employee;
- partner or co-owner;
- applicant, assignee, transferee or correspondent;
- person named in a route certificate, timetable, docket, order or carrier file.

Geographic priorities should include **Morton**, nearby **Mineral, Mossyrock, Packwood and Randle**, broader **eastern Lewis County**, then **Centralia/Chehalis**. Please do not treat those places as asserted residences; they are search targets based on family recollection.

The known **Anderson-LaFarlette Coos Bay–Powers** route in Oregon is independently documented and should be treated as a separate route unless a Washington record explicitly connects the operations.
""")

    append_once(PATHS["manual"], f"""
### MF-052 family-route refinement — Floyd trucking stop near Morton
<!-- {MARKER} -->

Rodney Young additionally believes **Floyd LaFarlette's trucking route stopped at Morton, Washington, or nearby**. This remains **PROJECT-STEWARD / FAMILY ORAL-HISTORY LEAD**.

Under **MF-052**, expand the Washington carrier-record query to search **Floyd LaFarlette / La Farlette directly**, not only Carl A. Anderson, and include Morton plus nearby eastern Lewis County communities such as Mineral, Mossyrock, Packwood and Randle. This may test whether the Morton family recollection arose from Floyd's transportation work even if a fixed Morton residence cannot be documented.

Keep the documented **Coos Bay–Powers** route separate: no evidence currently shows that the Oregon route extended into Washington.
""")

    print("Integrated Floyd Morton-area trucking-route family lead.")


if __name__ == "__main__":
    main()
