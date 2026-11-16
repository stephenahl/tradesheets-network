"""House Cleaning Pricing Calculator (Builder 2026-11-16). The generator is shared: etsy-digital/_calc/calc.py (key "cleaning").
Full pipeline (xlsx + LibreOffice recalc + images + guide): python3 etsy-digital/_calc/make.py cleaning <workdir>
This file only rebuilds the workbook: python3 build.py [out.xlsx]"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_calc"))
from calc import build
build("cleaning", sys.argv[1] if len(sys.argv) > 1 else "House-Cleaning-Pricing-Calculator.xlsx")
