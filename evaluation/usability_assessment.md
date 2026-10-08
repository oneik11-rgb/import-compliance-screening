\# Unit 6 Qualitative Usability Assessment



\## Explainable Human-in-the-Loop Import Compliance Document Screening System



\### Evaluation Scope



A structured developer heuristic review was used to assess interface clarity and usability of the Unit 6 prototype. This was not a formal usability study with customs officers or other external participants. The purpose was to evaluate observable interface characteristics that support the intended human-review workflow.



The review focused on five criteria:



1\. Clarity of extracted declaration information.

2\. Visibility and distinction of compliance outcomes.

3\. Explainability of automated rule results.

4\. Visibility of human reviewer control.

5\. Transparency of prototype scope and limitations.



Each criterion was rated on a five-point scale:



\- 1 = Poor

\- 2 = Limited

\- 3 = Adequate

\- 4 = Good

\- 5 = Very Good



\---



\## Assessment Results



| Criterion | Score | Assessment |

|---|---:|---|

| Extracted declaration field clarity | 5/5 | The interface presents declaration reference, declaration type, customs office code, importer, product, declared value, HS code, country of origin, and permit reference in a structured table. Labels and extracted values are visually separated and easy to scan. |

| Compliance outcome visibility | 5/5 | PASS and FLAG outcomes are visually distinguishable. Green indicators are used for successful checks, while flagged results use red visual emphasis, helping the reviewer identify potential compliance issues quickly. |

| Explanation clarity | 5/5 | Each rule result includes a rule identifier, status, and plain-language explanation. For example, the restricted pesticide rule explains that a pesticide was detected without a permit or licence reference and identifies the prototype regulatory authority. |

| Human reviewer control | 5/5 | Flagged results expose a Human Reviewer Decision section. The reviewer can confirm the flag, override it, or indicate that further review is required, and can record a supporting note. This supports the human-in-the-loop design principle that automated screening does not make the final regulatory decision. |

| Prototype scope transparency | 5/5 | The interface clearly states that the declaration uses synthetic ASYCUDA-aligned data and that the system does not validate permit authenticity, validity, expiry, quantity, approval, or live government records. This reduces the risk of presenting prototype output as an official regulatory determination. |



\### Overall Heuristic Score



The prototype received an overall developer heuristic score of:



\*\*25/25, or 5.0/5.0\*\*



This score reflects the clarity of the current prototype interface against the five selected criteria. It should not be interpreted as evidence of user satisfaction or operational usability in a live customs environment.



\---



\## Supporting Interface Evidence



The strongest qualitative evidence is the restricted agricultural pesticide example. In this scenario, the interface:



\- displays the extracted declaration fields;

\- identifies both the unsupported HS-code condition and the restricted-goods condition;

\- provides a deterministic explanation for each flagged rule;

\- identifies the prototype regulatory authority for the pesticide check;

\- presents a separate Human Reviewer Decision panel;

\- allows the reviewer to select Further Review Required;

\- allows a reviewer note to be recorded before the final decision is saved.



This example demonstrates that the interface is designed to support reviewer understanding rather than simply display an unexplained automated result.



The saved reviewer-decision screen provides additional evidence that the human decision and reviewer note are recorded in the audit trail.



\---



\## Interpretation



The qualitative assessment indicates that the prototype provides a clear and understandable review workflow for the functions currently implemented. The separation of extracted declaration data, compliance-rule results, explanations, and human reviewer controls supports traceability and transparency.



The interface also reinforces the intended role of the system as decision support. Automated rules identify potential compliance issues, but the reviewer remains responsible for the final decision.



A particularly important usability feature is the explicit prototype-scope notice. Because the system uses synthetic ASYCUDA-aligned declarations rather than a live ASYCUDA World connection, the notice helps distinguish prototype screening from official government verification.



\---



\## Limitations



This assessment was conducted as a developer heuristic review and did not involve representative customs officers, regulatory-agency officers, importers, or other external users. Therefore, the results cannot establish actual user satisfaction, learnability, task efficiency, accessibility, or operational suitability.



The current prototype also uses a relatively simple web interface. Additional usability evaluation with intended users would be required before production deployment.



Future evaluation should include structured user testing, task-completion measurements, error rates, reviewer feedback, and standardized usability instruments such as the System Usability Scale where appropriate.



\---



\## Conclusion



The qualitative review found that the Unit 6 prototype communicates screening results clearly, provides understandable explanations, exposes human-review controls, and states its operational limitations explicitly. These characteristics support the explainable human-in-the-loop objectives of the capstone while preserving human decision authority.

