\# Unit 6 Compliance Rule Catalog



\## Explainable Human-in-the-Loop Import Compliance Document Screening System



This catalog defines the 15 prototype compliance checks used for Unit 6 integration and evaluation.



The system is a decision-support prototype. Regulatory checks identify potential issues for human review and do not replace the legal judgment of a customs officer or other authorized government reviewer.



For restricted goods, a permit or licence reference recorded in the synthetic document indicates only that permit information was supplied. The prototype does not verify permit authenticity, validity, expiry, quantity, issuing authority approval, or other legal conditions against a live government system.



| Rule ID | Category | Prototype Check | Expected Outcome |

|---|---|---|---|

| DOC-001 | Document completeness | Required prototype fields must be present | FLAG when one or more mandatory fields are missing |

| VAL-001 | Value validation | Declared value must be a positive numeric value | FLAG when value is zero, negative, or non-numeric |

| HS-001 | HS consistency | Product description must be consistent with the predefined prototype HS reference | FLAG when inconsistent or unsupported; route for human review |

| RES-001 | Restricted goods | Meat and meat products require regulatory review/permit information | FLAG when detected without permit information |

| RES-002 | Restricted goods | Fresh fruits, vegetables, plants, and plant products require regulatory review/permit information | FLAG when detected without permit information |

| RES-003 | Restricted goods | Human remains, including cremated remains/ashes, require regulatory review/permit information | FLAG when detected without permit information |

| RES-004 | Restricted goods | Pharmaceuticals require regulatory review/permit information | FLAG when detected without permit information |

| RES-005 | Restricted goods | Pesticides require regulatory review/permit information | FLAG when detected without permit information |

| RES-006 | Restricted goods | Firearms and ammunition require regulatory review/permit information | FLAG when detected without permit information |

| RES-007 | Restricted goods | Toy guns or imitation firearms require regulatory review/permit information | FLAG when detected without permit information |

| RES-008 | Restricted goods | Camouflage clothing or material requires regulatory review | FLAG when detected without permit information |

| RES-009 | Restricted goods | Motor vehicles require applicable import-permit/licensing review | FLAG when detected without permit information |

| PRO-001 | Prohibited goods | Honey is treated as prohibited under the prototype reference | FLAG when detected |

| PRO-002 | Prohibited goods | Counterfeit coin is prohibited | FLAG when detected |

| PRO-003 | Prohibited goods | Indecent or obscene imported material is prohibited | FLAG when detected |

\## Synthetic ASYCUDA-Aligned Declaration Model



For Unit 6, the prototype uses synthetic declaration data structured to resemble information that could be supplied by a customs declaration environment such as ASYCUDA World.



This is an ASYCUDA-aligned prototype only. It does not connect to the live Jamaica Customs Agency ASYCUDA World environment, retrieve official declaration records, validate user credentials, or modify government data.



The prototype declaration model contains the following fields:



| Prototype Field | Purpose |

|---|---|

| declaration\_reference | Synthetic customs declaration or transaction reference |

| declaration\_type | Prototype declaration category or procedure |

| customs\_office\_code | Synthetic customs office identifier |

| importer | Importer or consignee name used for screening |

| product | Declared goods description |

| declared\_value | Declared customs value supplied to the prototype |

| hs\_code | HS code supplied in the synthetic declaration |

| country\_of\_origin | Declared country of origin |

| permit\_reference | Synthetic permit or licence reference when applicable |



\### Integration Boundary



A future authorized implementation could receive selected declaration data from ASYCUDA World through an approved interface or integration service.



For this capstone, an internal adapter will normalize synthetic ASYCUDA-aligned declaration data into the field structure expected by the compliance rule engine.



The prototype integration flow is:



Synthetic ASYCUDA-Aligned Declaration

→ ASYCUDA Adapter

→ Normalized Screening Fields

→ Compliance Rule Engine

→ Deterministic Explanation

→ Human Reviewer Decision

→ Audit Log / SQLite Database



The human reviewer remains the final decision-maker.

\## Rule Outcome Semantics



PASS:

The applicable prototype check was satisfied.



FLAG:

The system identified a potential compliance issue that requires human review.



NOT\_APPLICABLE:

The rule does not apply to the product being screened.



\## Regulatory Sources



Jamaica Customs Agency. Restricted / Prohibited Items.

https://jca.gov.jm/business/imports/restricted-prohibited-items/



Jamaica Customs Agency. Restricted Items.

https://jca.gov.jm/individual/passenger/test-fixes/



Jamaica Customs Agency. Prohibited Items.

https://jca.gov.jm/individual/passenger/prohibited-items/



Trade Board Limited. Import Permit.

https://www.tradeboard.gov.jm/ttbl/importPermit.php

