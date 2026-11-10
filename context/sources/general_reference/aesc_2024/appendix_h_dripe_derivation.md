---
source_file: "Synapse - 2024 - Avoided Energy Supply Components in New England 2024 Repor.pdf"
citekey: synapse_AvoidedEnergySupply_2024
zotero_item: "4HZWP4NM"
public_url: "https://drive.google.com/file/d/154NYJ1K_xbqwFq1uQeN2rifByQDQrYj0/view"
short_url: "https://pub.switch.box/synapse_AvoidedEnergySupply_2024"
source_url: "https://www.synapse-energy.com/sites/default/files/inline-images/AESC%202024%20May%202024.pdf"
md5: "4fb83ebfe927b541ac86cbf599b380be"
document_type: report
filer: Synapse Energy Economics, Sustainable Energy Advantage, North Side Energy, Resource Insight, Les Deman Consulting
pages_total: 436
extraction_scope: "partial: PDF pp. 396-397 (printed pp. 378-379), Appendix H: DRIPE Derivation; the other files of this folder hold the rest of the report"
citation_scheme: page
context: "Prepared for the AESC 2024 Study Group (New England electric and gas program administrators, energy offices and regulators), the triennial study that sets the avoided costs used to screen energy efficiency and other demand-side programs in all six states. Released February 7, 2024 and amended May 24, 2024 to correct summer on-peak energy values; this is the amended release."
contents: "Appendix H: the algebraic derivation of the demand reduction induced price effect (DRIPE) from linear supply and demand (VRR) curves: equilibrium quantity and price, and the effect of horizontally shifting the supply and demand curves, with Figure 62 giving a numerical example."
why_here: "Source for the mathematical definition of DRIPE (price effect of added efficiency or reduced load on a linear supply-demand intersection), useful when explaining or checking how AESC's capacity DRIPE values arise in New England rate cases."
---

_Extractor note (not source text): this file holds PDF pp. 396-397 (printed pp. 378-379) of AESC 2024, Appendix H: DRIPE Derivation; the rest of the report is in the other files of this folder (see README.md), so those pages are marked not transcribed here. The text is transcribed verbatim, including the source's own slips, which are flagged inline with `[sic]` or `[source discrepancy: …]`. Equations are transcribed from the rendered page as LaTeX. In the printed equations for the equilibrium quantity and price, the superscript on $x$ and on $Price$ is a missing-glyph box in the PDF; the closing paragraph of PDF p. 397 calls these $x^{*}$ and $Price^{*}$, and they are written that way here._

[PDF pp. 1-395 not transcribed: front matter, Chapters 1-12 and Appendices A-G, in the other files of this folder (see README.md)]

[PDF p. 396 | printed p. 378]

# Appendix H: DRIPE Derivation

This appendix describes the derivation of DRIPE. This is the price effect of adding energy efficiency resources or reducing load.

For the supply curve (the price that suppliers will charge for supplying $x$ MW):

$$S_0 = b_S + m_S x,$$

and the demand curve (the price set by the VRR curve for $x$ MW):

$$D_0 = b_D - m_D x$$

Note that $m_D$ is the magnitude of the slope with the direction noted in the preceding negative sign.

The demand curve meets the supply curve at

$$x^{*} = \frac{b_D - b_S}{m_S + m_D}$$

And the market-clearing price is

$$Price^{*} = b_D - m_D \left( \frac{b_D - b_S}{m_S + m_D} \right)$$

A positive horizontal shift of $\alpha$ MW to the supply curve shifts the supply y-intercept downward. A negative horizontal shift of the demand curve shifts the demand y-intercept downward as well.

The horizontal shift of the supply curve shifts its y-intercept:

$$b_{supply\ shifted} = b_S - m_S \alpha$$

The Supply function, horizontally shifted $+ \alpha$ units, equals:

$$S_{shifted} = m_S x + (b_S - m_S \alpha) = m_S (x - \alpha) + b_S$$

Similarly, applying a negative horizontal shift of $\alpha$ units to the demand curve shifts its y-intercept:

$$b_{demand\ shifted} = b_D - m_D \alpha$$

The shifted Demand function equals:

$$D_{shifted} = b_D - m_D (\alpha + x)$$

[PDF p. 397 | printed p. 379]

Figure 62 provides examples that describe the rationale for the shift in the y-intercept for each function. The supply function is S = _x_ + 0 and the demand function is D = 400–2_x_. Adding 100 MW at \$0 shifts the supply curve right by 100×$m_S$ = 100. Subtracting 100 MW from the demand curve likewise shifts that curve left by 100, equivalent to shifting down by 100×$m_p$ [sic: $m_D$] = 200.

**Figure 62. Example of supply and demand impact**

[DIAGRAM DESCRIPTION: Figure 62. Example of supply and demand impact. Line chart with four straight lines on one set of axes. The horizontal axis is "Capacity (MW)", ticks at -100, -50, 0, 50, 100, 150, 200, 250, 300; the vertical axis is "Price (\$)", ticks at -600, -400, -200, 0, 200, 400, 600, 800. Each line is labelled directly at its right-hand end rather than in a separate legend. (1) "Supply" (blue-teal): rises from about -100 at -100 MW through 0 at 0 MW to about 300 at 300 MW, i.e. S = x. (2) "Supply Shifted +100" (red): parallel to Supply and shifted right by 100 MW, from about -200 at -100 MW to about 200 at 300 MW, i.e. S = x - 100. (3) "Demand" (orange): falls from about 600 at -100 MW to about -200 at 300 MW, i.e. D = 400 - 2x. (4) "Demand Shifted -100" (green): parallel to Demand and shifted left by 100 MW, from about 400 at -100 MW to about -400 at 300 MW, i.e. D = 200 - 2x. The shifted supply curve crosses the original demand curve and the original supply curve crosses the shifted demand curve at lower prices and quantities than the unshifted pair, showing the price effect (DRIPE) of the shift. Values read from the plotted lines are approximate; the equations follow from the functions stated in the text above.] [→ See original PDF page 397 for visual rendering]

For the intersection of the supply curve $S_0$ with the VRR $D_{shifted}$ and the intersection of $S_{shifted}$ with $D_0$, we find the equilibrium quantity $x^{*}$ and then substitute that into either half to get $Price^{*}$.

[PDF pp. 398-436 not transcribed: Appendices I-K (matrix of reliability sources, guide to cleared and uncleared measures, scaling factor for uncleared resources), in the other files of this folder (see README.md)]
